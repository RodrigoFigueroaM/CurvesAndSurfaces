#!/usr/bin/env python

from Point import Point
from GeneralObject import GeneralObject
from Bezier import QuadraticBezier
import math


class Bspline(GeneralObject):
    def __init__(self):
        super(Bspline,self).__init__()
        self.controlPoints=[]
        k = 5
        degree = 2
        i = 2
        t = 2
        coeff = 3
        # knots = [x for x in range(degree + k + 1 )]
        # self.controlPoints = self.__coxDeBoor( degree, coeff, knots, i, k-1, t)
        self.compute()
        # self.points.append(Point(0,0,1))
        # self.points.append(Point(60,0,1))
    def __str__(self):
        return 'p = %s' %(self.points)

    # def calculteKnotVector(self):
    #     return l

    def compute(self):
        coeff = [Point(0,0,1),Point(10,10,1),Point(20,20,1),Point(30,30,1),Point(40,20,1),Point(50,10,1),Point(60,0,1)]
        degree = 2
        U = [Point(0,0,1),Point(10,10,1),Point(20,20,1),Point(30,30,1),Point(40,20,1),Point(50,10,1),Point(60,0,1) ]
        i = 4
        p = degree #degree
        knots = [0,1,2,3,4,5,6,7,8]
        for u in U:
            x = self.__coxDeBoor(coeff,knots,u,i,p)
            self.points.append(x)

    def __coxDeBoor(self,coeff,knots,u,i, p):
        if p == 0 :
            return coeff[i]
        else:
            bottomA = (knots[i+p] - knots[i])
            bottomB = (knots[i + p + 1] - knots[i + 1])
            if bottomA  == 0: 
                return 1
            if bottomB == 0:
                return 1
            left = (u - knots[i])/bottomA
            right = ( (u * -1) + knots[i + p + 1])/bottomB
            # print("N(",u,")","i=",i,"p=",p, ">>>",left,"* N(",u,")","i=",i,"p=",p-1,"+", right,"*N(",u,")","i=",i+1,"p=",p-1)
            return left * self.__coxDeBoor(coeff,knots,u,i, p-1) + right * self.__coxDeBoor(coeff,knots,u,i+1, p - 1)