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
attributes
----------
'''
import math
from Point import Point
from CatmullRom import CatmullRom
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QWidget
from GLStandardDrawingWindow import *

class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super(DrawingWindow,self).__init__()
        self.history=[]
        self.userDefinedPoints = []
        self.animationObjects = []
        self.setMouseTracking(True)
        self.history.append(CatmullRom())
        self.editFlag = False

    def mousePressEvent(self, event):
        if self.editFlag == False:
            a = Point( event.x(),self.height - event.y(), 1)
            self.userDefinedPoints.append(a)

    def mouseMoveEvent(self, event):
        if self.editFlag == True:
            if event.buttons() == QtCore.Qt.LeftButton:
                lastMousePosition = event.pos()
                bounds = 5
                for point in self.userDefinedPoints:
                    #mouse bound. Raise flag because space is taken
                    if ( point.x > event.x() - bounds
                        and point.x <  event.x() + bounds
                        and  point.y <  self.height - event.y() +  bounds
                        and  point.y > self.height - event.y()  - bounds ):
                        point.translate(lastMousePosition.x() - point.x, self.height - lastMousePosition.y() - point.y,0)
                        self.updateGL()

    def mouseReleaseEvent(self, event):
        self.updateGL()

    def setEditFlag(self, state):
        self.editFlag = state

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        self.drawPoints()
        if len(self.userDefinedPoints) >= 4:
            spline = self.history[-1]
            spline.compute(self.userDefinedPoints)
            self.drawCurve()
        self.drawAnimationObjects()

    # Draw user points
    def drawPoints(self):
        GL.glColor3f(.48, .80, .81)
        GL.glPointSize(5.0)
        GL.glBegin(GL.GL_POINTS)
        for point in self.userDefinedPoints:
            GL.glVertex3fv(point.data())
        GL.glEnd()

    # Draw Curves
    def drawCurve(self):
        GL.glColor3f(.85, .30, .90)
        GL.glPointSize(2.0)
        GL.glLineWidth(2.0)
        GL.glBegin(GL.GL_LINE_STRIP)
        for element in self.history:
            for point in element.points:
                GL.glVertex3fv(point.data())  #  #map points according to the coordinates they belong to
        GL.glEnd()

    #Draw objects for animation
    def drawAnimationObjects(self):
        GL.glColor3f(.9, .4, .5)
        GL.glPointSize(2.0)
        GL.glLineWidth(4.0)
        GL.glBegin(GL.GL_LINE_STRIP)
        for element in self.animationObjects:
            for point in element.points:
                GL.glVertex3fv(point)  #  #map points according to the coordinates they belong to
        GL.glEnd()
