#return the prime factors of a number second argument 
#'all' is a boolean saying if all instances of a repeated
#prime should be returned, e.g.:
# factors(12, True)  = [3, 2, 2]
# factors(12, False) = [3, 2]
def primeFactors(n, all):  
    if n == 1: return [1]  
    i = 2  
    limit = n**0.5  
    while i <= limit:  
        if n % i == 0:  
            ret = primeFactors(n/i,all)
            if all: ret.append(i)
            elif not i==ret[-1]: ret.append(i)
            return ret  
        i += 1  
    return [n]

# simplifies a list of prime factors by replacing a factor
# p repeated n times by p^n, for example:
# primeFactors(12,True)=[3,2,2] 
# replaceRepeatedFactors([3,2,2])={3,2^2}={3,4}
def replaceRepeatedFactors(factors):
    simpleFactors=list(set(factors))
    if simpleFactors==factors: return set(factors)
    for i, f in enumerate(simpleFactors):
        simpleFactors[i]=f**factors.count(f)
    return set(simpleFactors)

from time import time
st=time()
n=100000
while True:
    s1=replaceRepeatedFactors(primeFactors(n, True))
    s2=replaceRepeatedFactors(primeFactors(n+1, True))
    s3=replaceRepeatedFactors(primeFactors(n+2, True))
    s4=replaceRepeatedFactors(primeFactors(n+3, True))
    if len(s1)==4 and len(s2)==4 and \
       len(s3)==4 and len(s4)==4 and \
       s1.intersection(s2.intersection(s3.intersection(s4)))==set():
        print n,    s1
        print n+1,  s2
        print n+2,  s3
        print n+3,  s4
        break
    n+=1
print "(took %.2fs)" % (time()-st)

#output:
#134043 set([7, 3, 13, 491])
#134044 set([47, 31, 4, 23])
#134045 set([17, 83, 19, 5])
#134046 set([9, 2, 11, 677])
#(took 5.02s)
