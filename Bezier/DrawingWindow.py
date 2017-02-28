#!/usr/bin/env python
'''
DrawingWindow
----------
**DrawingWindow*** creates a GLStandardDrawingWindow from QGLWidget.
Implements : mousePressEvent
             mouseMoveEvent
             mouseReleaseEvent
             paintGL
attributes
----------
    *colorCounter to decide the color of the lines.
'''
import math
from Point import Point
from Bezier import QuadraticBezier, CubicBezier
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QWidget
from GLStandardDrawingWindow import *

class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super(DrawingWindow,self).__init__()
        self.history=[]
        self.userDefinedPoints = []
        self.setMouseTracking(True)
        self.editFlag = False
        self.curveType = "Quadratic Bézier"

        self.curvePoints = []

    def mousePressEvent(self, event):
        if self.editFlag == False:
            a = Point( event.x(),self.height - event.y(), 1)
            self.userDefinedPoints.append(a)
            self.curvePoints.append(a)


    def mouseMoveEvent(self, event):
        if self.editFlag == True:
            if event.buttons() == QtCore.Qt.LeftButton:
                lastMousePosition = event.pos()
                bounds = 5
                for curve in self.history:
                    for point in self.userDefinedPoints:
                        if ( point.x > event.x() - bounds
                            and point.x <  event.x() + bounds
                            and  point.y <  self.height - event.y() +  bounds
                            and  point.y > self.height - event.y()  - bounds ):
                            if(type(curve) == type(QuadraticBezier()) ):
                                curve.compute(curve.controlPoints[0],curve.controlPoints[1],curve.controlPoints[2])
                            else:
                                curve.compute(curve.controlPoints[0],curve.controlPoints[1],curve.controlPoints[2],curve.controlPoints[3])
                            point.translate(lastMousePosition.x() - point.x, self.height - lastMousePosition.y() - point.y,0)
                            self.updateGL()


    def mouseReleaseEvent(self, event):
        if self.curveType == "Quadratic Bézier":
            self.drawQuadraticBezier()
        else:
            self.drawCubicBezier()
        self.updateGL()

    def setCuverType(self,text):
        self.curveType = text

    def setEditFlag(self, state):
        self.editFlag = state

    def drawQuadraticBezier(self):
        if len(self.userDefinedPoints) > 0:
            if len(self.curvePoints)  == 3:
                spline = QuadraticBezier()
                spline.compute(self.curvePoints[0],self.curvePoints[1], self.curvePoints[2] )
                self.history.append(spline)
                self.curvePoints = []

    def drawCubicBezier(self):
        if len(self.userDefinedPoints) > 0:
            if len(self.curvePoints) == 4:
                spline = CubicBezier()
                spline.compute(self.curvePoints[0], self.curvePoints[1], self.curvePoints[2], self.curvePoints[3])
                self.history.append(spline)
                self.curvePoints = []

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        self.drawPoints()
        self.drawControlPolygon()
        self.drawCurve()

    # Draw user points
    def drawPoints(self):
        GL.glColor3f(.48, .80, .81)
        GL.glPointSize(5.0)
        GL.glBegin(GL.GL_POINTS)
        for point in self.userDefinedPoints:
            GL.glVertex3fv(point.data())
        GL.glEnd()

    def drawControlPolygon(self):
        GL.glColor3f(.3, .3, .3)
        GL.glLineWidth(0.5)
        GL.glBegin(GL.GL_LINE_STRIP)
        for curve in self.history:
            for conrolPoint in curve.controlPoints:
                GL.glVertex3fv(conrolPoint.data())
        GL.glEnd()

    # Draw Curves
    def drawCurve(self):
        GL.glColor3f(.85, .30, .90)
        GL.glPointSize(2.0)
        GL.glLineWidth(2.0)
        GL.glBegin(GL.GL_POINTS)
        for element in self.history:
            for point in element.points:
                GL.glVertex3fv(point.data())    #map points according to the coordinates they belong to
        GL.glEnd()
