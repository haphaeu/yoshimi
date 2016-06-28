'''
Project Euler - Problem 69

Euler's Totient function, f(n) [sometimes called the phi function], is used to
determine the number of numbers less than n which are relatively prime to n.
For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively
prime to nine, f(9)=6.

n   Relatively Prime    f(n)    n/f(n)
2          1             1        2
3          1,2           2        1.5
4          1,3           2        2
5          1,2,3,4       4        1.25
6          1,5           2        3
7          1,2,3,4,5,6   6        1.1666...
8          1,3,5,7       4        2
9          1,2,4,5,7,8   6        1.5
10         1,3,7,9       4        2.5

It can be seen that n=6 produces a maximum n/f(n) for n<=10.

Find the value of n <= 1,000,000 for which n/f(n) is a maximum.
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


#main starts here
n=2
maxratio=-1
maxn=-1
while n<=1000000:
    ratio=float(n)/totient(n)
    if ratio>maxratio:
        maxratio = ratio
        maxn     = n
    n+=1
print maxn, maxratio

#output is
#510510 5.53938802083

'''
Also, a more elegant solution, as pointed out in the forum:

A maximum for n/totient(n) occurs for a minimum of totient(n).
The totient(n) gives the numbers of co-primes of n.
To find a minimum for totient(n), one needs to find a number
with very few co-primes. *Hence, a product of primes*
Multiplying all smallest primes so that the product is smaller
then 1,000,000:
p     prod
2        2
3        6
5       30
7      210
11    2310
13   30030
17  510510 <- this is our guy :D
19 9699690



'''
