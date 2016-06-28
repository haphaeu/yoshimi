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
	#so, explanation is: largest factor is the square root of the number
	#but in this case, as our array has only odd numbers, we need to do
	#only half the steps to get to the square root, so that's why the square
	#root is being devided by 2.
    for i in range(i_lim):
        if not pos[i]: continue #position already marked as False, skipping
        #
        #considering a sequence of the odd numbers starting at 3
        #[3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41...]
		# 0 1 2 3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 th
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
    primes.extend([(i<<1)+3 for i in range(num) if pos[i]])
    
    return primes

from time import time
st=time()
limit=int(1e6)
Primes=primes(limit)
print "took %.3f" % (time()-st)

#
# for limit=10,000,000 it takes less than 2s
#
