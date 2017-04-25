#!/usr/bin/env python

from .GeneralObject import *
import math

class QuadraticBezier(GeneralObject):
    def __init__(self):
        super(QuadraticBezier,self).__init__()
        self.controlPoints=[]
        self.p0 = 0
        self.p1 = 0
        self.p2 = 0

    def __str__(self):
    	return 'p0 = %s, p1= %s, p2= %s' %(self.p0 ,self.p1, self.p2)

    def compute(self, p0, p1 , p2):
        self.controlPoints=[]
        self.points = []
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.controlPoints.append(self.p0)
        self.controlPoints.append(self.p1)
        self.controlPoints.append(self.p2)
        t = 0.0
        while t <= 1:
            t2 = t * t
            oneMinusT = (1.0 - t)
            ptx = oneMinusT * oneMinusT * p0.x + 2 * oneMinusT * t * p1.x + t2 * p2.x
            pty = oneMinusT * oneMinusT * p0.y + 2 * oneMinusT * t * p1.y + t2 * p2.y
            point = Point(ptx, pty, 1)
            self.points.append(point)
            t += 0.05


class CubicBezier(GeneralObject):
    def __init__(self):
        super(CubicBezier,self).__init__()
        self.controlPoints=[]
        self.p0 = 0
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0

    def __str__(self):
        return 'p0 = %s, p1= %s , p2= %s, p3= %s' %(self.p0 ,self.p1, self.p2 , self.p3)

    def compute(self, p0, p1, p2, p3):
        '''B(t) = (1 - t)* Bp(0 ... n-1) + t * Bp(1 ... n)'''
        # HermiteCurve function where: mn = (pn+1 - pn-1)/(tn+1 - tn-1))
        self.controlPoints=[]
        self.points = []
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.controlPoints.append(self.p0)
        self.controlPoints.append(self.p1)
        self.controlPoints.append(self.p2)
        self.controlPoints.append(self.p3)
        t = 0.0
        while t <= 1:
            t3 = t * t * t
            t2 = t * t
            oneMinusT = (1.0 - t)
            ptx = oneMinusT * oneMinusT * oneMinusT * p0.x + 3 * oneMinusT * oneMinusT * t * p1.x + 3 * oneMinusT * t2 * p2.x + t3 * p3.x
            pty = oneMinusT * oneMinusT * oneMinusT * p0.y + 3 * oneMinusT * oneMinusT * t * p1.y + 3 * oneMinusT * t2 * p2.y + t3 * p3.y
            point = Point(ptx, pty, 1)
            self.points.append(point)
            t += 0.05

class Bezier(GeneralObject):
    def __init__(self):
        super(Bezier,self).__init__()
        self.controlPoints=[]

    def compute(self, controlPoints):
        '''B(t) = (1 - t)* Bp(0 ... n-1) + t * Bp(1 ... n)'''
        # HermiteCurve function where: mn = (pn+1 - pn-1)/(tn+1 - tn-1))
        self.controlPoints=[]
        self.controlPoints = controlPoints
        self.points = []
        n = len(self.controlPoints)
        cofactors = binomialCoefficient(n-1)

        t = 0.0
        while t <= 1:
            ptx = 0
            pty = 0
            oneMinusT = (1.0 - t)

            i = 0
            while i < n:
                ptx += cofactors[-n + i] * math.pow(oneMinusT,n-1-i) * math.pow(t,i) * self.controlPoints[-n +i].x
                pty += cofactors[-n + i] * math.pow(oneMinusT,n-1-i) * math.pow(t,i) * self.controlPoints[-n +i].y
                i += 1

            point = Point(ptx, pty, 1)
            self.points.append(point)
            t += 0.05


def binomialCoefficient(k):
    li = [0 for x in range(0,k+1)]
    li[0] = 1
    for i in range(1, k+1):
        for j in range(i,0 , -1):
            li[j] = li[j] + li[j-1]
    return li

