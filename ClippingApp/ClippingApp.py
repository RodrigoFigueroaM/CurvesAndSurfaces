#!/usr/bin/env python

'''
A program that clips the most recent rectangle an ellipse drawn on screen 
used  PyQt5 and PyOpenGL
'''
import sys
import math

from Line import Line

from GeneralObject import GeneralObject
from operator import itemgetter,attrgetter
from DrawingWindow import *
from GeneralObject import *
from PyQt5.QtWidgets import  QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox

class IntersectionType(object):
    """docstring for IntersectionType."""
    def __init__(self, *argv):
        super(IntersectionType, self).__init__()
        self.angle, self.type = argv

    def __str__(self):
        return "%s, %s" %(self.angle, self.type)

    def __repr__(self):
        return repr((self.angle, self.type))

class MainWindow(QWidget):
    def __init__(self):
        self.layoutItemsMaxSize=150

        super(MainWindow, self).__init__()

        self.drawingWindow = DrawingWindow()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.drawingWindow)

        buttonsLayout = QVBoxLayout()

        clipButton = QPushButton("Clip")
        clipButton.setMaximumWidth(self.layoutItemsMaxSize)
        clipButton.clicked.connect(self.clipButtonFunction)
        buttonsLayout.addWidget(clipButton)

        undoButton = QPushButton("Remove last object")
        undoButton.setMaximumWidth(self.layoutItemsMaxSize)
        undoButton.clicked.connect(self.removeLastObject)
        buttonsLayout.addWidget(undoButton)


        self.shapesMenu = QComboBox()
        self.shapesMenu.setMaximumWidth(self.layoutItemsMaxSize)
        self.shapesMenu.addItem("Rectangle")
        self.shapesMenu.addItem("Ellipse")
        self.drawingWindow.setObjectType(self.shapesMenu.currentText())
        self.shapesMenu.activated.connect(self.chooseItem)
        buttonsLayout.addWidget(self.shapesMenu)

        vbox = QHBoxLayout()
        vbox.addLayout(mainLayout)
        vbox.addLayout(buttonsLayout)

        self.setLayout(vbox)
        self.resize(500, 600)
        self.setWindowTitle("Clipping App")

    def clipButtonFunction(self):
        '''
        Clipping approach
            gets the most recent drawn ellipse
            and clips it to the most recent drawn rectangle
        '''
        clippinRectangle = None
        ellipseToClip = None
        leftBound = rightBound = topBound = lowBound = 0

        clipEdges=[]

        # Get newest drawn Rectangle and Ellipse
        for element in self.drawingWindow.history:
            if type(element) is type(REC):
                clippinRectangle = element

            if type(element) is type(ELLI):
                ellipseToClip = element



        if clippinRectangle and ellipseToClip:
            self.drawingWindow.updateGL()

            leftBound = clippinRectangle.x0
            topBound = clippinRectangle.y0
            rightBound = clippinRectangle.x1
            lowBound = clippinRectangle.y1

            if leftBound > rightBound:
                leftBound, rightBound = rightBound, leftBound
            if lowBound > topBound:
                topBound, lowBound = lowBound, topBound

            clipEdges.append( leftBound)
            clipEdges.append( topBound )
            clipEdges.append( rightBound )
            clipEdges.append( lowBound )
            clippedObject = GeneralObject()

            inputList = ellipseToClip.points
            outputList = []

            if not clippedObject.points:
                inputList = ellipseToClip.points
                outputList = []
            else:
                inputList = clippedObject.points
                outputList = []

            #LEFT
            #outside
            if ellipseToClip.cx - ellipseToClip.a < leftBound:
                p1 = p2 = 0
                for point in inputList:
                    if point[0] >= leftBound:
                        outputList.append(point)
                        """find interception"""
                    if point[0] == leftBound:
                        if p1 == 0:
                            p1 = point[1]
                        elif p2 == 0:
                            p2 = point[1]

                leftBoundLine = Line(leftBound,p1,leftBound, p2)

                for point in leftBoundLine.points:
                    outputList.append(point)

                clippedObject.points = outputList

            if not clippedObject.points:
                inputList = ellipseToClip.points
                outputList = []
            else:
                inputList = clippedObject.points
                outputList = []


            #Top
            #outside
            if ellipseToClip.cy + ellipseToClip.b > topBound:
                p1 = p2 = 0
                """find interception"""
                for point in inputList:
                    if point[1] <= topBound:
                        outputList.append(point)
                    if point[1] == topBound:
                        if p1 == 0:
                            p1 = point[0]
                        elif p2 == 0:
                            p2 = point[0]

                topBoundLine = Line(p1,topBound,p2, topBound)
                for point in topBoundLine.points:
                    outputList.append(point)

                clippedObject.points = outputList

            if not clippedObject.points:
                inputList = ellipseToClip.points
                outputList = []
            else:
                inputList = clippedObject.points
                outputList = []


            #RIGHT
            #outside
            if ellipseToClip.cx + ellipseToClip.a > rightBound:
                p1 = p2 = 0

                for point in inputList:
                    if point[0] <= rightBound:
                        outputList.append(point)
                    """find interception"""
                    if point[0] == rightBound:
                        if p1 == 0:
                            p1 = point[1]
                        elif p2 == 0:
                            p2 = point[1]

                rightBoundLine = Line(rightBound,p1,rightBound, p2)
                for point in rightBoundLine.points:
                    outputList.append(point)
                clippedObject.points = outputList


            if not clippedObject.points:
                inputList = ellipseToClip.points
                outputList = []
            else:
                inputList = clippedObject.points
                outputList = []

            #Low
            #outside
            if ellipseToClip.cy - ellipseToClip.b < lowBound :
                p1 = p2 = 0
                """find interception"""
                for point in inputList:
                    if point[1] >= lowBound:
                        outputList.append(point)

                    if point[1] == lowBound:
                        if p1 == 0:
                            p1 = point[0]
                        elif p2 == 0:
                            p2 = point[0]

                lowBoundLine = Line(p1,lowBound,p2, lowBound)

                for point in lowBoundLine.points:
                    outputList.append(point)

                clippedObject.points = outputList

            if not clippedObject.points:
                clippedObject.points = ellipseToClip.points

            self.drawingWindow.history.remove(ellipseToClip)
            self.drawingWindow.history.remove(clippinRectangle)

            self.drawingWindow.object = clippedObject
            self.drawingWindow.history.append(clippedObject)
            self.drawingWindow.updateGL()



    def removeLastObject(self):
        self.drawingWindow.object = []
        if len(self.drawingWindow.history) > 0 :
            self.drawingWindow.history.pop()
            self.drawingWindow.updateGL()


    def chooseItem(self):
        self.drawingWindow.setObjectType(self.shapesMenu.currentText())




def ComputeIntersection(S,point,edge):
    while point[0] < S[0] and point[1] < S[1] :
        if point == edge:
            return point
        else:
            return(0,0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
