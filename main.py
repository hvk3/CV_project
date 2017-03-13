from VJdetection import *

base = '/home/hvk/opencv/data/haarcascades/'
groundTruthVideos = 'The Big Bang Theory/'
classifiers = ['haarcascade_frontalface_default.xml', 'haarcascade_profileface.xml']
featureDescriptors = ['ffaces', 'pfaces']
featureDetectors = []

for classifier in classifiers:
	featureDetectors.append(cv2.CascadeClassifier(base + classifier))

if __name__ == '__main__':
	detectFacesInFrames(base, groundTruthVideos, classifiers, featureDescriptors, featureDetectors)