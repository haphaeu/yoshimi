# Euler Project - Problem 38
# The number, 197, is called a circular 
# prime because all rotations of the digits: 
#    197, 971, and 719, are themselves prime.
#
# There are thirteen such primes below 100: 
#    2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
#
# How many circular primes are there below one million?
# ############################################



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
    ###MODIFICATION: don't need to evaluate the primes, neither returning them
    ###just need to return the array with their positions
    ###primes.extend([(i<<1)+3 for i in range(num) if pos[i]])
    ###return primes
    #attention: when using pos, remember 2 is not there!
    #to check is n (odd) is prime, use: pos[(n-3)/2)==True
    return pos
# #########################################################################

#quick function to check if a number is prime using the returned array
#from the function 'primes'define above
def isPrime(n,pos):
    if n==1: return False
    if n==2: return True
    if isEven(n): return False
    return pos[(n-3)>>1]
# #########################################################################

#quick function to check if a number is even
def isEven(n):
    if n&1==0: return True
    return False
# #########################################################################

#check if a prime is circular
#do not check is argument is prime!
#this is done separately
#def isCircular(n, listPrimes):
    
# #########################################################################

#circulate a number
# abc -> bca, cab
def circulate(n):
    strn=str(n)
    sz=len(strn)
    circ=[]
    for i in range(sz-1):
        circ.append(int(strn[i+1:]+strn[0:i+1]))
    return circ

# #########################################################################

from time import time
st=time()

#define the limits
lim= 1000000

print "Marking primes up to %d" % lim
pos=primes(lim)
lenpos=len(pos)
print "Done. Staring to find circular primes."
ct=1 #already counting the 2
i=0
circPrimes=[]
while i<lenpos:
    if pos[i]:
        prime=(i<<1)+3
        if prime<10:
            circPrimes.append(prime)
            ct+=1
        else:
            listCirc=circulate(prime)
            flag=True
            for p in listCirc:
                if not isPrime(p, pos): 
                    flag=False
                    break
            if flag:
                circPrimes.append(prime)
                ct+=1
    i+=1
print circPrimes
print "found %d circular primes up to %d" % (ct,  lim)
print "(took %.3fs to run)" % (time()-st)

#output:
# Marking primes up to 1000000
# Done. Staring to find circular primes.
# [3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, 97, 113, 131, 197, 199, 311, 337, 373, 719, 733, 919, 971, 991, 1193, 1931, 3119, 3779, 7793, 7937, 9311, 9377, 11939, 19391, 19937, 37199, 39119, 71993, 91193, 93719, 93911, 99371, 193939, 199933, 319993, 331999, 391939, 393919, 919393, 933199, 939193, 939391, 993319, 999331]
# found 54 circular primes up to 1000000
# (took 1.130s to run)
