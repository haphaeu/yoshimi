'''

!!! THIS IS A MODIFICATION OF AN EULER PROBLEM !!!
Instead of doing what the problem asks, this just
iterates and solves sqrt(2)

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
expansion, 1393/985 (...)
'''

#this imports the module fractions.py, writen by Rafael Rossi
#alternatively, the python module 'fractions' could be imported
#some changes are necessary if the python module is imported
from fractions import *
iters=9
sqr2 = fraction(2,1)
for _ in range(iters):
    sqr2 = sumFrac(fraction(2,1), invFrac(sqr2))
sqr2 = sumFrac(fraction(1,1), invFrac(sqr2))
print "With %d iterations, sqrt of 2 is %d/%d=%f" % (iters, sqr2.num, sqr2.den,float(sqr2.num)/sqr2.den)