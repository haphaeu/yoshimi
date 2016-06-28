def isPrime(n,primes):
    for p in primes:
        if n%p==0: return False
    return True

ct=0
i=12
primes=[2,3,5,7,11] #just a few to start with
while ct<10001:
    if isPrime(i,primes):
        primes.append(i)
        ct+=1
        #print ct, i #uncomment for lots of output
    i+=1
print ct, i-1
    
