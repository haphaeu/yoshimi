#
# Project Euler - Problem 243
#
#A positive fraction whose numerator is less than its denominator is called a 
#proper fraction.
#
# for any denominator, d, there will be d-1 proper fractions; for example, with
# d=12:
#1/12 , 2/12 , 3/12 , 4/12 , 5/12 , 6/12 , 7/12 , 8/12 , 9/12 , 10/12 , 11/12.
#
#We shall call a fraction that cannot be cancelled down a resilient fraction.
#Furthermore we shall define the resilience of a denominator, R(d), to be the 
#ratio of its proper fractions that are resilient; for example, R(12) = 4/11.
#In fact, d=12 is the smallest denominator having a resilience R(d)<4/10
#
#Find the smallest denominator d, having a resilience R(d) < 15499/94744 .
#
# ###########################################################################



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

#calculate the resilience factor of a denominator
#see comments in function totient(x)
#specially that resilience(d)=phi(d)
def resilience(x):
    return totient(x) / (x - 1. )

minResilience=15499./94744
min=res=99

#note that this is slow, to make it quicker will
#depend basically on a good choice of initial x
#so this is done by trials
x = 2 * 2 * 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23

while res > minResilience:
    res = resilience(x)
    if res < min:
        min=res
        print x, res
    x+=1