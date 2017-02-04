#!/usr/bin/env python
'''
DrawingWindow
----------
**DrawingWindow*** creates a GLStandardDrawingWindow from QGLWidget.
Used to make a window that allows the user to draw Rectangles while dragging the mouse.

methods :
        __init__
        rotateEllipse
        paintGL

'''
import math
from Ellipse import Ellipse
from PyQt5 import QtCore
from GLStandardDrawingWindow import *

class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super().__init__()
        self.colorCounter = 1
        self.setMouseTracking(False)
        __ellipseWidth = 100
        __ellipseHeight = 450
        self.object = Ellipse( 0 , 0 , __ellipseWidth, __ellipseHeight)
        self.theta = 0
        self.objectType = None
        self.rotationPointX = self.object.cx
        self.rotationPointY = self.object.cy

    def rotateEllipse(self,theta):
        '''
        From Matrix Based Ellipse Geometry, Graphic Gems V
            if self.rotationPointX = 0 and self.rotationPointY = 0
            the ellipse wil rotate around the origin (0,0)
            multiply each point in the matrix by the rotation matrix
        '''
        newPoints = []
        self.theta = theta

        for point in self.object.points:
            xPrime = (point[0] -  self.rotationPointX) * math.cos(self.theta) - (point[1] - self.rotationPointY ) * math.sin(self.theta) +   self.rotationPointX
            yPrime = (point[0] -  self.rotationPointX) * math.sin(self.theta) + (point[1] - self.rotationPointY )  * math.cos(self.theta) +self.rotationPointY

            newPoints.append( (xPrime, yPrime , 1) )
        self.object.points = newPoints
        self.updateGL()

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        GL.glBegin(GL.GL_LINES)
        for point in self.object.points:
            GL.glVertex3fv(point)
        GL.glEnd()
        GL.glFlush()
