'''
Project Euler - Problem 169

Solution:
based on the recursive property:
f(n) = f(n/2)+f(n/2-1), n even
f(n) = f((n-1)/2),      n odd

note the HUGE speed up due to the caching...
'''

from repoze.lru import lru_cache

@lru_cache(maxsize=5000)
def way2p2(n):
    if n==0 or n==1: return 1
    if n&1: return way2p2((n-1)/2)           #n odd
    else:   return way2p2(n/2)+way2p2(n/2-1) #n even

print way2p2(10**25)

# 178653872807
