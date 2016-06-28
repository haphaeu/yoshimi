#gcd - Greatest Commom Divisor
#in this problem, the use is
#if gcd==1: a and b are Coprimes
#http://en.wikipedia.org/wiki/Euclidean_algorithm#Implementations
def gcd(a, b):
    while not a == b:
        if a > b:
           a = a - b
        else:
           b = b - a
    return a
