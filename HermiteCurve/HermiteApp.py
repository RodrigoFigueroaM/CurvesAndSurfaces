#!/usr/bin/env python

'''
A program that allows users to .
used  PyQt5 and PyOpenGL
'''
import sys
import math

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

        '''NOTE: compute button? '''
        
        vbox = QHBoxLayout()
        vbox.addLayout(mainLayout)
        vbox.addLayout(buttonsLayout)

        self.setLayout(vbox)
        self.resize(500, 600)
        self.setWindowTitle("Hermite Curve")
   


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