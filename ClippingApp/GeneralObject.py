#!/usr/bin/env python
class GeneralObject(object):

    def __init__(self, *argv):
        super(GeneralObject, self ).__init__()
        self.points=[]
        self.color = [1, 0, 0]

    def __str__(self):
        return 'GeneralObject= %s' %(self.points)
