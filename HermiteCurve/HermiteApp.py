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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
