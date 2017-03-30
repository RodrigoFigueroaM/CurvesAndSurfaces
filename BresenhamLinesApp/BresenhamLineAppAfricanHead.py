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

        buttonsLayout = QVBoxLayout()
        undoButton = QPushButton("Undo")
        undoButton.setMaximumWidth(100)
        undoButton.clicked.connect(self.pressed)
        buttonsLayout.addWidget(undoButton)

        vbox = QHBoxLayout()
        vbox.addLayout(mainLayout)
        vbox.addLayout(buttonsLayout)

        self.setLayout(vbox)
        self.resize(500, 600)
        self.setWindowTitle("Bresenham Lines")

    def pressed(self):
        if len(self.drawingWindow.history) > 0 :
            self.drawingWindow.history.pop()
            self.drawingWindow.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
