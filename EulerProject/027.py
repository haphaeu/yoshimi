# Euler Project - Problem 27
# Considering quadratics of the form:
#
# n**2 + an + b, where |a| < 1000 and |b| < 1000
#
# Find the product of the coefficients, a and b, for the quadratic 
# expression that produces the maximum number of primes for 
# consecutive values of n, starting with n = 0.
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

#equation defined in the problem 27
#in the form n+a+b.n**2
def eq(n,a,b):
    return n**2+a*n+b
# #########################################################################


from time import time
st=time()

#define the limits
a_lim= 1000
b_lim= 1000
n_lim= 100


#makes an array with the position of all primes up to 'limit'
#from this point on, to check if a number is a prime number,
#just need to check its respective "position" in pos,
#all the primes are marked as true. just need to make sure that
#'limit'is large enough to cover all the required range of primes.
#the brief function 'isPrime' does this jobs by using pos
limit=eq(n_lim, a_lim, b_lim)
print "Marking primes up to %d" % limit
pos=primes(limit)
print "Done. Staring to find coefficients for the equation."
maxp=0
amax=0
bmax=0
for a in range(-a_lim,a_lim+1):
    for b in range(-b_lim,b_lim+1):
        ct=0
        for n in range(n_lim+1):
            m=eq(n,a,b)
            if m>limit: #just to make sure
                print "Error: need to increase limit."
                raise SystemExit
            if isPrime(m,pos):
                ct+=1
            else:
                break
        if ct>maxp:
            maxp=ct
            amax=a
            bmax=b
print "Coefficient a=%d and b=%d return %d consecutive primes" % (amax, bmax, maxp)

print "(took %.3fs to run)" % (time()-st)

#output is:
#Marking primes up to 111000
#Done. Staring to find coefficients for the equation.
#Coefficient a=-61 and b=971 return 71 consecutive primes
#(took 13.995s to run)
