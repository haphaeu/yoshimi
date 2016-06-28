#create the sequence with the terms
#of the continued fraction
terms=100
seq=[2]
i=0; k=1
while True:
    if i==terms-1: break
    seq.append(1)
    i+=1
    if i==terms-1: break
    seq.append(2*k)
    i+=1; k+=1
    if i==terms-1: break
    seq.append(1)
    i+=1
    if i==terms-1: break
#and now calculate the fraction
denominator=seq.pop()
numerator=1
while True:
    try:
        curr=seq.pop()
        numerator=denominator*curr+numerator
        #now inverse the fraction
        tmp=numerator
        numerator=denominator
        denominator=tmp
    except:
        tmp=numerator
        numerator=denominator
        denominator=tmp
        break
print "The %dth term is %d/%d." % (terms, numerator,  denominator)
#sum of the digits in the numerator
strnum=str(numerator)
soma=0
for c in strnum: soma+= int(c)
print "The sum of the digits in the numerator is %d." % soma

#output
#The 100th term is 
#6963524437876961749120273824619538346438023188214475670667
#/
#2561737478789858711161539537921323010415623148113041714756.
#The sum of the digits in the numerator is 272.

"""
#just a test
sqrt2=2.5
for i in range(20):sqrt2=2+1/sqrt2
sqrt2=1+1/sqrt2
print 2**.5-sqrt2
#just another test    
sqrt23=1.0
for i in range(5):
    sqrt23=8+1/sqrt23
    sqrt23=1+1/sqrt23
    sqrt23=3+1/sqrt23
    sqrt23=1+1/sqrt23
sqrt23=4+1/sqrt23
print 23**.5-sqrt23
#and another
from math import exp
e=1.0
for i in range(10, 0, -1):
    e=1+1/e
    e=2*i+1/e
    e=1+1/e
e=2+1/e
print exp(1.) - e
"""
