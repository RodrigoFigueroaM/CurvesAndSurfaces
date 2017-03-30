#!/usr/bin/env python

'''
A program that allows users to draw lines.
used  PyQt5 and PyOpenGL
'''
import sys
from DrawingLinesWindow import *
from PyQt5.QtWidgets import  QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.drawingWindow = DrawingLinesWindow()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.drawingWindow)

        vbox = QHBoxLayout()
        vbox.addLayout(mainLayout)


        self.setLayout(vbox)
        self.resize(700, 700)
        self.setWindowTitle("Bresenham Lines")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
