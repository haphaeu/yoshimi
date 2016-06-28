# -*- coding: utf-8 -*-
'''
Project Euler - Problem 70

Euler's Totient function, phi(n) [sometimes called the phi function], is used
to determine the number of positive numbers less than or equal to n which are
relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than
nine and relatively prime to nine, phi(9)=6.
The number 1 is considered to be relatively prime to every positive number, so
phi(1)=1.

Interestingly, phi(87109)=79180, and it can be seen that 87109 is a permutation
of 79180.

Find the value of n, 1<n<10^7, for which phi(n) is a permutation of n and the
ratio n/phi(n) produces a minimum.
'''

#return the prime factors of a number
#second argument 'all' is a boolean
#saying if all instances of a repeated
#prime should be returned, e.g.:
# factors(12, True)  = [3, 2, 2]
# factors(12, False) = [3, 2]
def primeFactors(n, all):
    if n == 1: return [1]  
    i = 2  
    limit = n**0.5  
    while i <= limit:  
        if n % i == 0:  
            ret = primeFactors(n/i,all)
            if all: ret.append(i)
            elif not i==ret[-1]: ret.append(i)
            return ret  
        i += 1  
    return [n]  

# return the Euler's totient phi of a number
#
# for a positive integer n, the totient of n is defined as
# the number of positive integers less than or equal to n
# that are co-primes to n (ie,having no common factors other
# than 1)
#
# In other words, specifically for this problem, given a
# fraction n/d, if n and d are co-primes, the fraction cannot
# be simplified and henceforth is resilient.
#
# Extending this, for a denominator d, the numbers of
# numerators which are co-prime to d is the resilience
# of that denominator - as those fraction cannot be
# simplified. And is exaclty that that the
# totient gives => hence: resilience(d)=phi(d)
#
# Computation:
# phi(n)= n . prod(1-1/p)
# for p ranging only over distinct prime factors of n
# hence:
# phi(n)=n.(1-1/p1)(1-1/p2)(1-1/p3)...
#
#http://en.wikipedia.org/wiki/Euler's_totient_function
def totient(x):
    t = x
    for k in primeFactors(x, False):
        t -= t // k
    return t

def isPermutation(n1, n2):
    a=[c for c in str(n1)]
    b=[c for c in str(n2)]
    a.sort()
    b.sort()
    if a==b: return True
    return False


#main starts here
from time import time
t=time()
n=2
minratio=999
minn=999
while n<=1e7:
    tot = totient(n)
    if isPermutation(n, tot):
        ratio=float(n)/tot
        if ratio<minratio:
            minratio = ratio
            minn     = n
            print minn, totient(minn), minratio
    n+=1
print "Took %.3fs" % (time()-t)

'''output is
21 12 1.75
291 192 1.515625
2817 1872 1.50480769231
2991 1992 1.5015060241
4435 3544 1.25141083521
20617 20176 1.02185765266
45421 44512 1.02042145938
69271 67912 1.02001119095
75841 75184 1.0087385614
162619 161296 1.00820231128
176569 175696 1.00496880976
284029 282940 1.00384887255
400399 399040 1.00340567362
474883 473488 1.00294622039
732031 730312 1.00235378852
778669 776896 1.00228215874
783169 781396 1.00226901597
1014109 1011904 1.00217906046
1288663 1286368 1.00178409289
1504051 1501504 1.00169629918
1514419 1511944 1.00163696539
1924891 1921984 1.00151249958
1956103 1953160 1.001506789
2006737 2003776 1.00147771008
2044501 2041504 1.00146803533
2094901 2091904 1.00143266613
2239261 2236192 1.0013724224
2710627 2707216 1.00125996596
2868469 2864896 1.00124716569
3582907 3578920 1.00111402322
3689251 3685192 1.00110143515
4198273 4193728 1.00108376127
4696009 4690960 1.00107632553
5050429 5045920 1.00089359324
5380657 5375860 1.00089232234
5886817 5881876 1.00084003811
6018163 6013168 1.00083067694
6636841 6631684 1.00077763054
7026037 7020736 1.00075504904
7357291 7351792 1.0007479809
7507321 7501732 1.00074502795
8316907 8310976 1.0007136346
8319823 8313928 1.00070905112
Took 1108.932s
'''
