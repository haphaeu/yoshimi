import sys

def isPrime(n,primes):
    for p in primes:
	if p==0: return True
        if n%p==0: return False
    return True

print "this will calc lots of primes"
nprimes2calc=10000000L
primes=[0L]*nprimes2calc

i=13L
primes[0:5]=[2L,3L,5L,7L,11L] #just a few to start with
ct=5
while True:
    if isPrime(i,primes):
	if i>=nprimes2calc: break
	ct+=1
        primes[ct-1]=i
        #print i #uncomment for lots of output
    i+=2L #will not be an even number
    #give some progress
    if i%10001==0: 
      sys.stdout.write("At %d - already found %d primes - last prime found is %d\r" % (i, ct, primes[ct-1]))
      sys.stdout.flush()
print ""
print "Found %d primes - last one is %d" % (ct, primes[ct-1])
pfile=open('primes.txt','w')
pfile.writelines(str(primes))
pfile.close()
print "List of primes saved in primes.txt"


