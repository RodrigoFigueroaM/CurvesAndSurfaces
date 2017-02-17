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
        undoButton = QPushButton("Delete Last")
        undoButton.setMaximumWidth(100)
        undoButton.clicked.connect(self.pressed)
        buttonsLayout.addWidget(undoButton)

        vbox = QHBoxLayout()
        vbox.addLayout(mainLayout)
        vbox.addLayout(buttonsLayout)

        self.setLayout(vbox)
        self.resize(500, 600)
        self.setWindowTitle("Hermite Curve")

    def pressed(self):
        if len(self.drawingWindow.history) > 0 :
            self.drawingWindow.history.pop()
            for i in range (0,4):
                self.drawingWindow.vectorsPoints.pop()
                self.drawingWindow.points.pop()
            self.drawingWindow.updateGL()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
