import cv2
import numpy as np
import os

def detectCameraShots(baseImages, differenceThreshold = 225000):
	prevFrame, currFrame = None, None
	cameraShots = []

	for image in sorted(os.listdir(baseImages)):
		frameCount = image.split('_')[0]
		if (int(frameCount) >= 2000):
			break
		currFrame = cv2.imread(baseImages + image)
		if (prevFrame is None):
			prevFrame = currFrame
			continue
		rows, cols = currFrame.shape[:2]

		HSVprevFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2HSV)
		HSVcurrFrame = cv2.cvtColor(currFrame, cv2.COLOR_BGR2HSV)

		HSVprevFrameQuads = [HSVprevFrame[ : rows / 2, : cols / 2], HSVprevFrame[ : rows / 2, cols / 2 : ], HSVprevFrame[ rows / 2 : , : cols / 2 ], HSVprevFrame[rows / 2 : , cols / 2 : ]]
		HSVcurrFrameQuads = [HSVcurrFrame[ : rows / 2, : cols / 2], HSVcurrFrame[ : rows / 2, cols / 2 : ], HSVcurrFrame[ rows / 2 : , : cols / 2 ], HSVcurrFrame[rows / 2 : , cols / 2 : ]]

		HSVprevFrameQuadsHist = [cv2.calcHist([HSVprevFrameQuads[i]], [0, 1], None, [30, 32], [0, 180, 0, 256]) for i in xrange(4)]
		HSVcurrFrameQuadsHist = [cv2.calcHist([HSVcurrFrameQuads[i]], [0, 1], None, [30, 32], [0, 180, 0, 256]) for i in xrange(4)]
		
		absDiff = 0.0
		for i in xrange(4):
			for j in xrange(30):
				for k in xrange(32):
					absDiff += abs(HSVprevFrameQuadsHist[i][j][k] - HSVcurrFrameQuadsHist[i][j][k])

		if (absDiff >= differenceThreshold):
			cameraShots.append(frameCount)

		prevFrame = currFrame
	return cameraShots

def getMaskedFrame(frame, groundTruthBoundingBox):
	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	x, y, width, height = groundTruthBoundingBox
	mask = np.zeros(grayFrame.shape).astype('uint8')
	cv2.rectangle(mask, (x, y), (x + width, y + height), (255, 255, 255), thickness = -1)

	return np.bitwise_and(mask, grayFrame)

def initialDetections(frame, groundTruthBoundingBox, minDistance = 5):
	maskedGrayFrame = getMaskedFrame(frame, groundTruthBoundingBox)
	# cv2.imshow('image', maskedGrayFrame)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	STcorners = cv2.goodFeaturesToTrack(maskedGrayFrame, 500, 0.2, minDistance)

	return STcorners

def KLTtracker(baseImages, baseDetectedImages):
	featureParams = dict(maxCorners = 50, qualityLevel = 0.3, minDistance = 7, blockSize = 7)
	kltParams = dict( winSize  = (15, 15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

	cameraShots = map(int, detectCameraShots(baseImages))
	prevFramePointsToTrack, currFramePointsToTrack = [], []
	prevFrame, currFrame = None, None
	groundTruthBoundingBoxes = {}

	for file in sorted(os.listdir(baseDetectedImages)):
		if ('txt' in file):
			frameCount = (file.split('_')[0])
			boundingBoxes = []
			f = open(baseDetectedImages + file, 'r')
			for line in f.readlines():
				line = map(int, line.strip().split(','))
				if (len(line) > 0):
					boundingBoxes.append(line)
			f.close()
			groundTruthBoundingBoxes[int(frameCount)] = boundingBoxes

	prevShotFrameCount, currShotFrameCount = -1, -1
	framesDetected = groundTruthBoundingBoxes.keys()
	
	prevShotFrameCount = min(framesDetected)
	shotBeginEnd = []
	for detectedFrame in framesDetected:
		if (detectedFrame in cameraShots):
			currShotFrameCount = detectedFrame
			shotBeginEnd.append([prevShotFrameCount, currShotFrameCount])
			prevShotFrameCount = currShotFrameCount

	for i in xrange(len(shotBeginEnd)):
		if (shotBeginEnd[i][1] - shotBeginEnd[i][0] < 60):
			stepSize = (shotBeginEnd[i][1] - shotBeginEnd[i][0]) / 6
		else:
			stepSize = 10

		STprevPoints, STcurrPoints = [], []
		for j in xrange(shotBeginEnd[i][0], shotBeginEnd[i][1] + 1, stepSize):

			if (j == shotBeginEnd[i][0]):
				imgName = str(j)
				while (len(imgName) < 5):
					imgName = '0' + imgName

				prevFrame = currFrame = cv2.imread(baseImages + imgName + '_groundTruth.bmp')
				for k in xrange(len(groundTruthBoundingBoxes[j])):
					STprevPoints.append(initialDetections(prevFrame, groundTruthBoundingBoxes[j][k]))
				continue

			if (j == shotBeginEnd[i][1]):
				prevFrame = None
				STprevPoints, STcurrPoints = [], []
				continue

			for k in xrange(len(STprevPoints)):
				currFrameGoodPoints, status, error = cv2.calcOpticalFlowPyrLK(prevFrame, currFrame, STprevPoints[k], None, **kltParams)
				prevFrameBestPoints = STprevPoints[k][status == 1]
				currFrameBestPoints = currFrameGoodPoints[status == 1]

				STprevPoints[k] = currFrameGoodPoints
				if (len(currFrameBestPoints) < 3 or len(prevFrameBestPoints) < 3):
					print j
					continue
				M = cv2.getAffineTransform(prevFrameBestPoints[:3], currFrameBestPoints[:3])
				print M
			prevFrame = currFrame