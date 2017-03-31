#!/usr/bin/env python

from Point import Point
from GeneralObject import GeneralObject
import math


class Bspline(GeneralObject):
    def __init__(self):
        super(Bspline,self).__init__()
        self.controlPoints=[]   
        self.__BasisFuntionLookUpTable = { }

        self.rec = 0

    def __str__(self):
        return 'p = %s' %(self.points)

    def compute(self, controlPoints):
        self.controlPoints = []
        self.points = []
        self.controlPoints = controlPoints

        degree = len(self.controlPoints) - 1
        p = degree
        
        knots = self.__computeKnotVector(degree = degree)

        for i in range(degree, degree + 1):
            u = knots[i]
            stopU = u+1 
            while u <= stopU:
                x = self.__coxDeBoor(degree,self.controlPoints,knots,u,i,p)
                self.points.append(x)
                u += 0.05


    def __coxDeBoor(self,degree,controlPoints,knots,u,i, p):
        '''original CoxDeBoor algorithm'''
        if p == 0 :
            return controlPoints[i]
        else:
            bottom = (knots[i + degree + 1 - p] - knots[i])
            if bottom == 0:
                bottom = 1
            alpha =  (u - knots[i])/bottom        
            return self.__coxDeBoor(degree,controlPoints,knots,u,i - 1, p - 1)* (1-alpha) + self.__coxDeBoor(degree, controlPoints,knots,u, i , p - 1) * alpha


    def __computeKnotVector(self, degree = 0 , knotVectorType = None):
        knots = []
        if not knotVectorType :
            return self.__computeKnotVector(degree, "periodic uniform")

        # open uniform      
        if knotVectorType == "open uniform": 
            for i in range (0,degree):
                knots.append(0)

            for i in range(len(knots),len(self.controlPoints) + 1):
                knots.append(i - degree)

            for i in range(len(self.controlPoints) + 2,len(self.controlPoints) + len(knots)):
                knots.append(len(self.controlPoints) - degree + 1)
            return knots
        # uniform sequence
        elif knotVectorType == "periodic uniform":
            knots =[x for x in range(len(self.controlPoints)+ degree + 1)]
            return knots

        elif knotVectorType == "open uniform bezier":
            for i in range (0,len(self.controlPoints)):
                knots.append(0)
            for i in range(len(knots),2 * len(self.controlPoints)):
                knots.append(1)
            return knots

        # nonuniform?
        elif knotVectorType == "nonuniform":
            for i in range (0,degree):
                knots.append(0)

            for i in range(len(knots),len(self.controlPoints) + 1):
                knots.append(degree  - 2)

            for i in range(len(self.controlPoints) + 2,len(self.controlPoints) + len(knots) + 1):
                knots.append(len(self.controlPoints) - degree + 2)
            return knots

        # if knotVectorType == "closed uniform": 
        #     m = len(self.controlPoints) + 1 + degree
        #     knots =[x for x in range((len(self.controlPoints)+ degree)/2 + 1)]
        #     j = 0
        #     for i in range(len(knots),len(self.controlPoints) + 1):
        #         knots.append(knots[i-j])
        #         j += 1

        #     return knots

        else:
            return knots
        

         
