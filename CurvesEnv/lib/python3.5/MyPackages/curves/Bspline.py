#!/usr/bin/env python

from .GeneralObject import GeneralObject
from MyPackages.geometry.Point import Point
import math

class Bspline(GeneralObject):
    def __init__(self,knotVectorType = None):
        super(Bspline,self).__init__()
        self.controlPoints=[]
        self.degree = 0
        self.knots =[]
        self.knotVectorType = knotVectorType
        
        if not knotVectorType :
            self.knotVectorType = "uniform"
        else:
            self.knotVectorType = knotVectorType.lower()
        self.rec = 0
    
    def __str__(self):
        return 'p = %s' %(self.points)
    
    def compute(self, controlPoints = None, degree = 0, knotVectorType = None ):
        if not knotVectorType :
            self.knotVectorType = "uniform"
        else:
            self.knotVectorType = knotVectorType.lower()
        
        self.controlPoints = []
        self.points = []
        self.controlPoints = controlPoints
        self.degree = degree
      
        if self.degree == 0 or self.degree  >= len(self.controlPoints):
            self.degree = len(self.controlPoints) - 1

        self.knots = self.__computeKnotVector( degree = self.degree , knotVectorType = self.knotVectorType, controlPoints = self.controlPoints)

        p = self.degree

        u = self.knots[self.degree]
        stopU = self.knots[len(self.knots) - self.degree - 1]
        while u <= stopU:
            i = checkU(u,self.knots)
            #x = self.__coxDeBoor(self.degree,self.controlPoints,self.knots,u,i,p)
            x = self.__coxDeBoorWithDictionary(degree = self.degree, controlPoints = self.controlPoints, knots = self.knots,u = u,i = i)
            self.points.append(x)
            u += 0.1


    def __coxDeBoor(self,degree = None, controlPoints = None, knots = None, u = None, i = None, p = None):
        '''original CoxDeBoor algorithm'''
        
        if p == 0 :
            key = str(i) + ',' + str(p) + ',' + str(u)
            return controlPoints[i]
        else:
            bottom = (knots[i + degree + 1 - p] - knots[i])
            if bottom == 0:
                bottom = 1
            alpha =  (u - knots[i])/bottom

            
        return self.__coxDeBoor(degree,controlPoints,knots,u,i - 1, p - 1) * (1-alpha)  + self.__coxDeBoor(degree, controlPoints,knots,u, i , p - 1) * alpha


    def __coxDeBoorWithDictionary(self,degree = None , controlPoints = None, knots = None, u = None, i = None):
        '''original CoxDeBoor algorithm computed with a dictionary'''
        top = 1
        bottom = 1
        dictionary = {}
        for x in range (i - degree , i + 1, 1):
            for y in range(0, x + i + degree , 1):
                
                if y == 0:
                    dictionary[str(x)+','+str(y)+ ',' + str(u)] = controlPoints[x]
                
                else:
                    alphaBottom = (knots[x + degree + 1 - y] - knots[x])
                    if alphaBottom == 0:
                        alphaBottom = 1
                    alpha =  (u - knots[x])/alphaBottom
            
                    top = alpha
                    bottom = 1 - top

                    bottomVal = 0
                    if str(x-1)+','+str(y-1) + ',' + str(u) in dictionary:
                        bottomVal = dictionary[str(x-1)+','+str(y-1) + ',' + str(u)]
                    dictionary[str(x)+','+str(y) + ',' + str(u) ] =  dictionary[str(x)+','+str(y-1)+ ',' + str(u)] * top + bottomVal * bottom
    
        return dictionary[str(i)+','+str(degree) + ',' + str(u)]


    def __computeKnotVector(self, degree = 0 , knotVectorType = None, controlPoints = None):
        knots = []
        if not knotVectorType :
            return self.__computeKnotVector(degree, "uniform")
    
        # open uniform
        if knotVectorType == "open uniform":
            for i in range (1,degree + 1):
                knots.append(0)
            
            for i in range(degree + 1,len(controlPoints) + 1):
                knots.append(i - degree)
            
            for i in range(len(controlPoints) + 2, len(controlPoints) + len(knots) + 1):
                knots.append(len(controlPoints) - degree + 1)
            return knots
                
        # uniform sequence
        elif knotVectorType == "uniform":
            knots =[x for x in range(len(controlPoints) + degree + 1)]
            return knots
    
        elif knotVectorType == "bezier":
            for i in range (0,len(controlPoints)):
                knots.append(0)
            for i in range(len(knots),2 * len(controlPoints)):
                knots.append(1)
            return knots
        
        else:
            return knots

def checkU(u = None, knots = None):
    for i in range(1, len(knots)):
        if u >= knots[i] and u < knots[i+1]:
            return i

