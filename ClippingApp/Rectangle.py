#!/usr/bin/env python

from Line import Line
import itertools

class Rectangle(object):
    '''
    __init__
        Creates ellipse Rectangle, it requires 4 arguments
        x0, y0, x1 and y1
    '''
    def __init__(self, *argv):
        super(Rectangle, self ).__init__()
        self.x0, self.y0, self.x1, self.y1 = argv
        self.color = [1, 1, 1]
        self.points =[]
        self.topLine = 0
        self.bottomLine = 0
        self.leftLine = 0
        self.rightLine = 0

        self.compute()

    def __str__(self):
        if self.points:
            return 'rectangle= %s ' %(self.points )
        #return 'rectangle= %s , %s ,%s ,%s ' %(self.x0, self.y0, self.length, self.width )

    def __del__(self):
        print ("Rectangle destroyed")

    def compute(self):
        self.topLine = Line(self.x0, self.y1, self.x1, self.y1)
        self.bottomLine = Line(self.x0, self.y0, self.x1, self.y0)
        self.leftLine = Line(self.x0, self.y0, self.x0, self.y1)
        self.rightLine = Line(self.x1, self.y0, self.x1, self.y1)

        self.points.append(self.topLine.points)
        self.points.append(self.bottomLine.points)
        self.points.append(self.leftLine.points)
        self.points.append(self.rightLine.points)

        # Make list 1D
        self.points = list( itertools.chain(*self.points))

    def getLength(self):
        if self.length != 0 :
            self.length = abs(self.x0 - self.x1)
        return self.length

    def getWidth(self):
         if self.width != 0 :
             self.width = abs(self.y0 - self.y1)
         return self.width
