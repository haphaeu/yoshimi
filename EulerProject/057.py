'''
Project Euler - Problem 57

It is possible to show that the square root of two can be expressed as an
infinite continued fraction.
 2 = 1 + 1/(2 + 1/(2 + 1/(2 + ... ))) = 1.414213...
By expanding this for the first four iterations, we get:
1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...
The next three expansions are 99/70, 239/169, and 577/408, but the eighth
expansion, 1393/985, is the first example where the number of digits in the
numerator exceeds the number of digits in the denominator.
In the first one-thousand expansions, how many fractions contain a numerator
with more digits than denominator
'''

#this imports the module fractions.py, writen by Rafael Rossi
#alternatively, the python module 'fractions' could be imported
#some changes are necessary if the python module is imported
from fractions import *
from math import log10

def digits(n):
    #returns the number of digits of an integer
    return int(log10(n))+1

iters=1000
numFracs=0
sqr2 = fraction(2,1)
for _ in range(iters):
    sqr2  = sumFrac(fraction(2,1), invFrac(sqr2))
    final = sumFrac(fraction(1,1), invFrac(sqr2))
    if digits(final.num)>digits(final.den): numFracs+=1
print numFracs
#output:
#153
    
    
