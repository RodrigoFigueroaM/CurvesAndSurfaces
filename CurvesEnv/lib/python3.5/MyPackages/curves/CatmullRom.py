#!/usr/bin/env python

from .GeneralObject import *

class CatmullRom(GeneralObject):
    def __init__(self):
        super(CatmullRom,self).__init__()
        self.userDefinedPoints=[]

    def __str__(self):
    	return 'p0 = %s, p1= %s, p2 = %s, p3 = %s' %(self.p0 ,self.p1, self.p2, self.p3)

    def compute(self, userDefinedPoints):
        self.points = [] #make sure our points to be ploted is empty
        self.userDefinedPoints = userDefinedPoints
        #we need at least 4 points to define a Catmull-Rom Spline
        if len(userDefinedPoints) >= 4:
            i = 0
            while  i < len(userDefinedPoints) - 3 :
                self.__computeCurve(userDefinedPoints[i], userDefinedPoints[i+1], userDefinedPoints[i+2],userDefinedPoints[i+3])
                i += 1
        else:
            sprint('at least 4 points need to be provided ')

    def __computeCurve(self, p0, p1, p2, p3):
        '''q(t) = 0.5 *( (2 * P1) + (-P0 + P2) * t + (2*P0 - 5*P1 + 4*P2 - P3) * t2 +(-P0 + 3*P1- 3*P2 + P3) * t3)'''
        # HermiteCurve function where: mn = (pn+1 - pn-1)/(tn+1 - tn-1))
        t = 0.0
        while t <= 1:
            t3 = t * t * t
            t2 = t * t
            ptx = 0.5 * ( (2 * p1.x) + (-1 * p0.x + p2.x) * t + (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2 + ( -1 * p0.x + 3 * p1.x - 3 * p2.x + p3.x )* t3 )
            pty = 0.5 * ( (2 * p1.y) + (-1 * p0.y + p2.y) * t + (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2 + ( -1 * p0.y + 3 * p1.y - 3 * p2.y + p3.y )* t3 )
            point = Point(ptx, pty, 1)
            self.points.append( point)
            t += 0.05
