# http://projecteuler.net/problem=85
#grid size
from time import time
t0=time()
target=2e6
minerr=9e9
for m in range(30,90):
    for n in range(30,m+1):
        ct=0
        for k in range(1,m+1):
            for l in range(1,n+1):
                ct+=(m-k+1)*(n-l+1)
        err=abs(target-ct)
        if err<minerr:
            minerr=err
            min_ct=ct
            min_m =m
            min_n =n
print min_m,min_n,min_ct,min_m*min_n
print "took %.2fms" % (1000*(time()-t0))
# output:
# 77 36 1999998 2772
#
# or, clever Partha's idea:
# A grid m by n has m+1 by n+1 lines.
# Any rectangle is limited by 2 lines in each way.
# Ao, the number of rectangle is all the possible
# combination of 2 lines amongst the total number of lines.
# This applies in both directions, then:
# grid (m,n)
# number of rectangles = comb(m+1,2) * comb(n+1,2)
# = (m+1)! / 2 / (m-1)! * (n+1)! / 2 / (n-1)!
# = (m+1)*m * (n+1)*n /4
# :)
#
t0=time()
minerr=9e9
for m in range(30,90):
    for n in range(30,m+1):
        ct=(m+1)*m*(n+1)*n/4
        err=abs(target-ct)
        if err<minerr:
            minerr=err
            min_ct=ct
            min_m =m
            min_n =n
print min_m,min_n,min_ct,min_m*min_n
print "took %.2fms" % (1000*(time()-t0))
#
#
# now attempt to solve this by root finding
# f(m,n)= (m+1)*m * (n+1)*n /4 - 2e6
# simple way to find minimum is converting f
# to f(n), fixing m0, then loops through only n
# f(n) = (n+1)*n * (m0+1)*m0 /4 - 2e6
# using Bhaskara:
# n= -1 + sqrt(1+32e6/mo/(mo+1))/2
#
t0=time()
minerr=9e9
for m in range(30,90):
    n=int(round(-1 + (1+32e6/m/(m+1))**0.5/2))
    ct=(m+1)*m*(n+1)*n/4
    err=abs(target-ct)
    if err<minerr:
            minerr=err
            min_ct=ct
            min_m =m
            min_n =n
print min_m,min_n,min_ct,min_m*min_n
print "took %.2fms" % (1000*(time()-t0))
