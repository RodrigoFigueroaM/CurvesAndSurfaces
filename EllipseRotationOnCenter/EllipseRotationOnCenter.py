#!/usr/bin/env python

'''
A program that display animation of an ellipse rotation around it's center.
used  PyQt5 and PyOpenGL
'''
import sys
import math

from PyQt5.QtCore import Qt , QTimer, pyqtSlot

from DrawingWindow import *

from PyQt5.QtWidgets import  QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QSlider

class MainWindow(QWidget):
    def __init__(self):
        self.layoutItemsMaxSize = 150
        self.thetaValue = 0

        super(MainWindow, self).__init__()
        self.drawingWindow = DrawingWindow()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.drawingWindow)

        vbox = QHBoxLayout()
        vbox.addLayout(mainLayout)

        timer = QTimer(self)
        timer.setInterval(100)
        timer.timeout.connect(self.timerFuntion)
        timer.start()

        self.setLayout(vbox)
        self.resize(500, 600)
        self.setWindowTitle("Rotation App")

    @pyqtSlot()
    def timerFuntion(self):
        self.thetaValue = (self.thetaValue + 1) % 2* math.pi / 100
        self.drawingWindow.rotateEllipse(self.thetaValue )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
