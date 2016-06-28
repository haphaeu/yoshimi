
from time import time
st=time()
numTerms=2500
penta=[i*(3*i-1)>>1 for i in range(1, numTerms+1)]
#this set is created to be used in the if x in set
#this is amazingly faster than doing the same with a list
pentaset=set(penta)
minD=penta[-1]
for i,x in enumerate(penta):
    for y in penta[:i]:
        if x+y in pentaset and x-y in pentaset:
               D=x-y
               if D < minD:
                   minD=D
                   print "Found a minimum of %d for the pair (%d, %d) - max term is %d" % (minD,x,y,i)
print "(took %.3fs to run)" % (time()-st)           

#output
#Found a minimum of 5482660 for the pair (7042750, 1560090) - max term is 2166
#(took 0.702s to run)
