from windowLayout import Ui_MainWindow
from PyQt5.QtCore import Qt , QTimer, pyqtSlot
from DrawingWindow import *
import sys

class MainWindow(Ui_MainWindow):
    """docstring for myWindow."""
    def __init__(self,window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        # self.undoButton.clicked.connect(self.pop)
        self.editCheckBox.stateChanged.connect(self.editState)
        self.ClearButton.clicked.connect(self.clear)
        self.computeButton.clicked.connect(self.openGLWidget.computeSpline)
        # self.popClicks = 0

    def pop(self):
        stack = self.openGLWidget.userDefinedPoints
        if len(stack) > 0:
            stack.pop()
            if len(self.openGLWidget.curvePoints) > 0 :
                self.openGLWidget.curvePoints.pop()
            if len(self.openGLWidget.history) > 0 :
                self.openGLWidget.curvePoints =[]
                self.openGLWidget.history.pop()
        self.openGLWidget.updateGL()

    def clear(self):
        self.openGLWidget.history=[]
        self.openGLWidget.userDefinedPoints =[]
        self.openGLWidget.curvePoints =[]
        self.openGLWidget.updateGL()


    def editState(self,state):
        if state == Qt.Checked:
            self.openGLWidget.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            self.openGLWidget.setEditFlag(True)
        else:
            self.openGLWidget.setEditFlag(False)
        self.openGLWidget.updateGL()
