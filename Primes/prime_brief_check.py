def isPrime(n):
        if n&1==0: return False #even number
        i=3 #start 3, step 2 - check only odds
        lim=int(n**.5) #need to check until sqrt of n, inclusive!
        while i<=lim: #using while to minimise memory allocation
                if n%i==0: return False
                i+=2
        return True

import time

st=time.time()
ret=isPrime(18014398777917439)
t=time.time()-st
print ret, t
'''
some larghe primes
      200560490131
     4398050705407
    70368760954879
 18014398777917439
 '''
