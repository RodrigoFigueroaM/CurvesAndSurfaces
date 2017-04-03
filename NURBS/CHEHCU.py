#!/usr/bin/env python

import math
def checkU(u = None, knots = None, start = None):
    for i in range(start, len(knots) - start):
        if u <= knots[i] and u < knots[i+1]:
            return i

if __name__ == "__main__":
    pi = math.pi
    knots = [0,0,0,pi/2, pi/2,pi,pi,3*pi/2,3*pi/2,2*pi, 2*pi, 2*pi]
    u = 0
    stopU = knots[9]
    while u <= stopU:
        i = checkU(u, knots,2)
        print(i)
        u += 0.1
