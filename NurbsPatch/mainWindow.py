#!/usr/bin/env python
# from MyPackages.qtPackage.windowLayoutSpline import Ui_MainWindow
from MyPackages.qtPackage.windowLayout3D import Ui_MainWindow
from PyQt5.QtCore import Qt , QTimer, pyqtSlot
from DrawingWindow import *
import sys

class MainWindow(Ui_MainWindow):
    """docstring for myWindow."""
    def __init__(self,window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        window.setWindowTitle("NURB Surface")
        self.editCheckBox.stateChanged.connect(self.editState)
        self.popClicks = 0

        #raidio buttons
        self.XrotationRadioButton.toggled.connect(lambda:self.openGLWidget.setRotationAxis(axis.x))
        self.YrotationRadioButton.toggled.connect(lambda:self.openGLWidget.setRotationAxis(axis.y))
        self.ZrotationRadioButton.toggled.connect(lambda:self.openGLWidget.setRotationAxis(axis.z))

    def editState(self,state):
        if state == Qt.Checked:
            # self.openGLWidget.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            self.openGLWidget.setEditFlag(True)
        else:
            self.openGLWidget.setEditFlag(False)
        self.openGLWidget.update()
