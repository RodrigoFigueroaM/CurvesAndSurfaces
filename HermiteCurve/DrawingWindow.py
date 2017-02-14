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
from Helper import distance
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
        '''testing/ debug'''
        # self.points.append ( Point(140,150, 1))

        # a = self.points[-1]
        # b = Point(80,100, 1)
        # m0 = Vector (a,b)

        # self.points.append(b)

        # self.vectors.append(m0)
        # self.vectorsPoints.append( (m0.pointOne.data()) )
        # self.vectorsPoints.append( (m0.pointTwo.data()) )

        # print(m0.slope())

        # self.points.append ( Point(200,100, 1))

        # c = self.points[-1]
        # d = Point(220,120, 1)
        # m1 = Vector (c,d)

        # self.points.append(d)

        # self.vectors.append(m1)
        # self.vectorsPoints.append( (m1.pointOne.data()) )
        # self.vectorsPoints.append( (m1.pointTwo.data()) )

        # print(m1.slope())

        # v0 = self.vectors[-2]
        # v1 = self.vectors[-1] 

        # if v0.pointOne.x > v1.pointOne.x:
        #     v0 , v1 = v1 , v0

        # hermiteCurve = HermiteCurve()
        # ytrans = 0 # used to modify transalation. if p0 > p1 (1,0) translate y coordinate to that point 
        
        # if v0.pointOne.y > v1.pointOne.y:
        #     hermiteCurve.compute(1, v0.slope(), 0, v1.slope())
        #     ytrans = distance(v1.pointOne.y, v0.pointOne.y)

        # elif v0.pointOne.y < v1.pointOne.y:
        #     hermiteCurve.compute(0, v0.slope(), 1, v1.slope())

        # elif v0.pointOne.y == v1.pointOne.y:
        #     hermiteCurve.compute(0, v0.slope(), 0, v1.slope())

        # hermiteCurve.scale(distance(v1.pointOne.x, v0.pointOne.x), distance(v1.pointOne.y, v0.pointOne.y))
        # hermiteCurve.translate(v0.pointOne.x, v0.pointOne.y  - ytrans)

        # self.history.append(hermiteCurve)

       
        '''NOTE: no testing'''
        bounds = 5
        i = 0
        for point in self.points:   
            # print("point" , point)
            #mouse bounds. Raise flag because space is taken 

            if ( point.x > event.x() - bounds and point.x <  event.x() + bounds 
                and  point.y <  self.height - event.y() +  bounds and  point.y > self.height - event.y()  - bounds ): 
                self.busyPixel = True
                self.selectedPoint = point
                self.selectedPointIndex = i 
                self.lastMousePosition = event.pos()
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

                if v0.pointOne.x > v1.pointOne.x:
                    v0 , v1 = v1 , v0

                hermiteCurve = HermiteCurve()
                ytrans = 0 # used to modify transalation. if p0 > p1 (1,0) translate y coordinate to that point 
                
                if v0.pointOne.y > v1.pointOne.y:
                    hermiteCurve.compute(1, v0.slope(), 0, v1.slope())
                    ytrans = distance(v1.pointOne.y,v0.pointOne.y)

                elif v0.pointOne.y < v1.pointOne.y:
                    hermiteCurve.compute(0, v0.slope(), 1, v1.slope())

                elif v0.pointOne.y == v1.pointOne.y:
                    hermiteCurve.compute(0, v0.slope(), 0, v1.slope())

                hermiteCurve.scale(distance(v1.pointOne.x, v0.pointOne.x), distance(v1.pointOne.y, v0.pointOne.y))
                hermiteCurve.translate(v0.pointOne.x, v0.pointOne.y  - ytrans)
                print("init")
                print(v0, v1)   
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

                if self.selectedPoint == v1.pointOne or self.selectedPoint == v1.pointTwo:
                    rotationPoint = v1.pointOne

                if v0.pointOne.x > v1.pointOne.x:
                    v0 , v1 = v1 , v0

                distanceX = distance(self.selectedPoint.x, event.x())
                distanceY =  distance(self.selectedPoint.y, self.height - event.y())

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
                   
                print("ROTATING ON :", rotationPoint.x, rotationPoint.y,  v0.slope(), v1.slope())
                # ??????????????????????
                # distanceX = distance(self.selectedPoint.x, event.x())
                # distanceY =  distance(self.selectedPoint.y, self.height - event.y())
                # # left
                # if self.lastMousePosition.x() > event.x():
                #     self.selectedPoint.translate(-1 * distanceX * mousedx, distanceY * mousedy, 0)
                    
               
                # # right
                # if self.lastMousePosition.x() < event.x():
                #     self.selectedPoint.translate(distanceX * mousedx, distanceY * mousedy, 0)
                   
                # # up
                # if self.lastMousePosition.y() < event.y():
                #     # hermiteCurve.scale(abs(v1.pointOne.x - v0.pointOne.x), abs(v1.pointOne.y - v0.pointOne.y) )
                #     self.selectedPoint.translate(distanceX * mousedx,  -1 * distanceY * mousedy, 0)
               
                # if self.lastMousePosition.y() > event.y():
                #     self.selectedPoint.translate(distanceX * mousedx, distanceY * mousedy, 0)

                self.vectorsPoints[self.selectedPointIndex] = self.selectedPoint.data()
                self.updateGL()
       
    def mouseReleaseEvent(self, event):
        self.busyPixel = False
        self.updateGL()
    
    def keyPressEvent(self, event):
        hermiteCurve = self.history[-1]
        v0 = self.vectors[-2]
        v1 = self.vectors[-1]
        ytrans = 0
        
        print ( "CURVE",hermiteCurve)
        if v0.pointOne.x > v1.pointOne.x:
            v0 , v1 = v1 , v0
        # Update curve
        ytrans = 0 # used to modify transalation. if p0 > p1 (1,0) translate y coordinate to that point 
        
        if v0.pointOne.y > v1.pointOne.y:
            hermiteCurve.compute(1, v0.slope(), 0, v1.slope())
            ytrans = distance(v1.pointOne.y,v0.pointOne.y)

        elif v0.pointOne.y < v1.pointOne.y:
            hermiteCurve.compute(0, v0.slope(), 1, v1.slope())

        elif v0.pointOne.y == v1.pointOne.y:
            hermiteCurve.compute(0, v0.slope(), 0, v1.slope())

        hermiteCurve.scale(distance(v1.pointOne.x, v0.pointOne.x), distance(v1.pointOne.y, v0.pointOne.y))
        hermiteCurve.translate(v0.pointOne.x, v0.pointOne.y  - ytrans)
        self.updateGL()




    #     self.updateGL()   
    #     origin = Vector(Point(0,0,1),Point(0,0,1))
    #     self.update+=1
    #     v0 = self.vectors[-2]
    #     v1 = self.vectors[-1] 
    #     hermiteCurve = self.history.pop()
    #     hermiteCurve.compute(0, 0, 1, 0)
    #     angleA = v0.angle(v1)
    #     angleB = v1.angle(origin)
    #     print("ANGLE: ", angleB, angleA) 
    #     hermiteCurve.translate(-1 * v0.pointOne.x, -1 * v0.pointOne.y)
    #     hermiteCurve.rotate(angleA)
    #     # hermiteCurve.scale(abs(v1.pointOne.x - v0.pointOne.x), abs(v1.pointOne.y - v0.pointOne.y) )
    #     hermiteCurve.translate(v0.pointOne.x, v0.pointOne.y)
    #     # print(hermiteCurve.points)
    #     print("HEHEEE") 
    #     self.history.append(hermiteCurve)
    #     self.updateGL()
    #     print("Asd",self.update)
        
   
    def paintGL(self):
        '''
        paintGL
        Updates the current object that is being drawn in screen.
        Draws whatever is on the history stack as a set of points
        '''
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        # Draw vectors
        GL.glColor3f(.48, .80, .81)
        GL.glPointSize(10.0)
        GL.glBegin(GL.GL_POINTS)
        for point in self.vectorsPoints:
            GL.glVertex3fv(point)
        GL.glEnd()


        # Draw Curves
        GL.glColor3f(.85, .30, .90)
        GL.glPointSize(2.0)
        GL.glBegin(GL.GL_POINTS)
        # if self.object:
        #     for point in self.object.points:
        #         GL.glVertex2fv(point)
        for element in self.history:
            for point in element.points:
                GL.glVertex3fv(point)  #  #map points according to the coordinates they belong to
        GL.glEnd()
        GL.glFlush()

