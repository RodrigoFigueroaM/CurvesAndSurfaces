#!/usr/bin/env python
'''
GLStandardDrawingWindow
----------
**GLStandardDrawingWindow** creates a QGLWidget of my thinking of a
standard window to draw. it handles the minimumSizeHint,sizeHint, initializeGL,
and resizeGLstandard
attributes
----------
        * standard width = 500
        * standard height = 600
        * history a Stack to kep track of the objects drawn on it
        * black background
        * white foreground
'''
import sys
import math

from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtCore import QSize
import OpenGL.GL as GL
import OpenGL.GLU as GLU

class GLStandardDrawingWindow(QGLWidget):
    def __init__(self):
        super().__init__()
        self.width, self.height = 600, 400
        self.resize(self.width, self.height)
        self.move(100, 100)


    def minimumSizeHint(self):
        return QSize(self.width, self.height)

    def sizeHint(self):
        return QSize(self.width, self.height)

    def initializeGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT| GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.1, 0.1, 0.15, 1.0)
        GL.glClearDepth(1.0)
        GL.glColor3f(.58, .90, .41)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.width, 0, self.height)
        GL.glFlush()

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glPointSize(3.0)
        GLU.gluOrtho2D(0, self.width, 0, self.height)
        GL.glMatrixMode(GL.GL_MODELVIEW)
