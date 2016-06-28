def isPrime(n,primes):
    for p in primes:
        if n%p==0: return False
    return True

i=13
primes=[2,3,5,7,11] #just a few to start with
sum=2+3+5+7+11
while True:
    if isPrime(i,primes):
	if i>=2000000: break
	sum+=i
        primes.append(i)
        #print i #uncomment for lots of output
    i+=2 #will not be an even number
print sum, primes[-1]
# took more than 30min to compute
# sum=142913828922, last prime=1,999,993
