#although this function is very simple
#this is not the best way as previous
#terms can be used to speed up the#process
def fib(n):
    if n==1 or n==2:
        return 1
    else:
        return fib(n-1)+fib(n-2)

from math import log
from time import time
st=time()
a=1
b=1
idx=2
while True:
    c=a+b
    a=b
    b=c
    idx+=1
    if int(log(c, 10)+1)==1000:
        break

print "first term in Fibonnacci sequence to have 1000 digits is the %d th." % idx
print "run in %.3f" % (time()-st)
