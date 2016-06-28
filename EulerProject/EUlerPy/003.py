"""
Project Euler Problem 3
=======================

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143?
"""


def isPrime(n):
    i=2L
    while i<n:
        if n%i==0:
            return False
        i += 1
    return True
    
n=600851475143L
#n=13195

i=1L
p=1L
while True: 
    if n%i==0:
        #print "factor", i,
        if isPrime(i):
            #print "prime!!!"
            p *= i
            if p==n:
                #print "done"
                break
        else:
            #print "not prime"
            n /= i
    i += 1L
print i


        

