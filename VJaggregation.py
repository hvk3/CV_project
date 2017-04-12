import copy
import cv2
import numpy as np

class Rectangle:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.area = 0
	def setParams(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.area = self.width * self.height
	def getParams(self):
		return self.x, self.y, self.width, self.height

def commonArea(a, b):
	area = 0
	width = min(a.x + a.width , b.x + b.width) - max(a.x, b.x)
	height = min(a.y + a.height, b.y + b.height) - max(a.y, b.y)
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
		x_avg += detectedRects[i].x
		y_avg += detectedRects[i].y
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
	numRectangles = len(detectedRects)
	similarity = computeMetrics(detectedRects)
	similarRectangles = [[] for i in xrange(numRectangles)]
	combinedRectangles = []
	finalCombinedRectangles = []

	for i in xrange(numRectangles):
		R_star = detectedRects[i]
		similarRectangles[i].append(R_star)
		for j in xrange(numRectangles):
			if (similarity[i][j] >= similarityThreshold and i != j):
				similarRectangles[i].append(detectedRects[j])

	while (True):
		mostSimilarRectangles_i = np.argmax([len(similarRectangles[i]) for i in xrange(numRectangles)])

		if (len(similarRectangles[mostSimilarRectangles_i]) < minimumSimilarRectangles):
			return finalCombinedRectangles

		R_avg = averageRectangle(similarRectangles[mostSimilarRectangles_i])

		for i in xrange(len(combinedRectangles)):
			if (commonArea(R_avg, combinedRectangles[i]) * 1.0 / min(combinedRectangles[i].area, R_avg.area) < intersectionThreshold):
				print commonArea(R_avg, combinedRectangles[i]) * 1.0 / min(combinedRectangles[i].area, R_avg.area)
				finalCombinedRectangles.append(combinedRectangles[i])

		similarRectangles[mostSimilarRectangles_i] = []
		finalCombinedRectangles.append(R_avg)
		combinedRectangles.append(R_avg)
