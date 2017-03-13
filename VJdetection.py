import cv2
import numpy as np
import os

from VJaggregation import *

def applyRotation(greyFrame):
	rotationsToApply = [ 3 * i for i in xrange(-3, 4) ]
	rotatedGreyFrames = []
	rows, cols = greyFrame.shape
	for i in xrange(len(rotationsToApply)):
		M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotationsToApply[i], 1)
		rotatedGreyFrames.append(cv2.warpAffine(greyFrame, M, (cols, rows)))
	return rotatedGreyFrames

def detectFacesInFrames(base, groundTruthVideos, classifiers, featureDescriptors, featureDetectors):
	videoFiles = sorted(os.listdir(groundTruthVideos))
	colorFeatures = {0 : (255, 0, 0), 1 : (0, 255, 0), 2 : (0, 0, 255)}
	pwd = os.getcwd() + '/'
	for videoFile in videoFiles[:1]:
		whereToDump = 'videoDump/' + videoFile[3:5] + '/'
		videoName = pwd + groundTruthVideos + videoFile
		video = cv2.VideoCapture(videoName)

		frameCount = 0
		while (True):
			ret, frame = video.read()
			if (ret != True):
				break
			greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			features = []
			featureRectangles = []
			rotatedGreyFrames = applyRotation(greyFrame)
			for i in xrange(len(featureDetectors)):
				for j in xrange(len(rotatedGreyFrames)):
					features = featureDetectors[i].detectMultiScale(rotatedGreyFrames[j], 1.05, 5)
					if (len(features) > 0):
						for (lower_left_x, lower_left_y, width, height) in features:
							featureRectangle = Rectangle()
							featureRectangle.setParams(lower_left_x, lower_left_y, width, height)
							featureRectangles.append(featureRectangle)
							cv2.rectangle(frame, (lower_left_x, lower_left_y), (lower_left_x + width, lower_left_y + height), colorFeatures[i])
			if (len(featureRectangles) > 0):
				consolidatedRectangles = consolidatedDetections(featureRectangles)
				print frameCount, len(consolidatedRectangles)
				for consolidatedRectangle in consolidatedRectangles:
					lower_left_x, lower_left_y, width, height = map(int, consolidatedRectangle.getParams())
					cv2.rectangle(frame, (lower_left_x, lower_left_y), (lower_left_x + width, lower_left_y + height), colorFeatures[2])
				cv2.imwrite(whereToDump + str(frameCount) + '.bmp', frame)
			frameCount += 1