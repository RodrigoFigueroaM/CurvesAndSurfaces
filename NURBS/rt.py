from Point import Point

def compute():
    coeff = [Point(0,0,1),Point(1,3,1), Point(2,3,1),Point(3,0,1)]
    degree = 2
    p = degree  #degree

    # knots =[0 for i in range(p*3+2)]
    # for i in range(p - ,p*2):
    #     knots[i] =i
    # # knots =[x for x in range(p,p*2)]
    # print(knots)

    knots =[0,0,0,0.5,1,1,1]
    
    
    # for i in range(3,9):
    for i in range(degree,degree+1):
        u = knots[i]
        stopU = u+1 

        while u <= stopU:
            x = __coxDeBoor(degree,coeff,knots,u,i,p)
            points.append(x)
            u+= 0.1

def __coxDeBoor(degree,coeff,knots,u,i, p):
    if p == 0 :
        return coeff[i]
    else:
        bottom = (knots[i + degree + 1 - p] - knots[i])
        if bottom == 0:
            bottom = 1
        alpha =  (u - knots[i])/bottom        
        return __coxDeBoor(degree,coeff,knots,u,i - 1, p - 1)* (1-alpha)  + __coxDeBoor(degree, coeff,knots,u, i , p - 1) * alpha
     

points=[]
pointsy = []
compute()

for point in points:
    print (point.x,",", point.y)




