'''
Project Euler - Problem 74
http://projecteuler.net/problem=74

Factorial chains...

145 => 1! + 4! + 5! = 1 + 24 + 120 = 145
hence, 145 has a chain with only 1 element

69 => 363600 => 1454 => 169 => 363601 ( => 1454 )
hence, 69 has a chain of 5 elements.

How many numbers below 1 million have a factorial
chain with 60 non-repeating elements?

'''
from math import factorial as fact
from math import log10
from time import time

#counts the length of the factorial chain starting at n
def length(n):
    l=[n]
    m=nxt(n)
    while m not in l:
        l.append(m)
        m=nxt(m)
    return len(l)

#calculates the next term of the factorial chain
def nxt(n):
    if n<10: return fact(n)
    order = int(log10(n))      #order of n
    digit = n/10**order        #leftmost digit
    rest  = n-digit*10**order  #rest of n w/o its leftmost digit
    if rest: orest = int(log10(rest))   #order of the rest
    else:    orest = 0
    zeros = order-orest-1      #if n has no zeros in it, orest=order-1
                               #if it has zeros, need to accont for them
                               #noting that 0! = 1
    return fact(digit) + zeros + nxt(rest)

#start main code here
st=time()
n=1
c=0
while n<=1000000:
    if length(n)==60:
        c+=1
        #print n,
    n+=1
print c
print time()-st

#output
# 402
# took less than a minute, due to the optimisation of the next term function
# not using list of strings, but log10 instead
