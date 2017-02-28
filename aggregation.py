import numpy as np
import cv2

detections = []
class rectangle:
	def __init__(self):
		top, bottom, right, left = 0, 0, 0, 0
		area = 0
	def setArea(w,h):
		area = w * h


def intersection(rectangles):
	w, h = len(rectangles), len(rectangles);
	similarity = [[0 for x in range(w)] for y in range(h)] 
	inter = [[0 for x in range(w)] for y in range(h)] 
	for i in range(0,len(rectangles)):
		for j in range(i+1, len(rectangles)):
			left = max(rectangles[i].left, rectangles[j].left)
			right = min(rectangles[i].right, rectangles[j].right)
			top = max(rectangles[i].top, rectangles[j].top)
			bottom = min(rectangles[i].bottom, rectangles[j].bottom)
			Area = (right - left) * (top - bottom);
			similarity[i][j] = float(2 * Area)/ float(rectangles[i].area + rectangles[j].area)
			# inter[i][j] = float(Area)/min(rectangles[i].area, rectangles[j].area )
	return similarity, inter

def ksimilar(sim_threshold, count_threshold, intersection_threshold, rectangles):
	similarity, inter = intersection(rectangles)
	len_rectangles = len(rectangles)
	results = [[] for i in xrange(len_rectangles)]
	for i in range(0, len_rectangles):
		for j in range(0, len_rectangles):
			if similarity[i][j] >= sim_threshold:
				results[i].append(rectangles[j])
		if len(results[i] < count_threshold):
			results[i] = []
			continue
		if (len(results[i]) > 0):
			resultant_rectangle = rectangle()
			resultant_rectangle.right = sum(results[i].right) / len(results[i])
			resultant_rectangle.left = sum(results[i].left) / len(results[i])
			resultant_rectangle.bottom = sum(results[i].bottom) / len(results[i])
			resultant_rectangle.top = sum(results[i].top) / len(results[i])
			resultant_rectangle.setArea(abs(resultant_rectangle.right - resultant_rectangle.left), abs(resultant_rectangle.bottom - resultant_rectangle.top))
			for k in xrange(len(detections)):
				left = max(detections[i].left, resultant_rectangle.left)
				right = min(detections[i].right, resultant_rectangle.right)
				top = max(detections[i].top, resultant_rectangle.top)
				bottom = min(detections[i].bottom, resultant_rectangle.bottom)
				Area = (right - left) * (top - bottom);
				if (Area * 1.0 / min(resultant_rectangle.area, detections[i].area) >= intersection_threshold):
					detections.remove(detections[i])
			detections.append(resultant_rectangle)
