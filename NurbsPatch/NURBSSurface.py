#!/usr/bin/env python
from PyQt5.QtGui import  QVector3D

class NURBSSurface(object):
	"""docstring for NURBSSurface"""
	def __init__(self, controlNet = None, Udegree = 0, Wdegree = 0, Uknots = None, Wknots = None):
		super(NURBSSurface, self).__init__()
		self.surfacePoints = []
		self.Udegree = Udegree
		self.Wdegree = Wdegree
		self.controlNet = controlNet
		self.weights = self.setWeights()
		self.Uknots = Uknots
		self.Wknots = Wknots

	def compute(self):
		self.surfacePoints = []
		w = self.Wknots[ self.Wdegree ]
		stopW = self.Wknots[len(self.Wknots) - self.Wdegree]
		
		while w <= stopW:
			newPoints = []
			newWeights = []
			i = self.checkU(u = w, knots = self.Wknots)
			for row in range(0, len(self.controlNet)):
				x = self.__coxDeBoorWithDictionary(  degree = self.Wdegree,
	                                            controlPoints= self.controlNet[row],
	                                            knots = self.Wknots,
	                                            u = w,
	                                            i = i,
	                                            homogenousCoordinates = self.weights[row])

				y = self.__coxDeBoorHomogenousCoordinatesWithDictionary(degree = self.Wdegree ,
	                                                               knots = self.Wknots,
	                                                               u = w,
	                                                               i = i,
	                                                               homogenousCoordinates = self.weights[row])


				newPoints.append(x)
				newWeights.append(y)

			u = self.Uknots[ self.Udegree ]
			stopU = self.Uknots[len(self.Uknots) - self.Udegree]
			while u <= stopU:
				i = self.checkU(u = u, knots = self.Uknots)
				for p in range(1,len(newPoints)):
					Q =  self.__coxDeBoorWithDictionary(  degree = self.Udegree,
	                                            controlPoints = newPoints,
	                                            knots = self.Uknots,
	                                            u = u,
	                                            i = i,
	                                            homogenousCoordinates = newWeights)

					y = self.__coxDeBoorHomogenousCoordinatesWithDictionary(degree = self.Udegree ,
	                                                                   knots = self.Uknots,
	                                                                   u = u,
	                                                                   i = i,
	                                                                   homogenousCoordinates = newWeights)
					u += 0.1
					self.surfacePoints.append(Q/y)
			w += 0.1



	def setControlNet(self, controlNet = None):
		self.controlNet = controlNet[:]
		self.setWeights()

	def setWeights(self, weights = []):
		self.weights = weights
		for row in self.controlNet:
			self.weights.append([1,1,1,1,1,1,1,1,1,1,1])

	def __coxDeBoorWithDictionary(self, degree = None , controlPoints = None, knots = None, u = None, i = None, homogenousCoordinates = None):
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

	def __coxDeBoorHomogenousCoordinatesWithDictionary(self, degree = None , knots = None, u = None, i = None, homogenousCoordinates = None):
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

	def checkU(self, u = None, knots = None):
		for i in range(1, len(knots)):
			if u >= knots[i] and u < knots[i+1]:
				return i


#test
if __name__ == '__main__':
	surface = NURBSSurface(
			controlNet = [
                    [ QVector3D( 0,0,10 ), QVector3D( 5,0,10 ), QVector3D( -5,0,10 ), QVector3D( -10,0,10 ) ],
                    [ QVector3D( 0,0,5), QVector3D( 5,6,5 ), QVector3D( -5,6,5 ), QVector3D( -10,0,5 ) ],
                    [ QVector3D( 10,0,-5 ), QVector3D(  5,6,-5  ), QVector3D( -5,6,-5  ), QVector3D( 0,0,-5 ) ],
                    [ QVector3D( 0,0,-10 ), QVector3D( 5,0,-10 ), QVector3D( -5,0,-10 ), QVector3D( -10,0,-10 ) ]
                    ],
                     Udegree = 3,
                     Wdegree = 3,
                     Uknots = [0, 0, 0, 0, 1, 1, 1, 1],
                     Wknots = [0, 0, 0, 0, 1, 1, 1, 1])
	surface.setWeights()
	surface.compute()

	for v in surface.surfacePoints:
		print(v.x(), v.y(), v.z() )
