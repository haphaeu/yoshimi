from math import log10

# Sieve of Eratosthenes for finding primes
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

def isConcatPrime(n1,n2):
    c1=n1*10**(1+int(log10(n2)))+n2 # n1n2
    c2=n2*10**(1+int(log10(n1)))+n1 # n2n1
    if c1 in PrimeSet and c2 in PrimeSet:
        return True
    return False

# ### MAIN ###
print "Getting primes"
PrimeLst=primes(int(1e8))
print "Got %d primes" % len(PrimeLst)
print "Creating set"
PrimeSet=set(PrimeLst)
sz=int(len(PrimeLst)**0.5)
print "Iterating up to %d" % sz
for i1 in range(0, sz-4):
    #print '%d' % (100*i1/(sz-4)),
    p1=PrimeLst[i1]
    for i2 in range(i1+1,sz-3):
        p2=PrimeLst[i2]
        if not isConcatPrime(p1,p2): continue
        for i3 in range(i2+1,sz-2):
            p3=PrimeLst[i3]
            if not isConcatPrime(p3,p2): continue
            if not isConcatPrime(p3,p1): continue
            for i4 in range(i3+1,sz-1):
                p4=PrimeLst[i4]
                if not isConcatPrime(p4,p3): continue
                if not isConcatPrime(p4,p2): continue
                if not isConcatPrime(p4,p1): continue
                for i5 in range(i4+1,sz):
                    p5=PrimeLst[i5]
                    if not isConcatPrime(p5,p4): continue
                    if not isConcatPrime(p5,p3): continue
                    if not isConcatPrime(p5,p2): continue
                    if not isConcatPrime(p5,p1): continue
                    #if this point is reached, p1 to p5 all
                    #concatenate to primes
                    print p1, p2, p3, p4, p5, sum([p1,p2,p3,p4,p5])

# Solution:
# 13 5197 5701 6733 8389 26033

# ### same as above but for 4 primes - to test example ###                    
##for i1 in range(0, sz-3):
##    p1=PrimeLst[i1]
##    for i2 in range(i1+1,sz-2):
##        p2=PrimeLst[i2]
##        if not isConcatPrime(p1,p2): continue
##        for i3 in range(i2+1,sz-1):
##            p3=PrimeLst[i3]
##            if not isConcatPrime(p3,p2): continue
##            if not isConcatPrime(p3,p1): continue
##            for i4 in range(i3+1,sz):
##                p4=PrimeLst[i4]
##                if not isConcatPrime(p4,p3): continue
##                if not isConcatPrime(p4,p2): continue
##                if not isConcatPrime(p4,p1): continue
##                print p1, p2, p3, p4, sum([p1,p2,p3,p4])                   
                
            
        



