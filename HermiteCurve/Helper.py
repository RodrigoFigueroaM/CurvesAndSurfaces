'''----------------------------------------------------------------------------
distance:
    calculates the distance between two points in one dimension
    params: p0, p1
    return: Integer distance
----------------------------------------------------------------------------'''
def distance(p0, p1):
    distance = (p1 - p0)
    return  abs(distance)

def isElementOfVector(point, v):
    if v.pointOne == point or v.pointTwo == point: 
        return True
    return False
