from meusPrimos import primes
from time import time
myPrimes=primes(10000)
sz=len(myPrimes)
st=time()
tg=2
while True:
    n=[0]*(tg+1)
    n[0]=1
    for i in range(sz):
        j=myPrimes[i]
        while j<=tg:
            n[j]+=n[j-myPrimes[i]]
            j+=1
    if n[tg]>5000: break
    tg+=1
et=time()-st
print tg
print "took",et,"s"
# 71    
