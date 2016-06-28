from math import factorial
comb = lambda n, r: factorial(n)/(factorial(r)*factorial(n-r))
print sum([1 for n in range(101) for r in range(n+1) if comb(n, r)>1e6])

