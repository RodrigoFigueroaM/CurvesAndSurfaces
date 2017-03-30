#!/usr/bin/env python
import math
class Point(object):
    """docstring for Vector"""
    def __init__(self, *arg):
        super(Point, self).__init__()
        if(len(arg) == 0):
            self.x = 0
            self.y = 0 
            self.z = 0
        else:
            self.x, self.y, self.z = arg

    def __str__(self):
        return 'type: %s (%s, %s, %s)' %(type(self), self.x, self.y, self.z)

    def __add__(self, other):
        if type(other) == type(Point()): 
            result = Point( self.x + other.x, self.y + other.y, self.z )
        else:
            result = Point( self.x + other, self.y + other, self.z)
        return result

    def __sub__(self, other):
        if type(other) ==type(Point()): 
            result = Point( self.x - other.x, self.y - other.y, self.z )
        else:
            result = Point( self.x - other, self.y - other, self.z )
        return result

    def __mul__(self, other):
        if type(other) == type(Point()): 
            result = Point( self.x * other.x, self.y * other.y, self.z )
        else:
            result = Point( self.x * other, self.y * other, self.z )
        return result

    def __truediv__(self, other):
        if type(other) == type(Point()): 
            result = Point( self.x / other.x, self.y / other.y, self.z )
        else:
            result = Point( self.x / other, self.y / other, self.z )
        return result

    def data(self):
        return self.x, self.y, self.z

    def toVertex(self):
        toGL = [self.x, self.y, self.z]
        return toGL

    def translate(self, x, y,z ):
    	self.x += x
    	self.y += y
    	self.z = z

    def rotate(self, theta):
        tempx = self.x * math.cos(theta) - self.y * math.sin(theta)
        tempy = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x = tempx
        self.y = tempy

    def rotateOn(self, theta, x, y):
        tempx = (self.x -  x) * math.cos(theta) - (self.y - y ) * math.sin(theta) + x
        tempy = (self.x -  x) * math.sin(theta) + (self.y - y)  * math.cos(theta) + y
        self.x = tempx
        self.y = tempy

    def normalize(self):
        magnitude = math.sqrt(self.x * self.x + self.y * self.y)
        self.x = self.x / magnitude
        self.y = self.y / magnitude
