def isPrime(n):
        if n&1==0: return False 
        i=3 
        lim=int(n**.5) 
        while i<=lim: 
                if n%i==0: return False
                i+=2
        return True

#Sieve for list of primes
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
    
#this is MUCH faster then the
# isPrime() defined above!!!
def lucasLehmer(p):
  s = 4; i = 3
  while i<=p:
      #the KaratsubaSquare ended up with worse performance
      #than just doing s*s...
      #s=lucasLehmerMod(KaratsubaSquare(s)-2, p) #just a%b, implemented bitwise for speed
      s=lucasLehmerMod(s*s-2, p) #just a%b, implemented bitwise for speed
      i+=1
  if s == 0: return True
  return False
    
def lucasLehmerMod(dividend, divisor):
# fast bitwise implementation of modulo
# returns dividend % (2**divisor-1)
    mask       = (1<<divisor) - 1
    remainder  = 0
    tempResult = dividend
    while (tempResult>>divisor)!=0:
        remainder    = tempResult & mask
        tempResult >>= divisor
        tempResult  += remainder
    if tempResult==mask: return 0
    return tempResult

global kc
kc=0
def KaratsubaSquare(x):
    global kc
    kc+=1
    n=x.bit_length()
    if n<=10000: return x*x                      # Standard square
    n = (n+1) >> 1
    b = x >> n                                   # Higher half
    a = x - (b << n)                             # Lower half
    ac = KaratsubaSquare(a)                      # lower half * lower half
    bd = KaratsubaSquare(b)                      # higher half * higher half
    c = Karatsuba(a, b)                          # lower half * higher half
    return ac + (c << (n + 1)) + (bd << (2 * n))

def Karatsuba(x, y):
    global kc
    kc+=1
    n = max(x.bit_length(), y.bit_length())
    if n <= 10000: return x * y
    n = (n+1) / 2
    b = x >> n;
    a = x - (b << n)
    d = y >> n
    c = y - (d << n)
    ac = Karatsuba(a, c)
    bd = Karatsuba(b, d)
    abcd = Karatsuba(a+b, c+d)
    return ac + ((abcd - ac - bd) << n) + (bd << (2 * n))


# ### MAIN ###
myPrimes=primes(10)
for p in myPrimes:
    if lucasLehmer(p):
        print p#, 2**p-1
        
'''
2 3
3 7
5 31
7 127
13 8191
17 131071
19 524287
31 2147483647
the next would be:
61 2305843009213693951

using the Lucas-Lehmer method this cript is able to
find the 20 first Mersenne primes in a few miniutes,
which brings us to 1961!!

02 3
03 5
04 7
05 13
06 17
07 19
08 31
09 61
10 89
11 107
12 127
13 521
14 607
15 1279
16 2203
17 2281
18 3217
19 4253
20 4423

21 9689
22 9941
23 11213
24 19937
25 21701
26 23209
27 44497
28 86243 <-- 1982!!!

Speed Results - 2**11213-1

st=time.time(); lucasLehmer(11213); time.time()-st

A - simple method, using nortaml aritimethics, and isPrime()
B - Lucas-Lehmer, normal aritimethics
C - Lucas-Lehmer, (1<<p)-1 instead of 2**p-1
D - fancy MOD function using only bitwise << and +
E - fancy square function using only bitwise << and +

A - lots and lots of time (didn't wait more then 30min)
B - 3.3s
C - 3.0s
D - 0.8s
E - 0.8s - nao vale a pena ter todos esses Karatsubas ...

'''
