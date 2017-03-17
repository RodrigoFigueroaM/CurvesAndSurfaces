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
from Bspline import Bspline
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QWidget
from GLStandardDrawingWindow import *
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
        self.curveType = "Quadratic Bézier"
        self.curvePoints = []

        self.userDefinedPointsBuffer = []
        self.historyBuffer = []
        self.history.append(Bspline())
        spline = self.history[-1] 
        for point in spline.controlPoints:
            self.userDefinedPoints.append(point)

    def mousePressEvent(self, event):
        if self.editFlag == False:
            a = Point( event.x(),self.height - event.y(), 1)
            self.userDefinedPoints.append(a)
            self.curvePoints.append(a)
    
            #if(len( self.userDefinedPoints)>3):
                #spline.compute()

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
                            curve.compute(curve.controlPoints)
                            point.translate(lastMousePosition.x() - point.x, self.height - lastMousePosition.y() - point.y,0)
                            self.updateGL()


    def mouseReleaseEvent(self, event):
        self.updateGL()

    def setCuverType(self,text):
        self.curveType = text

    def setEditFlag(self, state):
        self.editFlag = state

    def computeSpline(self):
        if len(self.curvePoints) > 1:
            spline = Bspline()
            spline.compute( self.curvePoints )
            self.history.append(spline)
            self.curvePoints = []
            self.updateGL()

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        self.userDefinedPointsBuffer = listToVertex(self.userDefinedPoints)
        self.historyBuffer=[]

        for obj in self.history:
            for point in obj.points:
                self.historyBuffer.append(point.toVertex())

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
        # GL.glDrawElements(GL.GL_LINE_STRIP, len(self.curvePointsBuffer), GL.GL_UNSIGNED_INT ,self.curvePointsBuffer)

    # Draw Curves
    def drawSpline(self, spline):
        # if len(self.history) > 0:
        #     GL.glColor3f(.85, .30, .90)
        #     GL.glPointSize(2.0)
        #     GL.glLineWidth(2.0)
        #     GL.glVertexPointer(3, GL.GL_FLOAT, 0, self.historyBuffer)
        #     GL.glDrawArrays(GL.GL_LINE_STRIP, 0, len(self.historyBuffer))
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
