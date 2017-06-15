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
'''

import math
import MyPackages
from MyPackages.geometry.Point import Point
from MyPackages.curves.NURBSTest import NURBS
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QWidget
from MyPackages.qtPackage.GLStandardDrawingWindow import *
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, \
                                                  glBindVertexArray

class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super(DrawingWindow,self).__init__()
        self.history=[]
        self.userDefinedPoints = []
        self.setMouseTracking(True)
        self.editFlag = False
        self.curvePoints = []

        self.userDefinedPointsBuffer = []
        self.historyBuffer = []

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
                            point.translate(lastMousePosition.x() - point.x, self.height - lastMousePosition.y() - point.y,0)
                            self.updateSpline(curve)
                            self.updateGL()


    def mouseReleaseEvent(self, event):
        self.updateGL()

    def setCuverType(self,text):
        self.curveType = text

    def setEditFlag(self, state):
        self.editFlag = state

    def computeSpline(self, degree = 0, knotVectorType = None ):
        if len(self.curvePoints) > 1:
            spline = NURBS( knotVectorType )
            spline.compute( controlPoints = self.curvePoints,  degree = degree, knotVectorType = knotVectorType , homogenousCoordinates = [1 for x in range(0,len( self.curvePoints))])
            self.history.append(spline)
            self.curvePoints = []
            self.updateGL()
   
    def updateSpline(self, spline = None):
        if spline:
            print(spline.degree)
            spline.compute(controlPoints = spline.controlPoints,  degree = spline.degree,  knotVector =  spline.knots, homogenousCoordinates = spline.homogenousCoordinates)
            self.updateGL()

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        self.userDefinedPointsBuffer = listToVertex(self.userDefinedPoints)
        self.historyBuffer=[]
   
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)

        self.drawPoints()

        for spline in self.history:
            self.drawSpline(spline)
            if self.editFlag == True:
                self.drawControlPolygon(spline)

        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)

    # Draw user points
    def drawPoints(self):
        GL.glColor3ub(103, 204, 207)
        GL.glPointSize(5.0)
        GL.glVertexPointer(3, GL.GL_FLOAT, 0, self.userDefinedPointsBuffer)
        GL.glDrawArrays(GL.GL_POINTS,0, len(self.userDefinedPointsBuffer))

    def drawControlPolygon(self, spline):
        GL.glColor3ub(76, 76, 76)
        GL.glLineWidth(1.0)
        GL.glBegin(GL.GL_LINE_STRIP)
        for point in spline.controlPoints:
            GL.glVertex3fv(point.data())  #  #map points according to the coordinates they belong to
        GL.glEnd()
  
    # Draw Curves
    def drawSpline(self, spline):
       GL.glColor3ub(216, 76, 230)
       GL.glPointSize(2.0)
       GL.glLineWidth(2.0)
       GL.glBegin(GL.GL_LINE_STRIP)
       for point in spline.points:
            GL.glVertex3fv(point.data())  #  #map points according to the coordinates they belong to
       GL.glEnd()

def listToVertex(inList):
    outList=[]
    for point in inList:
        outList.append(point.toVertex())
    return outList
