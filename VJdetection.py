import cv2
import numpy as np
import os

from aggregation import *

base = '/home/hvk/opencv/data/haarcascades/'
groundTruthVideos = 'The Big Bang Theory/'
classifiers = ['haarcascade_frontalface_default.xml', 'haarcascade_eye.xml', 'haarcascade_profileface.xml']
featureDescriptors = ['ffaces', 'eyes', 'pfaces']
featureDetectors = []

for classifier in classifiers:
	featureDetectors.append(cv2.CascadeClassifier(base + classifier))


def generateGroundTruthFrames(base, groundTruthVideos, classifiers, featureDescriptors, featureDetectors):
	videoFiles = sorted(os.listdir(groundTruthVideos))
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
			for i in xrange(len(featureDetectors)):
				features = featureDetectors[i].detectMultiScale(greyFrame, 1.05, 5)
				if (len(features) != 0):
					for (lower_left_x, lower_left_y, width, height) in features:
						featureRectangle = Rectangle()
						featureRectangle.setParams(lower_left_x, lower_left_y, width, height)
						featureRectangles.append(featureRectangle)

						cv2.rectangle(frame, (lower_left_x, lower_left_y), (lower_left_x + width, lower_left_y + height), (0, 255, 0))
						cv2.imwrite(whereToDump + str(frameCount) + '_' + featureDescriptors[i] + '.bmp', frame)
						frameCount += 1