#!/usr/bin/env python

import math 

class Vector(object):
    """docstring for Vector"""
    def __init__(self, *argv):
        super(Vector, self).__init__()
        self.pointOne, self.pointTwo = argv


    def __str__(self):
        return 'a= %s, b= %s' %(self.pointOne, self.pointTwo)


    def magnitude(self):
        return math.sqrt(self.pointOne.x * self.pointOne.x + self.pointOne.y * self.pointOne.y + self.pointOne.z * self.pointOne.z)

    def dot( self, other):
        return self.pointOne.x * other.pointOne.x + self.pointOne.y * other.pointOne.y +  self.pointOne.z * other.pointOne.z


    def angle( self, other):
        '''u · v = |u| |v| cos θ
            u · v /|u| |v| =  cos θ
            acos(u · v /|u| |v|) = θ
        '''
        return  math.acos(self.dot(other) / (self.magnitude() * other.magnitude()) )


    def slope( self):

        if self.pointTwo.x - self.pointOne.x == 0:
            return 0
        return (self.pointTwo.y - self.pointOne.y) / (self.pointTwo.x - self.pointOne.x) 


    def normalize( self):
        ''' x = ax/|a|
            y = ay/|a|
            z = az/|a|'''
        magnitude = self.magnitude()
        tempPointOne = self.pointOne
        tempPointTwo = self.pointTwo
        self.pointOne.x = self.pointOne.x / magnitude
        self.pointOne.y = self.pointOne.y / magnitude
        self.pointTwo.x = self.pointTwo.x / magnitude
        self.pointTwo.y = self.pointTwo.y / magnitude

        self.pointOne.translate(tempPointOne.x,tempPointOne.y , 1)
        self.pointOne.translate(tempPointTwo.x,tempPointTwo.y , 1)
        
      
      
    def translate(self,x, y, z):
        self.pointOne.translate(x, y , z)
        self.pointTwo.translate(x + self.magnitude(), y + self.magnitude(), z)
        
        

        
