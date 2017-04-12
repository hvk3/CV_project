import cv2
import numpy as np
import os

from VJaggregation import Rectangle, commonArea, computeMetrics, averageRectangle, consolidatedDetections

def rotatedFrames(frame):
	greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rotationsToApply = [ 3 * i for i in xrange(-3, 4) ]
	rotatedGreyFrames = []
	rows, cols = greyFrame.shape
	for i in xrange(len(rotationsToApply)):
		M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotationsToApply[i], 1)
		rotatedGreyFrames.append(cv2.warpAffine(greyFrame, M, (cols, rows)))
	return rotatedGreyFrames

def detectFacesInFrame(frame, classifiers, featureDescriptors, featureDetectors):
	rectangleColours = {0 : (255, 0, 0), 1 : (0, 255, 0), 2 : (0, 0, 255)}

	features = []
	featureRectangles = []
	rotatedGreyFrames = rotatedFrames(frame)
	for i in xrange(len(featureDetectors)):
		for j in xrange(len(rotatedGreyFrames)):
			features = featureDetectors[i].detectMultiScale(rotatedGreyFrames[j], 1.02, 3, 5)
			if (len(features) > 0):
				for (x, y, width, height) in features:
					featureRectangle = Rectangle()
					featureRectangle.setParams(x, y, width, height)
					featureRectangles.append(featureRectangle)
					cv2.rectangle(frame, (x, y), (x + width, y + height), rectangleColours[i])
	return featureRectangles

def aggregatedDetections(baseImages, classifiers, featureDescriptors, featureDetectors):
	rectangleColours = {0 : (255, 0, 0), 1 : (0, 255, 0), 2 : (0, 0, 255)}
	sortedBaseImages = sorted(os.listdir(baseImages))
	destinationDir = os.path.abspath(os.path.join(baseImages, os.pardir)) + '/VJ aggregated results/'
	for imageName in sortedBaseImages:
		if ('txt' in imageName):
			continue

		frameCount = imageName.split('_')[0]
		print frameCount
		if (int(frameCount) > 2000):
			break

		imageName = baseImages + imageName
		resultantImageName = destinationDir + frameCount + '_detectedRectangles.bmp'
		resultantVJonlyImageName = destinationDir + frameCount + '_detectedRectangles_VJonly.bmp'
		groundTruthConsolidatedDetections = destinationDir + frameCount + '_groundTruthConsolidatedDetections.txt'

		frame, frameCpy = cv2.imread(imageName), cv2.imread(imageName)
		featureRectangles = detectFacesInFrame(frame, classifiers, featureDescriptors, featureDetectors)

		if (len(featureRectangles) > 0):
			consolidatedRectangles = consolidatedDetections(featureRectangles)
			for consolidatedRectangle in consolidatedRectangles:
				x, y, width, height = (map(int, consolidatedRectangle.getParams()))
				consolidatedRectangle.setParams(x, y, width, height)

			uniqueConsolidatedRectangles = []
			flag = 0
			for consolidatedRectangle in consolidatedRectangles:
				if (len(uniqueConsolidatedRectangles) == 0):
					uniqueConsolidatedRectangles.append(consolidatedRectangle)
				else:
					for uniqueConsolidatedRectangle in uniqueConsolidatedRectangles:
						if (uniqueConsolidatedRectangle.getParams() == consolidatedRectangle.getParams()):
				 			flag = 1
					 		break
					if (flag == 0):
						uniqueConsolidatedRectangles.append(consolidatedRectangle)
				flag = 0
			if (len(uniqueConsolidatedRectangles) == 0):
				continue
			f = open(groundTruthConsolidatedDetections, 'w')
			for uniqueConsolidatedRectangle in uniqueConsolidatedRectangles:
				x, y, width, height = map(int, uniqueConsolidatedRectangle.getParams())
				GT = ','.join(map(str, map(int, uniqueConsolidatedRectangle.getParams())))
				if (len(GT) > 0):
					f.write(GT + '\n')
				cv2.rectangle(frame, (x, y), (x + width, y + height), rectangleColours[2])
			for featureRectangle in featureRectangles:
				x, y, width, height = map(int, featureRectangle.getParams())
				cv2.rectangle(frameCpy, (x, y), (x + width, y + height), rectangleColours[2])
			cv2.imwrite(resultantImageName, frame)
			cv2.imwrite(resultantVJonlyImageName, frameCpy)
			f.close()