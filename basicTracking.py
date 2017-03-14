import cv2
import numpy as np
import os

def detectCameraShots(base, groundTruthVideos, differenceThreshold = 22500):
	videoFiles = sorted(os.listdir(groundTruthVideos))
	pwd = os.getcwd() + '/'
	for videoFile in videoFiles[:1]:
		videoName = pwd + groundTruthVideos + videoFile
		video = cv2.VideoCapture(videoName)

		frameCount = 0
		averageDiff = 0.0
		sumDiff = 0
		prevFrame = None
		while (True):
			ret, currFrame = video.read()
			if (ret != True):
				break
			if (prevFrame is None):
				prevFrame = currFrame
				continue
			hsvPrevFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2HSV)
			hsvCurrFrame = cv2.cvtColor(currFrame, cv2.COLOR_BGR2HSV)

			rows, cols = hsvCurrFrame.shape[:2]
			prevFrameQuads, currFrameQuads = [], []
			for i in xrange(2):
				for j in xrange(2):
					prevFrameQuads.append(hsvPrevFrame[i * rows / 2 : (i + 1) * rows / 2,  j * cols / 2 : (j + 1) * cols / 2])
					currFrameQuads.append(hsvCurrFrame[i * rows / 2 : (i + 1) * rows / 2,  j * cols / 2 : (j + 1) * cols / 2])

			diff = 0
			for i in xrange(4):
				prevFrameHist = cv2.calcHist([prevFrameQuads[i]], [0, 1], None, [30, 32], [0, 180, 0, 256])
				currFrameHist = cv2.calcHist([currFrameQuads[i]], [0, 1], None, [30, 32], [0, 180, 0, 256])

				prevFrameHist = prevFrameHist.flatten()
				currFrameHist = currFrameHist.flatten()

				temp = np.abs([prevFrameHist[i] - currFrameHist[i] for i in xrange(len(prevFrameHist))])
				diff += np.sum(temp)
			
			print "Difference between frames:", diff
			if (diff > differenceThreshold):
				print "Camera shot detected."
			prevFrame = currFrame
			frameCount += 1