#Project Euler Problem 50

# ### !!!
# Using the script meusPrimos.py
from meusPrimos import primes

Primes=primes(1000000)
SZ=len(Primes)
SumPrimes=[]
SumPrimes.append(0)
for i in range(SZ): SumPrimes.append(SumPrimes[-1]+Primes[i])
SumPrimesSet=set(SumPrimes)

maxjump=0
maxp=0
for j in range(SZ):
    p=Primes[SZ-j-1] #get a big prime
    for i in range(SZ):
        sk=p+SumPrimes[i]
        if sk in SumPrimesSet: #making this set boosts speed!!!
            jump=SumPrimes.index(sk)-i
            if jump>maxjump:
                maxjump=jump
                maxp=p
                print maxp, maxjump, i
            break
print maxp, maxjump
'''
just run for a few seconds
and the answer will show up:
999983 29 3669
999863 71 1623
999809 79 1470
999769 109 1083
999749 237 458
999721 495 53
998857 509 38
997651 543 3   <---

'''
    
    
