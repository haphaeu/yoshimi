
'''
this works but takes years...


there are some clues at the bottom...

'''

from math import factorial
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
def totient(x):
    t = x
    for k in primeFactors(x, False):
        t -= t // k
    return t

fact13 = factorial(13)
n=6227180929*2
LIM=10*n
ct=0
while n<LIM:
    if totient(n)==fact13:
        ct+=1
        print ct, n, primeFactors(n,True)
    n+=1
'''
1    6 227 180 929
2    6 227 182 993
3    6 227 186 509
4    6 227 199 361
5    6 227 220 691
6    6 227 229 637
7    6 227 245 393
8    6 227 246 107
9    6 227 260 969
10   6 227 267 713
11   6 227 268 799

some clue... the n found have only 2 large prime factors:
1 6227180929 [93601L, 66529]
2 6227182993 [99793L, 62401]
3 6227186509 [108109L, 57601]
4 6227199361 [131041L, 47521]
5 6227220691 [161281L, 38611]
6 6227229637 [172801L, 36037]
7 6227245393 [192193L, 32401]
8 6227246107 [193051L, 32257]
9 6227260969 [210601L, 29569]
10 6227267713 [218401L, 28513]
11 6227268799 [219649L, 28351]
12 6227279341 [231661L, 26881]
13 6227280491 [232961L, 26731]

fudeu
4*n
1 24908759550 [1093L, 331, 17, 5, 5, 3, 3, 3, 3, 2]


opa!
2*n
1 12454361858 [93601L, 66529, 2]
2 12454365986 [99793L, 62401, 2]
3 12454373018 [108109L, 57601, 2]

'''
