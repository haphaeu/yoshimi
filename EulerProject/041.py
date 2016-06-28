"""
Project Euler - Problem 41

We shall say that an n-digit number is pandigital if it makes use of all the
digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is
also prime.

What is the largest n-digit pandigital prime that exists?
"""
def isPandigital(strN):
    Ln = [c for c in strN]
    Ln.sort() 
    Lck=[str(i) for i in range(1,len(Ln)+1)]
    if Ln == Lck:
        return True
    return False
# #########################################################################
def primes(n):
# Implementation of the prime finding algorithm of
# Sieve of Eratosthenes
	num=n//2+n%2-1
	pos=[True]*(num+1)
	i_lim=int(n**0.5)>>1
	for i in xrange(i_lim):
	    if not pos[i]: continue #position already marked as False, skipping
	    start=(i*(i+3)<<1)+3
	    step=(i<<1)+3
	    for j in xrange(start, num, step):
	        pos[j]=False
	prime=[((i)<<1)+3 for i in xrange(num) if pos[i]]
	return prime
# #########################################################################

# MAIN #
listPrimes=primes(7654321)
listPrimes.reverse()
maxPan=0
for p in listPrimes:
	if isPandigital(str(p)):
		print p
		break
#output
#7652413