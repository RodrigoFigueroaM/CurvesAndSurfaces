from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

'''----------------------------------------------------------------------------
     Global Variables
----------------------------------------------------------------------------'''
#(x0,y0), (x1,y1) , and radius
initialX = initialY= terminalX = terminalY = radius = 0

#points model
points=[]

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
plotPoints:
    draws pixel for a circle
     params: none
     return: none
----------------------------------------------------------------------------'''
def plotPoints():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    for point in points:
        glVertex2fv(point)  #map points according to the coordinates they belong to
    glEnd()
    glFlush()

'''----------------------------------------------------------------------------
BresenhamCaller: (used for debuging)
    Called by glutDisplayFunc to call another function.
     return: none
----------------------------------------------------------------------------'''
def BresenhamCaller():
    display()
    computeCircle(250,300,20)
    plotPoints()

'''----------------------------------------------------------------------------
computeCircle:
    Calculates the points for a circle on a grid according to
    Midpoint Circle Algorithm
     params:
        cx: x coordinate for center of the circle
        cy: y coordinate for center of the circle
        r : radius of the circle

     return: none
----------------------------------------------------------------------------'''

def computeCircle(cx,cy,r):
    x = r
    y = 0
    dx = 1 - 2 * r
    dy = 1
    E = 0
    while ( x >= y ):
        addPoint(x , y , cx, cy)
        y = y + 1
        E = E + dy
        dy = dy + 2
        if ( 2 * E + dx >0 ):
            x = x - 1
            E = E + dx
            dx = dx + 2

'''----------------------------------------------------------------------------
addPoint:
    adds point to an array of points depending on their position
     params:
        x : x coordinate from the center of the circle
        y : y coordinate from the center of the circle
        cx: x coordinate for center of the circle
        cy: y coordinate for center of the circle
        r : radius of the circle
     return: none
----------------------------------------------------------------------------'''
def addPoint(x, y,cx, cy):
    points.append( (cx + x ,cy + y) )
    points.append( (cx - x ,cy + y) )
    points.append( (cx + x ,cy - y) )
    points.append( (cx - x ,cy - y) )

    points.append( (cx + y ,cy + x) )
    points.append( (cx - y ,cy + x) )
    points.append( (cx + y ,cy - x) )
    points.append( (cx - y ,cy - x) )

'''----------------------------------------------------------------------------
distance:
    calculates the distance between two points
    params:x1, x2, y1, y2

    return: Integer distance
----------------------------------------------------------------------------'''
def distance(x1, x2, y1, y2):
    distanceX = (x2 - x1) * (x2 - x1)
    distanceY = (y2 - y1) * (y2 - y1)
    return int (math.sqrt(distanceX + distanceY))

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
    global points
    global numberOfClicks
    global initialX
    global initialY
    global terminalX
    global terminalY
    global radius

    points = []
    #check for left click on relese
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:

        if numberOfClicks == 0:
            initialX = x
            initialY = height - y
            numberOfClicks = 1 + numberOfClicks

        else :
            terminalX = x
            terminalY = height - y
            print initialX,initialY,terminalX,terminalY
            radius = distance(initialX, terminalX, initialY, terminalY)
            print "radius : " , radius
            computeCircle(initialX, initialY, radius)
            plotPoints()
            numberOfClicks = 0

'''----------------------------------------------------------------------------
display:
    display seetings for line
     params: none
     return: none
----------------------------------------------------------------------------'''
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glColor3f(255, 255, 255);
    glClear(GL_COLOR_BUFFER_BIT);
    glFlush();

'''----------------------------------------------------------------------------
main:
    open GL configuration
     params: none
     return: none
----------------------------------------------------------------------------'''
def main():
    glutInit()
    glutInitWindowSize(width,height)
    glutCreateWindow("Bresenham's Circle Algorithm")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    viewSetting()
    glutMouseFunc(mouse)
    glutDisplayFunc(display)
    #glutDisplayFunc(BresenhamCaller)
    glutMainLoop()

if __name__ == '__main__':
    main()
