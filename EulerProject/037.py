"""
Project Euler - Problem 37
The number 3797 has an interesting property. Being prime itself, it is 
possible to continuously remove digits from left to right, and remain
prime at each stage: 3797, 797, 97, and 7. Similarly we can work from
right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from
left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""

def primes(n):
# Implementation of the prime finding algorithm of
# Sieve of Eratosthenes
    if n<2: return []
    num=n//2+n%2-1
    pos=[True]*(num+1)
    i_lim=int(n**0.5)>>1
    for i in range(i_lim):
        if not pos[i]: continue #position already marked as False, skipping
        start=(i*(i+3)<<1)+3
        step=(i<<1)+3 
        for j in range(start, num, step):
            pos[j]=False
    primes=[2] #need to consider 2!!!
    primes.extend([(i<<1)+3 for i in range(num) if pos[i]])
    return primes
# #########################################################################
def isTruncable(n,primes):
	strn=str(n)
	sz=len(strn)
	for i in range(1,sz):
		if not int(strn[i:]) in primes or not int(strn[:i]) in primes:
			return False
	return True
# #########################################################################

# ### MAIN ###
from time import time
st=time()
listPrimes=primes(999999)
tsum=0
ct=0
for p in listPrimes:
	if p<10: continue
	if isTruncable(p,listPrimes):
		tsum+=p
		ct+=1
		print p, 
		if ct==11: break
print "sum is %d (took %.3fs)" % (tsum, (time()-st))

#output is:
#23 37 53 73 313 317 373 797 3137 3797 739397 sum is 748317 (took 89.139s)

