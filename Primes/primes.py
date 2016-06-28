import sys

"""project Euler, problem 10:
    The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.

Note this problem works in .35024 seconds
"""

# function range raises an error for ranges too large
#
#

from time import time
def sieve(end):  
    if end < 2: return []  

    #The array doesn't need to include even numbers  
    lng = ((end//2)-1+end%2)  

    # Create array and assume all numbers in array are prime  
    sieve = [True]*(lng+1)  

    # In the following code, you're going to see some funky  
    # bit shifting and stuff, this is just transforming i and j  
    # so that they represent the proper elements in the array.  
    # The transforming is not optimal, and the number of  
    # operations involved can be reduced.  

    # Only go up to square root of the end
    i_lim=long(end ** .5) >> 1
    for i in range(i_lim):  

        # Skip numbers that aren't marked as prime  
        if not sieve[i]: continue  

        # Unmark all multiples of i, starting at i**2  
        for j in range( (i*(i + 3) << 1) + 3, lng, (i << 1) + 3):  
            sieve[j] = False

        #if i%(i_lim/100)==0: #progress output
        #    sys.stdout.write("%i%%\r" % float(100*i/i_lim))

    sys.stdout.write("Primes located. Now calculating them...\r")

    # Don't forget 2!  
    primes = [2]  

    # Gather all the primes into a list, leaving out the composite numbers  
    #primes.extend([(i << 1) + 3 for i in range(lng) if sieve[i]])  
    #trying with xrange - range raises a MemoryError for end =~ 2e8
    primes.extend([(i << 1) + 3 for i in xrange(lng) if sieve[i]])

    return primes
limit=long(2e7)
print "Searching for primes up to", limit
startTime = time()
primes = sieve(limit)
total = sum(primes)
count=len(primes)
print("Elapsed Time = %f seconds" %(time() - startTime))
print("%i primes found and the their sum is %i" %(count, total))

#print this shit
print "Saving results to file" 
pFile=open('primes.txt','w')
for p in primes:
    pFile.write("%i\n" % p)
pFile.close()
print "Done" 
