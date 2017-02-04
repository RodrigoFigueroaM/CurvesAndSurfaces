#!/usr/bin/env python

class Ellipse(object):
    '''
    __init__
        Creates ellipse object, it requires 4 parameters
        cx, cy, a ,b
    '''
    def __init__(self, *argv):
        super(Ellipse, self ).__init__()
        self.cx, self.cy, self.a, self.b = argv
        self.cx = int(self.cx)
        self.cy = int(self.cy)
        self.a = int(self.a)
        self.b = int(self.b)
        self.points=[]
        self.color = [1, 1, 1]

        self.bresenhamAlg()

    def __str__(self):
        return 'ellipse= %s' %(self.points)

    def __del__(self):
        print ("Ellipse destroyed")

    def update(self):
        self.points=[]
        self.bresenhamAlg()

    '''----------------------------------------------------------------------------
    bresenhamAlg:
        Calculates the points for a Ellipse on a grid according to
        Midpoint  Algorithm
         params: none
         return: none
    ----------------------------------------------------------------------------'''
    def bresenhamAlg(self):
        #region 1 from y axis to x axis (clockwise)
        x = 0
        y = self.b

        E = 2 * (self.b * self.b) + (self.a * self.a) * (1 - 2 * self.b)
        while ( (self.b * self.b) * x ) < (self.a * self.a * y):
            self.__addPoint(x, y, self.cx, self.cy)
            if E >= 0:
                E = E + 4 * (self.a * self.a) * (1 - y)
                y = y - 1
     
            E = E + (self.b * self.b) * (4 * x + 6)
            x = x + 1
        x = self.a
        y = 0

        E = 2 * (self.a * self.a) + (self.b * self.b) * (1 - 2 * self.a)
       
        #region 2 from y axis to x axis(clockwise when slope == 1)
        while ((self.a * self.a) * y) < ((self.b * self.b) * x):
            self.__addPoint(x, y, self.cx, self.cy)
            if E >= 0:
                E = E + 4 * (self.b * self.b) * (1 - x)
                x = x - 1 
            
            E = E + (self.a * self.a) * ( 4 * y + 6 )
            y = y + 1

 
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
    def __addPoint(self, x, y,cx, cy):
        self.points.append( (cx + x, cy + y) )
        self.points.append( (cx - x, cy + y) )
        self.points.append( (cx + x, cy - y) )
        self.points.append( (cx - x, cy - y) )
       



'''----------------------------------------------------------------------------
distance:
    calculates the distance between two points in one dimension
    params: p0, p1

    return: Integer distance
----------------------------------------------------------------------------'''
def distance(p0, p1):
    distance = (p1 - p0)
    return int (abs(distance) )
