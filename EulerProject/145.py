"""
Project Euler - Problem 145

Some positive integers n have the property that the sum [ n + reverse(n) ]
consists entirely of odd (decimal) digits. For instance, 36 + 63 = 99 and
409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409,
and 904 are reversible. Leading zeroes are not allowed in either n or 
reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?
"""
def isReversible(n):
    if not n%10L: return False
    for c in str(n+long(str(n)[::-1])):
        if not int(c)&1: return False
    return True

from sys import stdout

# :)
print "Answer is 608720 - see code :)"
print "Now running brute force..."

#set up limits
start=long(0)
limit=long(1e8) #no reversible for 9 digits, see below

#progres report
limitPerCent=limit/100L
progresPrecision=0.01
verboseEvery=long(limit*progresPrecision/100)

#loop
n=start
ct=0L
while n<limit:
    if isReversible(n):
        ct+=1L
    if not n%verboseEvery:
        stdout.write(" Found %d - %.2f%%\r" % (ct,  1.0*n/limitPerCent))
        stdout.flush()
    n+=1L
print "Found %d reversible integers below %d" % (ct, limit)

#output:
#Found 120 reversible integers below 1000
#Found 608,720 reversible integers below 100,000,000

#Some benchmarking:
#     start    -    limit    - reversibles
#            0             9 -    ZERO
#           10 -          99 -      20
#          100 -         999 -     100
#        1,000 -       9,999 -     600
#       10,000 -      99,999 -     ZERO
#      100,000 -     999,999 -   18,000
#    1,000,000 -   9,999,999 -   50,000
#   10,000,000 -  99,999,999 -  540,000
#  100,000,000 - 999,999,999 -     ZERO(?)
#                        TOTAL  608,720
# et voi-la, cela est la bonne reponse!

"""
A very clever demosntration, by hand:

There are no 1-digit solutions.

For ab to be a two-digit solution, a+b must be odd and less than 10, 
with neither a nor b zero. There are twenty pairs.

For abc to be a three-digit solution, a+c must be odd and greater than 10,
2b must be less than 10. Five choices for b, 20 choices for ac, 
100 solutions.

For abcd to be a four-digit solution, a+d must be odd and less than 10,
neither a nor d can be zero, b+c must be odd and less than 10. Twenty 
choices for ad, thirty for bc, 600 solutions.

There are no five-digit solutions.

For abcdef to be a six-digit solution, a+f, b+e, c+d
must all be odd and less than 10. a and f cannot be zero.
20 choices for af, 30 for be, 30 for cd, 18000 solutions.

For abcdefg to be a seven digit solution:
   a+g odd and greater than 10
   b+f even and greater than 10
   c+e odd and greater than 10
   2d less than 10
5 choices for d, 20 for ce, 25 for bf, 20 for ag, 50000 solutions.

Eight digit solutions are like 2-, 4-, 6-digit solutions.
abcdefgh; a+h, b+g, c+f, d+e all odd and less than 10,
neither a nor h can be zero. 20*30*30*30=540000 solutions

There are no nine-digit solutions.

In general, moving forward, there are:
20 * 30^(n-1)        2n-digit solutions
zero                 4n+1-digit solutions, and
5*20**(n+1)*25**n    4n+3-digit solutions.

and hence:

2 digits - 2n   digits solution with n=1 - 20*30^(n-1)      =20*30^0     =20
3 digits - 4n+3 digits solution with n=0 - 5*20^(n+1)*25**n =5*20^1*25^0 =100
4 digits - 2n   digits solution with n=2 - 20*30^(n-1)      =20*30^1     =600
5 digits - 4n+1 digits solution with n=1 - ZERO solutions
6 digits - 2n   digits solution with n=3 - 20*30^(n-1)      =20*30^2     =18,000
7 digits - 4n+3 digits solution with n=1 - 5*20^(n+1)*25^n  =5*20^2*25^1 =50,000
8 digits - 2n   digits solution with n=4 - 20*30^(n-1)      =20*30^3     =540,000
9 digits - 4n+1 digits solution with n=2 - ZERO solutions
TOTAL --->                                                         TOTAL =608,720
"""