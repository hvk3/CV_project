import numpy as np
import cv2

# TODO : For each detection, rotate back the bounding rectangle to be axis aligned if necessary (keeping its center and size constant).

detections = []
class Rectangle:
	def __init__(self):
		self.lower_left_x = 0
		self.lower_left_y = 0
		self.width = 0
		self.height = 0
		self.area = 0
	def setParams(self, lower_left_x, lower_left_y, width, height):
		self.lower_left_x = lower_left_x
		self.lower_left_y = lower_left_y
		self.width = width
		self.height = height
		self.area = self.width * self.height

def commonArea(a, b):
	area = 0
	width = min(a.lower_left_x + a.height , b.lower_left_x + b.height) - max(a.lower_left_x, b.lower_left_x)
	height = min(a.lower_left_y + a.width , b.lower_left_y + b.width) - max(a.lower_left_y, b.lower_left_y)
	if (width >= 0 and height >= 0):
		area = width * height
	return area

def computeMetrics(detectedRects):
	numRectangles = len(detectedRects)
	similarity = np.zeros((numRectangles, numRectangles))
	
	for i in xrange(numRectangles):
		for j in xrange(numRectangles):
			area = commonArea(detectedRects[i], detectedRects[j])
			similarity[i][j] = area * 2.0 / (detectedRects[i].area + detectedRects[j].area)
	return similarity

def averageRectangle(detectedRects):
	x_avg, y_avg, width_avg, height_avg = 0.0, 0.0, 0.0, 0.0
	numRectangles = len(detectedRects)
	for i in xrange(numRectangles):
		x_avg += detectedRects[i].lower_left_x
		y_avg += detectedRects[i].lower_left_y
		width_avg += detectedRects[i].width
		height_avg += detectedRects[i].height

	x_avg = (x_avg * 1.0) / numRectangles
	y_avg = (y_avg * 1.0) / numRectangles
	width_avg = (width_avg * 1.0) / numRectangles
	height_avg = (height_avg * 1.0) / numRectangles

	Rectangle avg;
	avg.setParams(x_avg, y_avg, width_avg, height_avg)

	return avg

def consolidatedDetections(detectedRects, similarityThreshold = 0.65, minimumSimilarRectangles = 3, intersectionThreshold = 0.2):
	similarity, intersection = computeMetrics(detectedRects)
	numRectangles = len(detectedRects)
	for i in xrange(numRectangles):
		temp = []
		for j in range(numRectangles):
			if (similarity[i][j] >= similarityThreshold and i != j):
				temp.append(detectedRects[j])
		if (len(temp) < count_threshold):
			temp = []
		else:
			R_avg = averageRectangle(temp)
			for j in xrange(len(temp)):
				intersection = commonArea(R_avg, temp[j])
				if (intersection < intersection_threshold):
					consolidatedDetections.append(temp[j])
	return consolidatedDetections
	