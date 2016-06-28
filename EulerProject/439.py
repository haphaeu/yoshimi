from time import time
from math import sqrt
from copy import copy

'''
this works but is too slow for the problem

too much time spent on prime fatorization

maybe a totally different approach is needed

'''

#Sieve for list of primes
def primes(n):
    if n<2: return []
    num=n//2+n%2-1
    pos=[True]*(num+1)
    i_lim=int(sqrt(n))>>1
    for i in range(i_lim):
        if not pos[i]: continue 
        start=(i*(i+3)<<1)+3
        step=(i<<1)+3 
        for j in range(start, num, step):
            pos[j]=False
    primes=[2]
    primes.extend([(i<<1)+3 for i in range(num) if pos[i]])
    return primes

#return all the prime factors of a number 
# factors(12)  = [3, 2, 2]
#
# !!! uses a global variable myPrimes !!!
# !!! uses a global dictionary myDict_p !!!
#
def primeFactors(n):
    if n in myDict_p: return copy(myDict_p[n])
    limit = sqrt(n)
    for i in myPrimes:
        if i>limit: break
        if n % i == 0:  
            ret = primeFactors(n/i)
            ret.append(i)
            myDict_p[n]=copy(ret)
            return ret
    myDict_p[n]=[n]
    return [n]

# returns a list of tuples (pi, mi)
# where a factor pi has mi occurences
# in the factors
# examples:
#
# factors=[3,2,2]
# return [(3,1),(2,2)]
#
# factors=[2,2,2,2,2]
# return [(2,5)]
#
def countFactors(factors):
    simpleFactors=list(set(factors))
    tuplesFactors=[]
    for i, f in enumerate(simpleFactors):
        tuplesFactors.append((f,factors.count(f)))
    return tuplesFactors

#
# !!! uses a global dictionary myDict_d !!!
#
def d(i,j):
# http://planetmath.org/formulaforsumofdivisors
    n=i*j
    if n in myDict_d: return myDict_d[n]
    ifactors = pFactors[i-1]
    jfactors = pFactors[j-1]
    if i>1 and j>1:                                   
        if set(ifactors) & set(jfactors) == set():    
            return d(1, i) * d (1, j)                 
    factors = countFactors(pFactors[n-1])
    prod=1
    for pi,mi in factors:
        prod*= (pi**(mi+1)-1)/(pi-1)
    myDict_d[n]=prod
    return prod

def S(N):
    i=1
    s=1
    while i<=N:
        if i>1: s+=d(i,i)
        j=i+1
        while j<=N:
            s+=(d(i,j)<<1)
            j+=1
        i+=1
    return s

# ### MAIN ###
st=time()
N=int(1e3)
print "Calculating S(%d)" % N
print "Time to run:"
#build a list of primes
myPrimes=primes(N)
t1=time()
print "\tsieve\t%.3fs" % (t1-st)
#build a list with prime factors
myDict_p={1:[]}
pFactors=[primeFactors(i) for i in xrange(1,N*N+3)]
t2=time()
print "\tfact\t%.3fs" % (t2-t1)
#dictionary for the function d(i,j)
myDict_d={1:1}
#main function
res=S(N)
t3=time()
print "\tS(n)\t%.3fs" % (t3-t2)
print "\ttotal\t%.3f" % (t3-st)
print "S(%d)=%d" % (N,res)

'''
S(1000)=563576517282
sieve took 1.420s, S(n) took 2.675s

S(10000)=5628614363174016
sieve took 1.148s, S(n) took 619.334s
'''
