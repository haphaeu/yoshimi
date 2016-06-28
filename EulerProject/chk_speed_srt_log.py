'''
Check for speed

Need to get each digit of a number and sum them.
Which is faster:
1. use a list of strings
2. calculate using log

Conclusion:

splitting the digits of a number is faster using math calculation with log
than using string conversion. Log showed up to be 2.76x faster!

Disadvantage is that using log is more complex.
Str lambda function is 1 liner.

>>>See project euler problem 74, which run 5x faster using logs!!

'''
from math import log10
from time import time

#sum the digits of a number, using log
def sum_log(n):
    if n<10: return n
    o=int(log10(n))
    d = n/10**o
    return d + sum_log(n-d*10**o)

#sum the digits of a number, using string conversion
sum_str = lambda n: sum([int(a) for a in str(n)])

#and now check which one is faster
iters=100000
r=1
while r<=3:
    t0=time()
    i=1
    while i<=iters:
        s=sum_str(i)
        i+=1
    t1=time()
    i=1
    while i<=iters:
        s=sum_log(i)
        i+=1
    tf=time()
    print "Trial %d - str took %.3fs and log took %.3fs" % (r, t1-t0, tf-t1),
    print " - log is %.2f times faster than str" % ((t1-t0)/(tf-t1))
    r+=1

'''
output
Trial 1 - str took 0.717s and log took 0.266s  - log is 2.70 times faster than str
Trial 2 - str took 0.718s and log took 0.249s  - log is 2.88 times faster than str
Trial 3 - str took 0.717s and log took 0.265s  - log is 2.71 times faster than str
'''
