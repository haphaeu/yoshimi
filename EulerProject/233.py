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
eps=1e-10
#1e9 passou de 1000
#6e8 passou de 420
#5.5e8 deu 
#5e8 deu 360
#1e8 deu 68
#1e7 deu 60
#1e6 deu 52
#1e5 deu 44
#1e4 deu 36
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
N_over_2=N/2.
N_sqrd_over_2=0.5*N**2
#iterate trhough domain x
ct=0
for x in xrange(int(lowerBound),int(upperBound+1)):
    #given integer x, calculate y1 as float
    y1 = N_over_2 + sqrt( N_sqrd_over_2 - (x-N_over_2)**2 )
    if abs(y1-int(y1))<eps: 
        ct+=2 #due to symmetry, always 2 points count
        #print ct, x
        #progress
        sys.stdout.write("progress %.2f%%\r" % (float(x-lowerBound)/(domainRangePercentage)))
    if ct>420:
        print "\ncanceled"
        break
print "\nf(%d)=%d" % (N,  ct)
#output
#for N=10,000 -> f(N)=36
