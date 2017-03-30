#!/usr/bin/env python

from .GeneralObject import *
import math
'''
    NOTE:
    # let user choose the degree of curves
    
'''
class NURBS(GeneralObject):
    def __init__(self,knotVectorType = None):
        super(NURBS,self).__init__()
        self.controlPoints=[]
        self.degree = 0
        self.knots =[] #determined by number of control points + degree + 1
        self.homogenousCoordinates = []
        self.knotVectorType = knotVectorType
        if not knotVectorType :
            self.knotVectorType = "periodic uniform"
        else:
            self.knotVectorType = knotVectorType.lower()
    

    def __str__(self):
        return 'p = %s' %(self.points)

    def compute(self, controlPoints):
        self.controlPoints = []
        self.points = []
        self.controlPoints = controlPoints
        self.degree = 4
        p = self.degree
        
#        pi = math.pi

#        self.knots = [0,0,0,pi/2, pi/2,pi,pi,3*pi/2,3*pi/2,2*pi, 2*pi, 2*pi]
        self.knots = [0,0,0,0,1,2,2,2,2]
#        self.knots = [0,0,0,1,2,3,3,3]#self.__computeKnotVector( degree = self.degree , knotVectorType = self.knotVectorType)
#        self.knots = self.__computeKnotVector( degree = self.degree , knotVectorType = "open uniform")


        self.homogenousCoordinates = [1,1,1,1,1] # attached to each control point
#        sq = math.sqrt(2)/2
#        self.homogenousCoordinates = [1,sq,1,sq,1,sq,1,sq,1]

        #save this left part
#        for i in range(self.degree, self.degree + 1):
#            u = self.knots[i-1]
#            print(i,u)
#            stopU = u + 1
#            while u <= stopU:
#                x = self.__coxDeBoor(self.degree,self.controlPoints,self.knots,u,i,p)
#                y = self.__coxDeBoorY(self.degree,self.controlPoints,self.knots,u,i,p)
#                self.points.append(x/y)
#                u += 0.01
# i = 3 u = 0.... 0.99


        u = self.knots[self.degree ]
        stopU = self.knots[len(self.knots) - self.degree ]
        while u <= stopU:
            i = checkU(u, self.knots)
            x = self.__coxDeBoor(self.degree,self.controlPoints,self.knots,u,i,p)
            y = self.__coxDeBoorY(self.degree,self.controlPoints,self.knots,u,i,p)
            self.points.append(x/y)
            u += 0.01

#        p = self.degree
#        for i in range(self.degree  , self.degree + 1):
#            print(i)
#            u = self.knots[i]
#            stopU = u+1
#            while u < stopU:
#                x = self.__coxDeBoor(self.degree,self.controlPoints,self.knots,u,i,p)
#                y = self.__coxDeBoorY(self.degree,self.controlPoints,self.knots,u,i,p)
#                self.points.append(x/y)
#                u += 0.01

                    
    def __coxDeBoor(self,degree,controlPoints,knots,u,i, p):
        '''original CoxDeBoor algorithm'''
        if p == 0 :
            return controlPoints[i] * self.homogenousCoordinates[i]
        else:
            bottom = (knots[i + degree + 1 - p] - knots[i])
            if bottom == 0:
                bottom = 1
            alpha =  (u - knots[i])/bottom
            return self.__coxDeBoor(degree,controlPoints,knots,u,i - 1, p - 1)* (1-alpha) + self.__coxDeBoor(degree, controlPoints,knots,u, i , p - 1) * alpha

    def __coxDeBoorY(self,degree,controlPoints,knots,u,i, p):
        '''original CoxDeBoor algorithm'''
        if p == 0 :
            return self.homogenousCoordinates[i]
        else:
            bottom = (knots[i + degree + 1 - p] - knots[i])
            if bottom == 0:
                bottom = 1
            alpha =  (u - knots[i])/bottom
            return self.__coxDeBoorY(degree,controlPoints,knots,u,i - 1, p - 1)* (1-alpha) + self.__coxDeBoorY(degree, controlPoints,knots,u, i , p - 1) * alpha


    def __computeKnotVector(self, degree = 0 , knotVectorType = None):
        knots = []

        # open uniform
        if knotVectorType == "open uniform":
            for i in range (0,degree):
                knots.append(0)

            for i in range(len(knots),len(self.controlPoints) + 1):
                knots.append(i - degree + 1)

            for i in range(len(self.controlPoints) + 2,len(self.controlPoints) + len(knots) + 1):
                knots.append(len(self.controlPoints) - degree + 1)
            return knots
        # uniform sequence
        elif knotVectorType == "periodic uniform":
            knots =[x for x in range(len(self.controlPoints) + degree + 1)]
            return knots

        elif knotVectorType == "open uniform bezier":
            for i in range (0,len(self.controlPoints)):
                knots.append(0)
            for i in range(len(knots),2 * len(self.controlPoints)):
                knots.append(1)
            return knots

        elif knotVectorType == "spiral":
            j = 0
            for i in range (1,len(self.controlPoints) + degree + 2):
                knots.append(j)
                if i % 4 == 0:
                    j += 1
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

        else:
            return knots


def checkU(u = None, knots = None):
    for i in range(1, len(knots)):
        if u >= knots[i] and u < knots[i+1]:
#            print(knots[i] ,u ,knots[i+1],i)
            return i
