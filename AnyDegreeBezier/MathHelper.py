#!/usr/bin/env python

def binomialCoefficient(k):
    li = [0 for x in range(0,k+1)]
    li[0] = 1
    for i in range(1, k+1):
        for j in range(i,0 , -1):
            li[j] = li[j] + li[j-1]
    return li
