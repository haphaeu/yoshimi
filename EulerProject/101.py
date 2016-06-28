#project euler problem 101
x=[1,2,3,4,5,6,7,8,9,10,11]
y=[1-k+k**2-k**3+k**4-k**5+k**6-k**7+k**8-k**9+k**10 for k in x]
#http://en.wikipedia.org/wiki/Polynomial_interpolation#Constructing_the_interpolation_polynomial
def pfit(x0,x,y,n):
    s=0
    for i in range(n):
        p=1
        for j in range(n):
            if not j==i:
                p*=1.0*(x0-x[j])/(x[i]-x[j])
        s+=y[i]*p
    return s
bops=0
for k in range(2,12):
    bops+=pfit(k,x[0:k-1],y[0:k-1],k-1)
print(bops)
# 37076114526
