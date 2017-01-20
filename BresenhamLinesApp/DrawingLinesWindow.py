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

class DrawingLinesWindow(GLStandardDrawingWindow):
    def __init__(self):
        super().__init__()
        self.colorCounter = 1
    def mousePressEvent(self, event):
        '''
        mousePressEvent
            creates a line with the mouse coordiantes when clicked.
            NOTE: two clicks are needed for a line. First click sets the
            first point of the line. Second click sets the final point pf the line
        '''
        global tempX0, tempY0

        if self.numberOfClicks == 0:
            tempX0 = event.x()
            tempY0 = self.height - event.y()
            self.numberOfClicks = self.numberOfClicks + 1
        elif self.numberOfClicks == 1:
            line = Line(tempX0, tempY0, event.x(), self.height - event.y())
            if self.colorCounter % 2 == 0:
                line.color = (self.colorCounter, 0, 0)
            elif self.colorCounter  % 3 == 0:
                line.color = (0, self.colorCounter, 0)
            else:
                line.color = (0, 0, self.colorCounter)
                self.colorCounter = self.colorCounter % 3

            self.colorCounter = self.colorCounter + 1
            self.history.append(line)
            self.numberOfClicks = 0
        self.update()
