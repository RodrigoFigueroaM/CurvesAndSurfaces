from windowLayout import Ui_MainWindow
from PyQt5.QtCore import Qt , QTimer, pyqtSlot
from DrawingWindow import *
from Ellipse import Ellipse
import sys

class MainWindow(Ui_MainWindow):
    """docstring for myWindow."""
    def __init__(self,window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.timer = QTimer(self.openGLWidget)
        self.delay = 75
        self.undoButton.clicked.connect(self.pop)
        self.animateButton.clicked.connect(self.animate)
        self.timer.timeout.connect(self.animateCallback)
        self.editCheckBox.stateChanged.connect(self.editState)
        self.index = 0

    def pop(self):
        if self.timer.isActive() == False:
            undoButtonFunction(self.openGLWidget)
            self.openGLWidget.updateGL()


    def animate(self):
        self.index = 0
        catmull = self.openGLWidget.history[0]
        if len(self.openGLWidget.animationObjects) == 1:
            self.openGLWidget.animationObjects.pop()
        ellipse = Ellipse(catmull.userDefinedPoints[1].x, catmull.userDefinedPoints[1].y, 10, 10)
        ellipse.compute()
        self.openGLWidget.animationObjects.append(ellipse)
        self.timer.start(self.delay)

    def animateCallback(self):
         if type(self.openGLWidget.history[0]) == type(CatmullRom()):
            catmull = self.openGLWidget.history[0]
            if len(self.openGLWidget.animationObjects) is not None:
                ellipse = self.openGLWidget.animationObjects[0]
                self.openGLWidget.updateGL()
                if catmull.points[self.index+1] == catmull.points[-1]:
                    self.openGLWidget.animationObjects.pop()
                    self.timer.stop()
                else:
                    ellipse.translate(catmull.points[self.index+1].x - catmull.points[self.index].x ,catmull.points[self.index+1].y - catmull.points[self.index].y )
                    self.index += 1

    def editState(self,state):
        if state == Qt.Checked:
            self.openGLWidget.setEditFlag(True)
        else:
            self.openGLWidget.setEditFlag(False)



'''controller for buttons'''
def undoButtonFunction(element):
    stack = element.userDefinedPoints
    if len(stack) > 0:
        stack.pop()

def animateButtonFunction(element):
        print("animate")


def editCheckBoxFunction():
    print("animate")
    return True
