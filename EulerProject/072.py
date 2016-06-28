'''
Project Euler - Problem 72

Consider the fraction, n/d, where n and d are positive integers. If n<d and
HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d<=8 in ascending order
of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3,
5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper fractions
for d<=1,000,000?

Solution:
=========

For each denominator d, the fraction n/d is a proper fraction if n and d do
not have any common division rather than one, in other words, n/d is a proper
fraction for all n which are co-primes of d. This is the definition of the
totient function. Hence, for d varying from 1 to 1e6, need to add totient(d).

Note:
If d is a prime, all n/d are proper fractions. But adding this to the code
does not decrease running time notably. I tested and run only 25% faster...
'''

from time import time

#MODIFIED - return SET, do NOT repeat
#return the prime factors of a number
# factors(12) = set([3, 2])
def primeFactors(n):
    if n == 1: return set([1])
    i = 2  
    limit = n**0.5  
    while i <= limit:  
        if n % i == 0:  
            ret = primeFactors(n/i)
            ret.add(i)
            return ret  
        i += 1  
    return set([n])

#http://en.wikipedia.org/wiki/Euler's_totient_function
def totient(x):
    t = x
    for k in primeFactors(x):
        t -= t // k
    return t

#main starts here
st=time()
max_d=int(1e6)
d=2
c=0
while d<=max_d:
    c+=totient(d)
    d+=1
    
print( "Total number of proper fractions: %d" % c)
print( "Took %.3fs" % (time()-st))

#output
#Total number of proper fractions: 303963552391
#Took 23.951s
