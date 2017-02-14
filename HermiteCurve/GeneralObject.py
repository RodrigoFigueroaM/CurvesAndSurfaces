#!/usr/bin/env python
import math
from Point import Point
class GeneralObject(object):

    def __init__(self, *argv):
        super(GeneralObject, self ).__init__()
        self.points=[]
        self.color = [1, 0, 0]

    def __str__(self):
        return 'type= %s, %s' %(type(self), self.points)

    def translate(self, x, y):
    	newPoints =[]
    	for point in self.points:
    		newPoint = Point (point[0] + x ,point[1]+y ,point[2])
    		newPoints.append( newPoint.data() )
    	self.points = newPoints

    def scale(self, scalex, scaley):
    	newPoints =[]
    	for point in self.points:
    		newPoint = Point (point[0]* scalex, point[1]* scaley ,point[2])
    		newPoints.append( newPoint.data() )
    	self.points = newPoints

    def rotate(self, theta):
    	newPoints =[]
    	for point in self.points:
    		newPoint = Point (point[0] * math.cos(theta) - point[1] * math.sin(theta) , point[0]* math.sin(theta) + point[1] * math.cos(theta), point[2])
    		newPoints.append( newPoint.data() )
    	self.points = newPoints
