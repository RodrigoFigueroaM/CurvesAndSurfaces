#!/usr/bin/env python
'''
Line
----------
A class that computes the points on a line
attributes
----------
        *set of poits
        * color
'''
class Line(object):
    '''
    __init__
        makes the object of a line, it requires 4 parameters
        x0, y0, x1 ,y1
    '''
    def __init__(self, *argv):
        if len(argv) == 4:
            super(Line, self ).__init__()
            self.initialX,self.initialY,self.terminalX,self.terminalY = argv
            self.initialX = int(self.initialX)
            self.initialY = int(self.initialY)
            self.terminalX = int(self.terminalX)
            self.terminalY = int(self.terminalY)
            self.points=[]
            self.color = [1, 1, 1]
            self.bresenhamAlg()
        else:
            print ("4 parameters needed x0, y0, x1 ,y1")

    '''----------------------------------------------------------------------------
    __str__
    prints all the points of the line
        print(line)
        >>>[(0,0),(0,1),(0,2),(0,3)... ]
    ----------------------------------------------------------------------------'''
    def __str__(self):
         return '(linePoints= (%s))' %(self.points)

    '''----------------------------------------------------------------------------
    bresenhamAlg:
        Calculates the points for a line on a grid according to
        Bresenham's Algorithm
         params:
            self
         return: none
    ----------------------------------------------------------------------------'''
    def bresenhamAlg(self):
        xstep = 1
        ystep = 1

        #Calculate dx and dy
        dx = abs(self.terminalX - self.initialX)
        dy = abs(self.terminalY - self.initialY)

        # X as the driving axis
        if dx >= dy:
            E = 2* dy - dx

            # swap points if x0 > x1
            if self.initialX > self.terminalX :
                self.initialX,self.terminalX = self.terminalX, self.initialX
                self.initialY,self.terminalY = self.terminalY, self.initialY

            # to support 4nd and 8th octant
            if self.initialY > self.terminalY :
                ystep = ystep * -1

            for i in range(self.initialX, self.terminalX, xstep):
                self.points.append((self.initialX,self.initialY,1))
                if E >= 0:
                    self.initialY = self.initialY + ystep
                    E = E - 2*dx
                E = E + 2* dy
                self.initialX = self.initialX + xstep

        # Y as the driving axis
        else:
            E = 2* dx - dy
            # swap points if y0 > y1
            if self.initialY > self.terminalY :
                self.initialX,self.terminalX = self.terminalX, self.initialX
                self.initialY,self.terminalY = self.terminalY, self.initialY

            # to support 3nd and 7th octant
            if self.initialX > self.terminalX :
                xstep = xstep * -1

            for i in range(self.initialY, self.terminalY, ystep):
                self.points.append((self.initialX,self.initialY,1))
                if E >= 0:
                    self.initialX = self.initialX + xstep
                    E = E - 2* dy
                E = E + 2 * dx
                self.initialY = self.initialY + ystep
