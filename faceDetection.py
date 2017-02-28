import numpy as np
import cv2

from aggregation import *

face_cascade = cv2.CascadeClassifier('/home/ishita/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/ishita/opencv/data/haarcascades/haarcascade_eye.xml')
#img = cv2.imread('/home/ishita/Desktop/photo.png')
vid = cv2.VideoCapture('/home/ishita/Desktop/CV/Project/The Big Bang Theory/01x01 - Pilot.avi')
flag = 0
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver)  < 3 :
        fps = vid.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
else:
	fps = vid.get(cv2.CAP_PROP_FPS)
	print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

all_rectangles = []

cnt = 0
while(cnt<750):
	cnt = cnt+1
	flag = 1
	ret, frame = vid.read()

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		r = rectangle()
		r.left = 
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		if flag>0:
			cv2.imwrite( "/home/ishita/Desktop/photo" + str(cnt) + ".png", frame );
		flag = 0
		
cv2.waitKey(0)
cv2.destroyAllWindows()