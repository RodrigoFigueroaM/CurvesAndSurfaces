#!/usr/bin/env python
'''
DrawingWindow
----------
**DrawingWindow*** creates a GLStandardDrawingWindow from QGLWidget.
Used to make a window that allows the user to draw Rectangles and ellipseswhile dragging the mouse.
If shift key is hold down, while drawing a rectangle, it will automatically turn it into a square.
If shift key is hold down, while drawing an ellipse, it will automatically turn it into a circle.

Implements : __init__
             mousePressEvent
             mouseMoveEvent
             mouseReleaseEvent
             paintGL

helper method: distance

'''
from Rectangle import Rectangle
from Ellipse import Ellipse
from PyQt5 import QtCore
from GLStandardDrawingWindow import *

class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super().__init__()
        self.colorCounter = 1
        self.setMouseTracking(False)
        self.object = None
        self.objectType = None


    def setObjectType(self, name):
            self.objectType = name

    def mousePressEvent(self, event):
        #check the type of object we are drawing
        if self.objectType == "Rectangle":
            # create Rectangle with properties at the clicked point:
            self.object = Rectangle(event.x(),self.height - event.y(),event.x(), self.height - event.y())

        else:
            # create Ellipse with properties at the clicked point:
            self.object = Ellipse(event.x(), self.height - event.y(), event.x(), self.height - event.y())

    def mouseMoveEvent(self, event):
        #check the type of object we are re-drawing
        if type(self.object) is type(REC):
            self.object.points = []
            self.object.x1 = event.x()
            # Make square
            if event.modifiers() and QtCore.Qt.ShiftModifier:
                    #length and width have to be the same
                    self.object.y1 = distance (self.object.y0 , (distance(self.object.x0 ,self.object.x1 )) )
            else:
                self.object.y1 = distance(self.height , event.y())
            self.object.compute()

        elif type(self.object) is type(ELLI):
            self.object.points = []
            self.currentX = distance(self.object.cx, event.x())

            if event.modifiers() and QtCore.Qt.ShiftModifier:
                self.object.a =  self.currentX
                self.object.b = self.currentX

            else:
                self.object.a =  self.currentX
                self.object.b =  distance(self.object.cy,self.height - event.y())

            self.object.bresenhamAlg()

        else:
            pass
        self.updateGL()

    def mouseReleaseEvent(self, event):
        self.history.append(self.object)

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        GL.glBegin(GL.GL_POINTS)
        if self.object:
            for point in self.object.points:
                GL.glVertex2fv(point)
        for element in self.history:
            for point in element.points:
                GL.glVertex2fv(point)  #  #map points according to the coordinates they belong to



        GL.glEnd()
        GL.glFlush()


'''----------------------------------------------------------------------------
distance:
    calculates the distance between two points in one dimension
    params: p0, p1

    return: Integer distance
----------------------------------------------------------------------------'''
def distance(p0, p1):
    distance = (p1 - p0)
    return int (abs(distance) )
