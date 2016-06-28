# Project Euler Problem 80
# http://projecteuler.net/problem=80
# http://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Decimal_.28base_10.29
def sqroot(num):
    res=0
    bit=1<<100
    while bit>num:
        bit>>=2
    while not bit==0:
        if num>=res+bit:
            num-=res+bit
            res=(res>>1)+bit
        else:
            res>>=1
        bit>>=2
    return res

def sqroot(num):
    res=0.0
    bit=2.0**30
    while bit>num:
        bit/=4.0
    while not bit==0:
        if num>=res+bit:
            num-=res+bit
            res=(res/2.0)+bit
        else:
            res/=2.
        bit/=4.
    return res
