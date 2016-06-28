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



#
# Implementation of the prime finding algorithm of
#
#    ___ Sieve of Eratosthenes ___
#
# as per reference
# http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
# 
# A very fast algorithm. Instead of looking for primes,
# which involves modules and lots of divisions, it uses
# quick bit shifts to mark all non-primes numbers in a
# range - non-prime numbers are multiple of smaller numbers
# in this sequence.
#
# Optimisation is done by excluding all the even numbers,
# performing a number of 'seeks' of the magnitude os the
# half of the squared root of the upper bound of the sequence,
# and finally by strating each 'seek' at the square of its
# seed odd number.
#
# See wikipedia page for details.
#
# NOTE: this version is modified. See original in Primes/meusPrimos.py
#
# R. Rossi - October 2011
#
def primes(n):
    if n<2: return []
    
    #max number of primes up to 'n'
    #which is the number of odd numbers
    #discounting 1 (the prime number 2)
    num=n//2+n%2-1

    #allocate an array filled with True
    #assumung initially that all numbers will be primes
    #this array represents all the odd numbers starting from 3
    #[3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,...,num]
    pos=[True]*(num+1)

    #number of factors to check is Sqrt(n)/2    
    i_lim=int(n**0.5)>>1
    #!!! maybe add more description here on the meaning of i_lim
    for i in range(i_lim):
        if not pos[i]: continue #position already marked as False, skipping
        #
        #considering a sequence of the odd numbers starting at 3
        #[3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41...]
        #and also considering that the indexes of this sequence **start at 0**
        #the _start_ is the index in this sequence of the square of the i_th element
        #   i   i_th odd   odd^2  index
        #   0      3        9       3
        #   1      5       25      11
        #   2      7       49      23
        #   3      9       81      39
        #   ...
        # the _step_ will be the i_th element of the sequence
        #
        #the loop will work like this:
        # i=0 => start=3, step=3 => non-prime odds:[9,15,21,27,33,39,...]
        # i=1 => start=11,step=5 => non-prime odds:[25,35,45,55,65,...]
        # i=2 => start=23,step=7 => non-prime odds:[49,63,77,...]
        # ...
        start=(i*(i+3)<<1)+3
        step=(i<<1)+3 
        for j in range(start, num, step):
            pos[j]=False

    #need to consider 2!!!
    primes=[2]
    #and now back calculates all the primes given their positions
    # if ith odd number is prime, ith_prime_number = 2*i + 3
    ###MODIFICATION: both primes and pos are returned
    primes.extend([(i<<1)+3 for i in range(num) if pos[i]])
    #attention: when using pos, remember 2 is not there!
    #to check is n (odd) is prime, use: pos[(n-3)/2)==True
    return pos,  primes
    
# #########################################################################

#quick function to check if a number is prime using the returned array
#from the function 'primes'define above
def isPrime(n):
    if n==1: return False
    if n==2: return True
    if isEven(n): return False
    return globalPRIMESPOS[(n-3)>>1]
# #########################################################################

#quick function to check if a number is even
def isEven(n):
    if n&1==0: return True
    return False
# #########################################################################

#check is a fraction is resilient (cannot be simplified)
def isResilient(n,d):  
    if n==1: return True
    #if both are even, can be divided by 2
    if isEven(n) and isEven(d): return False
    #if numerator is prime, cannot be simplified
    if isPrime(n): return True
    #if denominator is divisible by numerator, can be simplified
    if d%n==0 and not n==1: return False
    #now we have to iterate, knowing that 
    #at least one of them is not even,
    #so we only have to check if they're divisible by odd numbers
    fim=n/2+1
    for mdc in globalPRIMES:
        if mdc > fim: return True
        if n%mdc==0 and d%mdc==0: return False
    
#calculate the resilience factor of a denominator
def resilience(d):
    resilientFractions=0
    i=1
    while i<d:
        if isResilient(i,d):
            resilientFractions+=1
        i+=1
    return resilientFractions

# #########################################################################

from sys import stdout
from time import time

#attention, this is used as a global variable in order to
#avoid passing it as argument to a number of funcions
# resilience()->isResilient->isPrime...
global globalPRIMESPOS
global globalPRIMES

st=time()
#define the limits
lim= 1000000
print "Marking primes up to %d" % lim
globalPRIMESPOS, globalPRIMES = primes(lim)
print "Done. Starting to calculating resiliences"

minResilience=15499./94744

#d has to be at least 94745
d=94745
while False:
    st=time()
    res_d = float(resilience(d)) / float(d)
    stdout.write("The resilience of %d is %.3f (took %.3fs)\r" % (d, res_d,  time()-st))
    stdout.flush()
    if res_d < minResilience:
        break
    d+=1
print d

#
# ok, ok, shame on me... this works, but...
# took more than 1h to loop from 94,745 to 95,000-
# and the answer is 892,371,480 (!!!!!!)
# make a quick handcalc to see how long my stupid brute
# force method would take :PPPP
# have a look in the 243.hs (in Haskell), which
# which uses a magic Euler Phi functions, or totients. 
# need to learn that...
#

