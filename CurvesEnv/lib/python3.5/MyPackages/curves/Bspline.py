#!/usr/bin/env python

from .GeneralObject import *
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
            self.knotVectorType = "periodic uniform"
        else:
            self.knotVectorType = knotVectorType.lower()
        self.rec = 0
    
    def __str__(self):
        return 'p = %s' %(self.points)
    
    def compute(self, controlPoints = None, degree = 0, knotVectorType = None ):
        if not knotVectorType :
            self.knotVectorType = "periodic uniform"
        else:
            self.knotVectorType = knotVectorType.lower()
        
        self.controlPoints = []
        self.points = []
        self.controlPoints = controlPoints
        self.degree = degree
      
        if self.degree == 0 or self.degree  >= len(self.controlPoints):
            self.degree = len(self.controlPoints) - 1

        self.knots = self.__computeKnotVector( degree = self.degree , knotVectorType = knotVectorType)

        p = self.degree

        u = self.knots[self.degree]
        stopU = self.knots[len(self.knots) - self.degree - 1]
        while u <= stopU:
            i = checkU(u,self.knots)
            #x = self.__coxDeBoor(self.degree,self.controlPoints,self.knots,u,i,p)
            x = self.__coxDeBoorWithDictionary(degree = self.degree, knots = self.knots,u = u,i = i)
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


    def __coxDeBoorWithDictionary(self,degree = None ,knots = None, u = None, i = None):
        '''original CoxDeBoor algorithm computed with a dictionary'''
        top = 1
        bottom = 1
        dictionary = {}
        for x in range (i - degree , i + 1, 1):
            for y in range(0, x + i + degree , 1):

                alphaBottom = (knots[x + degree + 1 - y] - knots[x])
                if alphaBottom == 0:
                    alphaBottom = 1
                alpha =  (u - knots[x])/alphaBottom
                
                top = alpha
                bottom = 1 - top
                
                if y == 0:
                    dictionary[str(x)+','+str(y)+ ',' + str(u)] = self.controlPoints[x]
                
                else:
                    bottomVal = 0
                    if str(x-1)+','+str(y-1) + ',' + str(u) in dictionary:
                        bottomVal = dictionary[str(x-1)+','+str(y-1) + ',' + str(u)]
                    
                    dictionary[str(x)+','+str(y) + ',' + str(u) ] =  dictionary[str(x)+','+str(y-1)+ ',' + str(u)] * top + bottomVal * bottom
    
        return dictionary[str(i)+','+str(degree) + ',' + str(u)]


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
            
            for i in range(len(self.controlPoints) + 2, len(self.controlPoints) + len(knots) ):
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
            
            #elif knotVectorType == "spiral":
            #j = 0
            #for i in range (1,len(self.controlPoints) + degree + 2):
            #   knots.append(j)
            #   if i % 4 == 0:
            #       j += 1
            #return knots


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

def checkU(u = None, knots = None):
    for i in range(1, len(knots)):
        if u >= knots[i] and u < knots[i+1]:
            #            print(knots[i] ,u ,knots[i+1],i)
            return i

