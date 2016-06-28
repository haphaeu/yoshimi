#Project Euler Problem 51

# ### !!!
# Using the script meusPrimos.py
from meusPrimos import primes

Primes=primes(1000000)
PrimesSet=set(Primes)
SZ=len(Primes)
N=3
FAMILY=8

def checkN(p,N):
    pstr=[c for c in str(p)]
    for c in pstr:
        if pstr.count(c)==N:
            return int(c)
    return -1
def replace(p,old,new):
    pstr=[c for c in str(p)]
    if new==0 and int(pstr[0])==old:
        return -1 #leading 0's not allowed
    for i,c in enumerate(pstr):
        if int(c)==old:
            pstr[i]=str(new)
    v=0
    pstr.reverse()
    for i in range(len(pstr)):
        v+=int(pstr[i])*10**i
    return v

start=100000
for p in Primes:
    if p<start: continue
    d=checkN(p,N)
    if d==-1: continue
    count=0
    for i in range(10):
        if replace(p,d,i) in PrimesSet:
            count+=1
    if count==FAMILY: break
print p
            
'''
takes about 1s ...
121313

'''
