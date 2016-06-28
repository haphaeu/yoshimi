#function which returns the number
#of factors of a number
def fact(n):
    #new way - took 15s
    last=n
    i=1
    fact=0
    while True:
      if n%i==0: 
        fact+=2
        last=n/i
      if i>=last: break
      i+=1
    return fact
        
    #my old slow way = took 5h
    ##fact=[1]
    ##for i in xrange(2,n/2+1):
    ##    if n%i==0: fact.append(i)
    #fact.append(n)
    #return len(fact)

#function which returns the triangle
#number of an integer
def triang(n):
    s=0
    for i in xrange(n+1):
        s+=i
    return s 

#import sys
from time import time
i=2600
t=triang(i)
numfactors=500
start=time()
while True:
    factors=fact(t)
    #sys.stdout.write("%d                 \r" % factors)
    #sys.stdout.flush()
    #print i, t, factors
    if factors>=numfactors:
        print t
        break
    i+=1
    t+=i
print time()-start
