#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

'''----------------------------------------------------------------------------
     Global Variables
----------------------------------------------------------------------------'''
#(x0,y0), (x1,y1)
initialX = initialY= terminalX = terminalY = 0
#square model
linePoints=[]
#number of clicks
numberOfClicks = 0

#view dimentions
width = 500
height = 600

#coordinates of the view for gluOrtho2D
viewCoordinates = [0, width, 0 ,height]

'''----------------------------------------------------------------------------
viewSetting:
    settings for display
     params: none
     return: none
----------------------------------------------------------------------------'''
def viewSetting():
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D( viewCoordinates[0],
                viewCoordinates[1],
                viewCoordinates[2],
                viewCoordinates[3]
                )

'''----------------------------------------------------------------------------
drawLine:
    draws pixel for a line
     params: none
     return: none
----------------------------------------------------------------------------'''
def drawLine():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    for point in linePoints:
        glVertex2fv(point)  #map points according to the coordinates they belong to
    glEnd()
    glFlush()

'''----------------------------------------------------------------------------
bresenhamAlg:
    Calculates the points for a line on a grid according to
    Bresenham's Algorithm
     params:
        initialX = x0, initial x coordinate of the line
        initialY = y0, initial y coordinate of the line
        terminalX = x1, final  x coordinate of the line
        terminalY = y1, final  y coordinate of the line

     return: none
----------------------------------------------------------------------------'''
def bresenhamAlg(initialX,initialY,terminalX,terminalY):
    xstep = 1
    ystep = 1

    #Calculate dx and dy
    dx = abs(terminalX - initialX)
    dy = abs(terminalY - initialY)

    # X as the driving axis
    if dx >= dy:
        E = 2* dy - dx

        # swap points if x0 > x1
        if initialX > terminalX :
            initialX,terminalX = terminalX, initialX
            initialY,terminalY = terminalY, initialY

        # to support 4nd and 8th octant
        if initialY > terminalY :
            ystep = ystep * -1

        for i in range(initialX, terminalX, xstep):
            linePoints.append((initialX,initialY))
            if E >= 0:
                initialY = initialY + ystep
                E = E - 2*dx
            E = E + 2* dy
            initialX = initialX + xstep

    # Y as the driving axis
    else:
        E = 2* dx - dy
        # swap points if y0 > y1
        if initialY > terminalY :
            initialX,terminalX = terminalX, initialX
            initialY,terminalY = terminalY, initialY

        # to support 3nd and 7th octant
        if initialX > terminalX :
            xstep = xstep * -1

        for i in range(initialY, terminalY, ystep):
            linePoints.append((initialX,initialY))
            if E >= 0:
                initialX = initialX + xstep
                E = E - 2* dy
            E = E + 2 * dx
            initialY = initialY + ystep


'''----------------------------------------------------------------------------
mouse:
    callback to listen mouse clicks
     params:
        button = checks for b
        state = check the type of event emited by button
        x = x coordinate based on cursor position on window
        y = y coordinate based on cursor position on window

     return: none
----------------------------------------------------------------------------'''
def mouse( button,  state,  x, y):
    global linePoints
    global numberOfClicks
    global initialX
    global initialY
    global terminalX
    global terminalY

    linePoints = []
    #check for left click on relese
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        #print numberOfClicks
        if numberOfClicks == 0:
            initialX = x
            initialY = height - y
            numberOfClicks = 1 + numberOfClicks
        else :
            terminalX = x
            terminalY = height - y
            #print initialX,initialY,terminalX,terminalY
            bresenhamAlg(initialX, initialY, terminalX, terminalY)
            drawLine()
            print ( linePoints)
            numberOfClicks = 0
'''----------------------------------------------------------------------------
display:
    display seetings for line
     params: none
     return: none
----------------------------------------------------------------------------'''
def display():
    glClearColor(0.0,0.0,0.0,0.0)
    glColor3f(255, 255, 255)
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

'''----------------------------------------------------------------------------
main:
    open GL configuration
     params: none
     return: none
----------------------------------------------------------------------------'''
def main():
    glutInit()
    glutInitWindowSize(width,height)
    glutCreateWindow("Integer Bresenham Algorithm")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    viewSetting()
    glutMouseFunc(mouse)
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == '__main__':
    main()
