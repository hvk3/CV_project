import cv2
import numpy as np

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
	def getParams(self):
		return self.lower_left_x, self.lower_left_y, self.width, self.height

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

	avg = Rectangle()
	avg.setParams(x_avg, y_avg, width_avg, height_avg)

	return avg

def consolidatedDetections(detectedRects, similarityThreshold = 0.65, minimumSimilarRectangles = 3, intersectionThreshold = 0.2):
	prevLen = -1
	while (True):
		similarity = computeMetrics(detectedRects)
		i, j = 0, 0
		while (i < len(detectedRects)):
			while (j < len(detectedRects)):
				if (similarity[i][j] < similarityThreshold):
					detectedRects.pop(j)
				j += 1
			i += 1
			if (len(detectedRects) <= minimumSimilarRectangles):
				return detectedRects
			else:
				R_avg = averageRectangle(detectedRects)
				while (j < len(detectedRects)):
					intersection = commonArea(R_avg, detectedRects[j])
					if (intersection >= intersectionThreshold):
						detectedRects.pop(j)
					j += 1
		if (len(detectedRects) == 0 or prevLen == len(detectedRects)):
			return detectedRects
		prevLen = len(detectedRects)
	return detectedRects
