'''
Project Euler - Problem 58

'''
def isPrime(n):
    for i in range(2,1+int(n**0.5)):
        if n%i==0: return False
    return True

from sys import stdout
from time import time
st=time()
#generates the terms in the diagonal of the matrix,
#as per the problem definition,
#and check if they're primes
diag=[1]
numPrimes=0
sz=2
while True:
    for _ in range(4):
        diag.append(diag[-1] + sz)
        if isPrime(diag[-1]):
            numPrimes+=1
    #calculate the ratio of primes
    ratio=float(numPrimes)/len(diag)
    stdout.write("For a square of size of %d, the ratio is %.4f%%\r" % (1+sz, 100*ratio))
    if ratio<0.1: break
    #increment size of square
    sz+=2

#give user some output
print "\ntook %.3fs" % (time()-st)

# output
# For a square of size of 26241, the ratio is 9.9998%%
# took 22.901
#