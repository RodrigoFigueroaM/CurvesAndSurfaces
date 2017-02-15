#!/usr/bin/env python

from Point import Point
from GeneralObject import GeneralObject 

class HermiteCurve(GeneralObject):
    def __init__(self, *argv):
        super(HermiteCurve, self).__init__()
        if len(argv) == 4:
            self.p0 ,self.m0, self.p1,self.m1 = argv
        else:
            self.p0 = 0
            self.m0 = 0
            self.p1 = 0
            self.m1 = 0
    
    def __str__(self):
        return 'p0 = %s,m0 = %s, p1 = %s, m1 = %s' %(self.p0 ,self.m0, self.p1, self.m1)

    def compute(self, *argv):
        '''
        curve is always computed fron the origin
        p(t) = (2t^3 - 3t^2 + 1)p0 + (t^3 - 2t^2 + t)m0 + ( -2t^3 + 3t^2)p1 + (t^3 - t^2)m1
        '''
        # m0, m1 tangents at p0 and p1 respectively 
        self.p0, self.m0, self.p1, self.m1 = argv
        self.points = []
        t = 0.0
        while t < 1.0:
            t3 = t * t * t
            t2 = t * t
            pty = (2 * t3 - 3 * t2 + 1) * self.p0.y + (t3 - 2 * t2 + t) * self.m0 + ( -2 * t3 + 3 * t2) * self.p1.y + (t3 - t2) * self.m1
            point = Point(t, pty, 1)
            self.points.append( point.data() )
            t += 0.001 
   

