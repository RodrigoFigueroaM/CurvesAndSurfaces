
from MyPackages.curves.BsplineTest import Bspline
from MyPackages.geometry.Point import Point

curvePoints = [Point(1,1,1),Point(5,5,1),Point(10,10,1)]
spline = Bspline()
spline.compute( curvePoints )
# print(spline.knots)
print("CONTROL")
for point in spline.controlPoints:
	print ("%s,%s" %(point.x,point.y) )

print("POINTS")
for point in spline.points:
	print ("%s,%s" %(point.x,point.y) )

# print(lookupTable)