'''
Project Euler - Problem 71

Consider the fraction, n/d, where n and d are positive integers. If n<d and
HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d<=8 in ascending order of
size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7,
3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d<=1,000,000 in ascending
order of size, find the numerator of the fraction immediately to the left of
3/7.
'''

from math import ceil

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

#main

target_n = 3
target_d = 7
max_d = 1000000

#Idea: we want to be smaller than and as close as possible to 3/7.
#The smallest steps occurs for the largest denominators d.
#Algotithm is:
#   1- assuming the max d, 1000000
#   2- calculate n such that n/d<=3/7
#   3- if n/d is a proper fraction, stop, answer found.
#   4- if not, reduce n by 1 and repeat step 2.
# ###

# calculates the maximum numerator for which n/d<3/7, d=1000000
max_n = max_d * target_n/target_d
# now iterates n<max_n and finds a d<max_d
# which result in a proper fraction
n=max_n
while n>1:
    d=int(ceil(float(n)*target_d/target_n))
    #check is n/d is proper fraction
    if set(primeFactors(n,False)).intersection(
       set(primeFactors(d,False)))==set():
        print n
        break
    n-=1

#output
# 428570
