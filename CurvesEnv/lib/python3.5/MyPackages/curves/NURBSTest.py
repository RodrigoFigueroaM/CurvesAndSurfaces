#!/usr/bin/env python

from .GeneralObject import *
import math

class NURBS(GeneralObject):
    def __init__(self,knotVectorType = None):
        super(NURBS,self).__init__()
        self.controlPoints=[]
        self.degree = 0
        self.knots =[] #determined by number of control points + degree + 1
        self.homogenousCoordinates = []
        self.knotVectorType = knotVectorType
    

    def __str__(self):
        return 'p = %s' %(self.points)
    

    def setHomogenousCoordinates(self, homogenousCoordinates = None, controlPoints = None):
        if not homogenousCoordinates:
            self.homogenousCoordinates = [1 for i in range(0,len(controlPoints)) ] # attached to each control point
        else:
            self.homogenousCoordinates = homogenousCoordinates


    def compute(self, controlPoints = None, degree = 0, knotVectorType = None, knotVector = None, homogenousCoordinates = None ):    
        self.points = []
        self.controlPoints = controlPoints
        self.degree = degree
        print(self.degree, degree)
        if self.degree == 0 or self.degree  >= len(self.controlPoints):
            self.degree = len(self.controlPoints) - 1
        print(self.degree)
        if knotVector:
            self.knots = knotVector
        else:
            if not knotVectorType :
                self.knotVectorType = "uniform"
            else:
                self.knotVectorType = knotVectorType.lower()
            self.knots = self.__computeKnotVector( degree = self.degree , knotVectorType = self.knotVectorType, controlPoints = self.controlPoints)
                 
        self.setHomogenousCoordinates(homogenousCoordinates = homogenousCoordinates, controlPoints = self.controlPoints)
        
        u = self.knots[ self.degree  ]
        stopU = self.knots[len(self.knots) - self.degree]
        while u <= stopU:
            i = checkU(u = u, knots = self.knots)
            # x = self.__coxDeBoor(degree = self.degree,controlPoints = self.controlPoints,knots = self.knots, u = u,i = i,p = p, homogenousCoordinates =  self.homogenousCoordinates)
            # y = self.__coxDeBoorHomogenousCoordinates(degree = self.degree,controlPoints = self.controlPoints,knots = self.knots, u = u,i = i,p = p, homogenousCoordinates = self.homogenousCoordinates)
            x = self.__coxDeBoorWithDictionary(degree = self.degree, controlPoints = self.controlPoints, knots = self.knots, u = u, i = i, homogenousCoordinates = self.homogenousCoordinates)
            y = self.__coxDeBoorHomogenousCoordinatesWithDictionary(degree = self.degree, controlPoints = self.controlPoints, knots = self.knots, u = u, i = i, homogenousCoordinates = self.homogenousCoordinates)
            self.points.append(x/y)
            u += 0.1

     

    def __coxDeBoor(self,degree = None, controlPoints = None, knots = None, u = None, i = None, p = None, homogenousCoordinates = None):
        '''original CoxDeBoor algorithm return the value at u i.e. f(u) = coxDeBoor'''
        if p == 0 :
            return controlPoints[i] * homogenousCoordinates[i]
        else:
            bottom = (knots[i + degree + 1 - p] - knots[i])
            if bottom == 0:
                bottom = 1
            alpha =  (u - knots[i])/bottom
            return self.__coxDeBoor(degree = degree, controlPoints = controlPoints, knots = knots, u = u, i = i-1, p = p - 1, homogenousCoordinates = homogenousCoordinates) * ( 1 - alpha) + self.__coxDeBoor(degree = degree, controlPoints = controlPoints, knots = knots, u = u, i = i, p = p - 1, homogenousCoordinates = homogenousCoordinates) * alpha


    def __coxDeBoorHomogenousCoordinates(self,degree = None, controlPoints = None, knots = None, u = None, i = None, p = None, homogenousCoordinates = None):
        '''CoxDeBoor algorithm for Homogenous Coordinates'''
        if p == 0 :
            return homogenousCoordinates[i]
        else:
            bottom = (knots[i + degree + 1 - p] - knots[i])
            if bottom == 0:
                bottom = 1
            alpha =  (u - knots[i])/bottom
            return self.__coxDeBoorHomogenousCoordinates(degree = degree, controlPoints = controlPoints, knots = knots, u = u, i = i - 1, p = p - 1, homogenousCoordinates = homogenousCoordinates) * ( 1 - alpha) + self.__coxDeBoorHomogenousCoordinates(degree = degree, controlPoints = controlPoints, knots = knots, u = u, i = i, p = p - 1, homogenousCoordinates = homogenousCoordinates) * alpha

    def __coxDeBoorWithDictionary(self,degree = None , controlPoints = None, knots = None, u = None, i = None, homogenousCoordinates = None):
        '''original CoxDeBoor algorithm computed with dictionaries'''
        top = 1
        bottom = 1
        dictionary = {}
        for x in range (i - degree , i + 1, 1):
            for y in range(0, x + 1 , 1):
                if y == 0:
                    dictionary[str(x)+','+str(y)+ ',' + str(u)] = controlPoints[x] * homogenousCoordinates[x]
                
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

    def __coxDeBoorHomogenousCoordinatesWithDictionary(self,degree = None , controlPoints = None, knots = None, u = None, i = None, homogenousCoordinates = None):
        '''original CoxDeBoor algorithm computed with dictionaries'''
        top = 1
        bottom = 1
        dictionary = {}
        for x in range (i - degree , i + 1, 1):
            for y in range(0, x + 1 , 1):
                if y == 0:
                    dictionary[str(x)+','+str(y)+ ',' + str(u)] = homogenousCoordinates[x]
                
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
        if knotVectorType == "open":
            for i in range (1,degree + 1):
                knots.append(0)
            
            for i in range(degree + 1,len(controlPoints) + 1):
                knots.append(i - degree)
            
            for i in range(len(controlPoints) + 2, len(controlPoints) + len(knots) + 1):
                knots.append(len(controlPoints) - degree + 1)
            return knots
                
        # periodic uniform sequence
        elif knotVectorType == "periodic":
            knots =[x for x in range(0,len(controlPoints) + degree )]
            return knots
    
  
        elif knotVectorType == "bezier":
            for i in range (0, degree + 1,1):
                knots.append(0)
            for i in range(1, len(controlPoints) + degree - 2 * (degree),1):
                knots.append(i)
            knotVectorSize = len(knots)
            for i in range(0,degree + 1, 1):
                knots.append(knotVectorSize - degree)

            print(knots)
            return knots
        
        else:
            return knots


def checkU(u = None, knots = None):
    for i in range(1, len(knots)):
        if u >= knots[i] and u < knots[i+1]:
            return i
