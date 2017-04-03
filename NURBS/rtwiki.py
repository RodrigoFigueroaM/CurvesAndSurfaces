from Point import Point

def compute():
    coeff = [0, 0, 0, 6, 0, 0, 0]
    degree = 3
    p = degree  #degree
    knots =[i for i in range(len(coeff)+ p +2)]
    knots =[-2, -2, -2, -2, -1, 0, 1, 2, 2, 2, 2]
    
    # print(knots[i])
    # for i in range(3,9):
    for i in range(3,7):
        u = knots[i]
        stopU = u+1 
        print("U",u, stopU)
        print(i)
        
        while u <= stopU:
            x = __coxDeBoor(degree,coeff,knots,u,i,p)
            points.append(x)
            u+= 0.05

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
x = -2.0
for point in points:
    print (x,",", point)
    x += 0.05
