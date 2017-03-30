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
        self.degree = 3
        if self.degree == 0 or  self.degree  >= len(self.controlPoints):
            self.degree = len(self.controlPoints) - 1

        p = self.degree

        self.knots = [0,0,0,1,2,3,3,3]
        self.knots = self.__computeKnotVector( degree = self.degree , knotVectorType = "open uniform")
        print("KNOTS:",self.knots)
        self.homogenousCoordinates = [1 for i in range(0,len(self.controlPoints)) ] # attached to each control point


        u = self.knots[ self.degree ]
        stopU = self.knots[len(self.knots) - self.degree ]
        while u <= stopU:
            i = checkU(u, self.knots)
            # x = self.__coxDeBoor(self.degree,self.controlPoints,self.knots,u,i,p)
            # y = self.__coxDeBoorY(self.degree,self.controlPoints,self.knots,u,i,p)

            x = self.__coxDeBoorWithDictionary(self.degree,self.knots,u,i,p)
            y = self.__coxDeBoorWithDictionaryY(self.degree,self.knots,u,i,p)
            self.points.append(x/y)
            u += 0.05


    def __coxDeBoor(self,degree,controlPoints,knots,u,i, p):
        '''original CoxDeBoor algorithm'''
        if p == 0 :
            print(controlPoints[i])
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


    def __coxDeBoorWithDictionary(self,degree,knots,u,i, p):
        '''original CoxDeBoor algorithm computed with dictionaries'''
        top = 1
        bottom = 1
        somewhereelse = {}
        for x in range (i - degree , i + 1, 1):
            for y in range(0, x + i + degree , 1):

                abottom = (knots[x + degree + 1 - y] - knots[x])
                if abottom == 0:
                    abottom = 1
                alpha =  (u - knots[x])/abottom

                top = alpha
                bottom = 1 - top

                if y == 0:
                    somewhereelse[str(x)+','+str(y)+ ',' + str(u)] = self.controlPoints[x] * self.homogenousCoordinates[x]

                else:
                    bottomVal = 0
                    if str(x-1)+','+str(y-1) + ',' + str(u) in somewhereelse:
                        bottomVal = somewhereelse[str(x-1)+','+str(y-1) + ',' + str(u)]

                    somewhereelse[str(x)+','+str(y) + ',' + str(u) ] =  somewhereelse[str(x)+','+str(y-1)+ ',' + str(u)] * top + bottomVal * bottom

        return somewhereelse[str(i)+','+str(p) + ',' + str(u)]

    def __coxDeBoorWithDictionaryY(self,degree,knots,u,i, p):
        '''original CoxDeBoor algorithm computed with dictionaries'''
        top = 1
        bottom = 1
        somewhereelse = {}
        for x in range (i - degree , i + 1, 1):
            for y in range(0, x + i + degree , 1):

                abottom = (knots[x + degree + 1 - y] - knots[x])
                if abottom == 0:
                    abottom = 1
                alpha =  (u - knots[x])/abottom

                top = alpha
                bottom = 1 - top

                if y == 0:
                    somewhereelse[str(x)+','+str(y)+ ',' + str(u)] = self.homogenousCoordinates[x]

                else:
                    bottomVal = 0
                    if str(x-1)+','+str(y-1) + ',' + str(u) in somewhereelse:
                        bottomVal = somewhereelse[str(x-1)+','+str(y-1) + ',' + str(u)]

                    somewhereelse[str(x)+','+str(y) + ',' + str(u) ] =  somewhereelse[str(x)+','+str(y-1)+ ',' + str(u)] * top + bottomVal * bottom

        return somewhereelse[str(i)+','+str(p) + ',' + str(u)]





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
            return i
