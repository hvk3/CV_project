import cv2
import os

from VJdetection import rotatedFrames, aggregatedDetections
from basicTracking import detectCameraShots, KLTtracker

base = '/home/hvk/opencv/data/haarcascades/'
groundTruthVideos = 'The Big Bang Theory/'
baseImages = 'videoDump/01/Ground Truth/'
baseDetectedImages = 'videoDump/01/VJ aggregated results/'
classifiers = ['haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml']
featureDescriptors = ['ffaces', 'pfaces']
featureDetectors = []

for classifier in classifiers:
	featureDetectors.append(cv2.CascadeClassifier(base + classifier))

def loadFrames(groundTruthVideos):
	videoFiles = sorted(os.listdir(groundTruthVideos))
	pwd = os.getcwd() + '/'
	for videoFile in videoFiles[:1]:
		whereToDump = 'videoDump/' + videoFile[3:5] + '/'	# In general; otherwise this is the same as baseImages
		videoName = pwd + groundTruthVideos + videoFile
		video = cv2.VideoCapture(videoName)
		frameCount = 0

		while (True):
			ret, frame = video.read()
			if (ret != True):
				break
			imgName = str(frameCount)
			while (len(imgName) < 5):
				imgName = '0' + imgName
			cv2.imwrite(whereToDump + imgName + '_groundTruth.bmp', frame)
			frameCount += 1

if __name__ == '__main__':
	# Generate ground truth frames from video files.
	# loadFrames(groundTruthVideos)
	# a) Viola-Jones detection with and without slight rotations.
	# aggregatedDetections(baseImages, classifiers, featureDescriptors, featureDetectors)
	# b) KLT tracking.
	KLTtracker(baseImages, baseDetectedImages)