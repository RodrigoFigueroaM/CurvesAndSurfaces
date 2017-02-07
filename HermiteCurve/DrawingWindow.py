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
from random import randint
from PyQt5 import QtCore
from GLStandardDrawingWindow import *

class DrawingWindow(GLStandardDrawingWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(False)
        self.li=[]
    
    def mousePressEvent(self, event):

        '''p(t) = (2t^3 - 3t^2 + 1)p0 + (t^3 - 2t^2 + t)m0 + ( -2t^3 + 3t^2)p1 + (t^3 - t^2)m1'''
        # m0, m1 derivatives 

        p0 = 1
        p1 = 0
        m0 = 0
        m1 = 0
       
        t = 0.0 

        while t < 1.0:
            t3 = t * t * t
            t2 = t * t
            pt  = (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + ( -2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1
            self.li.append( (t, pt, 1) )
            t += 0.001

        p0 = 0
        p1 = 1
        m0 = 0
        m1 = 0
       
        t = 0.0 

        while t < 1.0:
            t3 = t * t * t
            t2 = t * t
            pt  = (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + ( -2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1
            self.li.append( (t, pt, 1) )
            t += 0.001

        p0 = 0
        p1 = 0
        m0 = 1
        m1 = 0
       
        t = 0.0 

        while t < 1.0:
            t3 = t * t * t
            t2 = t * t
            pt  = (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + ( -2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1
            self.li.append( (t, pt, 1) )
            t += 0.001

        p0 = 0
        p1 = 0
        m0 = 0
        m1 = 1
       
        t = 0.0 

        while t < 1.0:
            t3 = t * t * t
            t2 = t * t
            pt  = (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + ( -2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1
            self.li.append( (t, pt, 1) )
            t += 0.001

    def mouseReleaseEvent(self, event):
    #     listlist = []
    #     # for element in self.history:
    #     #     # for point in element.points:
    #     #     listlist.append( (element[0] + randint(10,100) , element[1], 1) )
        self.history = self.li
        self.updateGL()

    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        GL.glBegin(GL.GL_POINTS)
        # if self.object:
        #     for point in self.object.points:
        #         GL.glVertex2fv(point)
        for element in self.history:
            # for point in element.points:
            GL.glVertex3fv(element)  #  #map points according to the coordinates they belong to
        
        GL.glEnd()
        GL.glFlush()

