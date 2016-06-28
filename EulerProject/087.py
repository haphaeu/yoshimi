#Sieve for list of primes
def primes(n):
    if n<2: return []
    num=n//2+n%2-1
    pos=[True]*(num+1)
    i_lim=int(n**0.5)>>1
    for i in range(i_lim):
        if not pos[i]: continue 
        start=(i*(i+3)<<1)+3
        step=(i<<1)+3 
        for j in range(start, num, step):
            pos[j]=False
    primes=[2]
    primes.extend([(i<<1)+3 for i in range(num) if pos[i]])
    return primes

# ### MAIN ###
from time import time
st=time()
LIM=50000000
myPrimes=primes(int(LIM**0.5))
sz=len(myPrimes)
mySet=set()
LIM=50000000
for p1 in myPrimes:
        a=p1*p1
        if a>LIM: break
        for p2 in myPrimes:
                b=p2*p2*p2
                m=a+b
                if m>LIM: break
                for p3 in myPrimes:
                        n = m + p3*p3*p3*p3
                        if n>LIM: break
                        mySet.add(n)

print len(mySet), "took",time()-st,"s"
# 1097343 took 1.24899983406 s
                        

