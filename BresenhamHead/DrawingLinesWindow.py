#!/usr/bin/env python

'''
DrawingLinesWindow
----------
**DrawingLinesWindow*** creates a GLStandardDrawingWindow from QGLWidget.
Used to make a window that allows the user to draw lines with two clicks,
which specify the first and last points of the lines.

Implements mousePressEvent

attributes
----------
    *colorCounter to decide the color of the lines.
'''

from Line import Line
from GLStandardDrawingWindow import *
from PyQt5.QtCore import QSize,QTimer

class DrawingLinesWindow(GLStandardDrawingWindow):
    def __init__(self):
        super().__init__()
        self.colorCounter = 1
        # work that file out
        self.timer2 = QTimer(self)
        self.timer2.start(100)
        self.timer2.timeout.connect(self.update)
        global  vertices
        vertices=[]
        facesList = []
        global faces
        faces=[]
        file = open("head.txt","r")
        data = file.readlines()
        file.close()
        for txtLine in data:
            vertices.append(txtLine.split())
        

        file = open("faces.txt","r")
        data = file.readlines()
        file.close()
        for txtLine in data:
            facesList.append(txtLine.split())
        
        for face in facesList:
            if face[0] == "f":
                splitFaceOne = face[1].split("/")
                splitFaceTwo = face[2].split("/")
                splitFaceThree = face[3].split("/")
                faces.append(int(splitFaceOne[0]) -1 )
                faces.append(int(splitFaceTwo[0]) -1)
                # faces.append(int(splitFaceTwo[0]) -1)
                # faces.append(int(splitFaceThree[0]) -1) 
                # faces.append(int(splitFaceThree[0]) -1) 
                # faces.append(int(splitFaceOne[0]) -1) 
        
        # lets plot that face
        # for i in range(0,9890):
        for i in range(0,len(faces)-3):
            # x0 = (float(vertices[faces[i]][1]) + 1 )
            # y0 = (float(vertices[faces[i]][2]) + 1 ) 
            # # print(i ,faces[i ],  vertices[ faces[i ] ], vertices[ faces[i + 1] ], len(faces))
            # x1 = (float(vertices[ faces[i + 1] ][1]) + 1 )
            # y1 = (float(vertices[ faces[i + 1] ][2]) + 1) 
            # # print(float(vertices[faces[i]][3]))
            if float(vertices[faces[i]][3]) > -0.20:
                x0 = (float(vertices[faces[i]][1]) + 1) * self.width /6 + 100
                y0 = (float(vertices[faces[i]][2]) + 1 ) * self.height /6 + 100
                # print(i ,faces[i ],  vertices[ faces[i ] ], vertices[ faces[i + 1] ], len(faces))
                x1 = (float(vertices[ faces[i + 1] ][1]) + 1) * self.width /6 + 100
                y1 = (float(vertices[ faces[i + 1] ][2]) + 1) * self.height /6 + 100
                self.history.append(Line(x0,y0,x1,y1))

    def paintGL(self):
        '''
        paintGL
        draws whatever is on the history stack as a set of points
        '''
        # print(self.timer.elapsed())
        # GL.glRotatef(float(self.timer.elapsed())* 50.0, 0.0, 0.0, 1.0)
        # GL.glRotatef(float(self.timer.elapsed())* 10.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        if len(self.history) > 0:
            for line in self.history:
                self.drawLine(line)
            GL.glFlush()
            GL.glFinish()

    def drawLine(self, line):
        GL.glColor3f(1,1,1)
        GL.glPointSize(0.1)
        GL.glBegin(GL.GL_POINTS)
        for point in line.points:
            GL.glVertex3fv(point)  #map points according to the coordinates they belong to
        GL.glEnd()
