'''
Problem 95
The proper divisors of a number are all the divisors excluding the number
itself. For example, the proper divisors of 28 are 1, 2, 4, 7, and 14.
As the sum of these divisors is equal to 28, we call it a perfect number.

Interestingly the sum of the proper divisors of 220 is 284 and the sum of
the proper divisors of 284 is 220, forming a chain of two numbers. For this
reason, 220 and 284 are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with 12496,
we form a chain of five numbers:

12496  14288  15472  14536  14264 ( 12496  ...)

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element
exceeding one million.

======
brucutu solution:
the code is kind of brute force... the function sumdivs() is not
clever at all.

anyway, found a clue [1] that the largest chain has 28 elements.
so, just started high, at 10,000 and run until a 28-elements chain was found,
which occurred at 14,316

Indeed, this answer is given in [2]...

[1] https://en.wikipedia.org/wiki/Sociable_number
[2] http://mathworld.wolfram.com/SociableNumbers.html
'''

##### BRUCUTU MODIS ON #####
#Brucutu sumdivs
'''
def sumdivs(n):
    i=2
    ie=n/2
    s=1
    while i<=ie:
        if not n%i: s+=i
        i+=1
    return s
def chain(n):
    i=1
    m=n
    s={m}
    while True:
        m=sumdivs(m)
        #print m,
        if m>1e6 or m in s and not m==n:
            i=0
            break
        if m==n: break
        s.add(m)
        i+=1
    return i
        
#MAIN
i=10000
while i<1e6:
    sz=chain(i)
    if sz: print i, sz
    i+=1
'''

##### CLEVER MODE ####
from time import time

#  Clever sumdivs.
#  Using Eratosthenes Sieve style - each number is a divisor
# of its multiples.
#   1. create an array SUMDIV filed with 1's (1 divides all numbers)
#   2. loop N from 2 to LIMIT
#   2.1. subloop, starting from 2N, step N, add N to SUMDIV
#  At the end, we have a buffer with the sum of divisors for all numbers
# up to LIMIT.
def init_sumdivs():
    limit=1000000
    sumdivs=[1]*limit
    n=2
    while n<limit:
        pos=2*n
        while pos<limit:
            sumdivs[pos-1]+=n
            pos+=n
        n+=1
    return sumdivs

def chain(n):
    i=1
    m=n
    s={m}
    while True:
        m=sumdivs[m-1]
        #print m,
        if m>1e6 or m in s and not m==n:
            i=0
            break
        if m==n: break
        s.add(m)
        i+=1
    return i
        
#MAIN
t0=time()
sumdivs=init_sumdivs()
print "init took %.3fms" % (time()-t0)
t0=time()
i=10000
mxsz=0
while i<1e6:
    sz=chain(i)
    if sz>mxsz:
        mxsz=sz
        print i, sz
    i+=1
print "took another %.3fms" % (time()-t0)
