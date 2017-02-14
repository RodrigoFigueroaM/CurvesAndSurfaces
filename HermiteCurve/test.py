#!/usr/bin/env python

from Point import Point

if __name__ == '__main__':
	print("hello")
	li = []
	lidata = []


	a = Point(1,1,1)
	b = Point(2,2,2)
	c = Point(3,3,3)
	lidata.append(a.data())
	lidata.append(b.data())
	lidata.append(c.data())
	li.append(a)
	li.append(b)
	li.append(c)	

	a.translate(10,0,0)

	for point in li:
		print(point)

	for i, point in enumerate(lidata):
		print(i, point)
