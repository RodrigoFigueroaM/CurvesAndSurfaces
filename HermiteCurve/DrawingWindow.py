#!/usr/bin/env python
'''
DrawingWindow
----------
**DrawingWindow*** creates a GLStandardDrawingWindow from QGLWidget.
Used to make a window that allows the user to draw Rectangles while dragging the mouse.

Implements : mousePressEvent
             mouseMoveEvent
             mouseReleaseEvent
             paintGL

helper method: distance

attributes
----------
    *colorCounter to decide the color of the lines.
'''
import math
from Point import Point
from Helper import distance, isElementOfVector
from Vector import Vector
from HermiteCurve import HermiteCurve
from random import random

from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QWidget
from GLStandardDrawingWindow import *


class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(False)
        self.numberOfClicks = 0
        self.vectors = []
        self.vectorsPoints = []
        self.points = []
        self.update = 0.0

        self.busyPixel = False # flag for taken space
        self.selectedPoint = object
        self.rotate = .1
        self.selectedPointIndex = 0

    def mousePressEvent(self, event):
        # check if pixel busy
        bounds = 5
        i = 0
        for point in self.points:
            #mouse bounds. Raise flag because space is taken
            if ( point.x > event.x() - bounds
                and point.x <  event.x() + bounds
                and  point.y <  self.height - event.y() +  bounds
                and  point.y > self.height - event.y()  - bounds ):

                self.busyPixel = True
                self.selectedPointIndex = i
                self.selectedPoint = point
                self.lastMousePosition = event.pos()
                print ("BUSY")
                break
            i += 1

        #Click on mouse and set a point
        if self.busyPixel == False:
            self.numberOfClicks = self.numberOfClicks + 1
            if self.numberOfClicks% 2 != 0:
                self.points.append ( Point(event.x(),self.height - event.y(), 1))

            else:
                a = self.points[-1]
                b = Point(event.x(),self.height - event.y(), 1)
                m0 = Vector (a,b)

                self.points.append(b)

                self.vectors.append(m0)
                self.vectorsPoints.append( (m0.pointOne.data()) )
                self.vectorsPoints.append( (m0.pointTwo.data()) )

            if self.numberOfClicks % 4 == 0:
                v0 = self.vectors[-2]
                v1 = self.vectors[-1]
                v0dist = distance(v0.pointTwo.y, v0.pointOne.y)
                v1dist = distance(v1.pointTwo.y, v1.pointOne.y)

                if v0.pointOne.x > v1.pointOne.x:
                    v0 , v1 = v1 , v0

                hermiteCurve = HermiteCurve()

                hermiteCurve.compute(v0.pointOne, v0.slope() * v0dist, v1.pointOne, v1.slope() * v1dist)
                hermiteCurve.scale(distance(v1.pointOne.x, v0.pointOne.x), 1)
                hermiteCurve.translate(v0.pointOne.x,0)
                self.history.append(hermiteCurve)

    def mouseMoveEvent(self, event):
        if self.busyPixel == True:
            mousedx = .01
            mousedy = .01

            if len(self.history) > 0 :
                v0 = self.vectors[-2]
                v1 = self.vectors[-1]

                if v0.pointOne.x > v1.pointOne.x:
                    v0 , v1 = v1 , v0

                rotationPoint = v0.pointOne
                hermiteCurve = self.history[-1]
                v0dist = distance(v0.pointTwo.y, v0.pointOne.y)
                v1dist = distance(v1.pointTwo.y, v1.pointOne.y)

                if self.selectedPoint == v1.pointOne or self.selectedPoint == v1.pointTwo:
                    rotationPoint = v1.pointOne

                distanceX = distance(self.selectedPoint.x, event.x())
                distanceY =  distance(self.selectedPoint.y, self.height - event.y())
                revertZero = 1
                revertOne = 1
                # left/ mouse moving right
                if self.lastMousePosition.x() > event.x():
                    if rotationPoint.y <= self.selectedPoint.y :
                        self.selectedPoint.rotateOn( mousedx, rotationPoint.x, rotationPoint.y )
                    else:
                        self.selectedPoint.rotateOn( -1 * mousedx, rotationPoint.x, rotationPoint.y )

                # right/ mouse moving left
                elif self.lastMousePosition.x() < event.x():
                    if rotationPoint.y >= self.selectedPoint.y :
                        self.selectedPoint.rotateOn( mousedx, rotationPoint.x, rotationPoint.y )
                    else:
                        self.selectedPoint.rotateOn( -1 * mousedx, rotationPoint.x, rotationPoint.y )

                if not isElementOfVector(rotationPoint, v0):
                    if rotationPoint.x > self.selectedPoint.x and rotationPoint.y < self.selectedPoint.y:
                        revertOne = -1
                    if rotationPoint.x > self.selectedPoint.x and rotationPoint.y > self.selectedPoint.y:
                        revertOne = -1
                else:
                    if rotationPoint.x > self.selectedPoint.x and rotationPoint.y < self.selectedPoint.y:
                        revertZero = -1
                    if rotationPoint.x > self.selectedPoint.x and rotationPoint.y > self.selectedPoint.y:
                        revertZero = -1

                if self.selectedPoint == v0.pointOne or self.selectedPoint == v1.pointOne:


                    # left
                    if self.lastMousePosition.x() > event.x():
                        self.selectedPoint.translate(-1 * distanceX * mousedx, distanceY * mousedy, 0)

                    # right
                    if self.lastMousePosition.x() < event.x():
                        self.selectedPoint.translate(distanceX * mousedx, distanceY * mousedy, 0)

                    # up
                    if self.lastMousePosition.y() < event.y():
                        # hermiteCurve.scale(abs(v1.pointOne.x - v0.pointOne.x), abs(v1.pointOne.y - v0.pointOne.y) )
                        self.selectedPoint.translate(distanceX * mousedx,  -1 * distanceY * mousedy, 0)

                    if self.lastMousePosition.y() > event.y():
                        self.selectedPoint.translate(distanceX * mousedx, distanceY * mousedy, 0)

                hermiteCurve.compute(v0.pointOne, revertZero * v0.slope() * v0dist, v1.pointOne, revertOne * v1.slope() * v1dist)
                hermiteCurve.scale(distance(v1.pointOne.x, v0.pointOne.x), 1)
                hermiteCurve.translate(v0.pointOne.x,0)
                self.vectorsPoints[self.selectedPointIndex] = self.selectedPoint.data()
                self.updateGL()

    def mouseReleaseEvent(self, event):
        self.busyPixel = False
        self.updateGL()

    def keyPressEvent(self, event):
        hermiteCurve = self.history[-1]
        v0 = self.vectors[-2]
        v1 = self.vectors[-1]

        print ( "CURVE",hermiteCurve)
        print ( "Points",int(v0.pointOne.y) == int(v1.pointOne.y), int(v0.pointOne.y), int(v1.pointOne.y))

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        # Draw vectors
        GL.glColor3f(.50, .80, .81)
        GL.glBegin(GL.GL_LINES)
        for point in self.vectorsPoints:
            GL.glVertex3fv(point)
        GL.glEnd()

        # Draw points on vectors
        GL.glPointSize(10.0)
        GL.glColor3f(.30, .30, .51)
        GL.glBegin(GL.GL_POINTS)
        for point in self.vectorsPoints:
            GL.glVertex3fv(point)
        GL.glEnd()


        # Draw Curves
        GL.glColor3f(.85, .30, .90)
        GL.glPointSize(2.0)
        GL.glBegin(GL.GL_POINTS)
        for element in self.history:
            for point in element.points:
                GL.glVertex3fv(point)  #  #map points according to the coordinates they belong to
        GL.glEnd()
        GL.glFlush()
