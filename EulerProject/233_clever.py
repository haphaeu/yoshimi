"""
Project Euler - Problem 233

 Circle passing through (0,0),(N,0),(0,N),(N,N)
 this is a square - so the diameter of the circle
 is N*Sqrt(2), and its centre is (N/2,N/2)
 Circle equation is 
 (X-Xc)^2+(Y-Yc)^2=N^2/2 or
 (x-N/2)^2 + (y-N/2)^2 = N^2/2
 
 for a given N, the x domain Dx is
 lower bound N/2 - N*sqrt(2)/2 = N/2*(1-sqrt(2))
 upper bound N/2 + N*sqrt(2)/2 = N/2*(1+sqrt(2))
 same domain applied for y, Dy
 
 for a given x, the y is
 (y-N/2)^2 = N^2/2 - (x-N/2)^2
 y-N/2 = sqrt( N^2/2 - (x-N/2)^2 )
 y     = N/2 +/- sqrt( N^2/2 - (x-N/2)^2 )
 hence
 y1     = N/2 + sqrt( N^2/2 - (x-N/2)^2 )
 y2     = N/2 - sqrt( N^2/2 - (x-N/2)^2 )
 
 So, for a given integer N
 1- iterate integer x in domain Dx
 2- given x calculate y1 and y2 (floats)
 3- check if integers y1 and y2 satisfy circle equation
    (x-N/2)^2 + (y1-N/2)^2 - N^2/2 < eps
    (x-N/2)^2 + (y2-N/2)^2 - N^2/2 < eps
"""
from math import sqrt
import sys
from time import time
st=time()
eps=1e-10
try:
   N=int(sys.argv[1])
except:
   N=int(1e7)
print "using N=%d (%.3e)" % (N, N)
lowerBound = N/2*(1-sqrt(2))
upperBound = N/2*(1+sqrt(2))
domainRange = upperBound - lowerBound
domainRangePercentage=domainRange/100. 
#prepare some variables to avoid re-calculate
N_over_2=N/2.0
N_sqrd_over_2=0.5*N**2
rootFinderDelta=sqrt(N)
rootFinderTol=1.0e-4
#iterate trhough domain x
ct=0
x=int(lowerBound)
while x<=N_over_2:
    #given integer x, calculate y1 as float
    y1 = N_over_2 + sqrt( N_sqrd_over_2 - (x-N_over_2)**2 )
    if abs(y1-int(y1))<eps:
        #due to symmetry, always 2 points count
        # +2 positive and negavtive y
        # +2 either sides (left and right) of the circle
        ct+=4 
        #progress (either one of the below)
        print ct, x, 
        #sys.stdout.write("progress %.2f%%\r" % (float(x-lowerBound)/(domainRangePercentage)))
        # === estimate next x ===
        # line equation, tangent to (x,y1)
        a = -(x-N_over_2)/(y1-N_over_2)
        b = y1 - a * x
        #root finder by delta
        h0=-1.0
        iters=0
        delta=rootFinderDelta
        while abs(h0)>rootFinderTol:
           x+=delta
           h1=a*x+b-1.0-N_over_2-sqrt(N_sqrd_over_2-(x-N_over_2)**2)
           if h0*h1<0: delta*=-0.5
           h0=h1
           iters+=1
        x=int(x)
        print "next x is %d, with tol %f after %d iters" % (x, h0, iters)
    if ct>420:
        print "\ncanceled"
        break
    x+=1
print "\nf(%d)=%d (took %.3fs)" % (N,  ct, (time()-st))

#output:
# f(10000000)=60 (took 10.702s)
