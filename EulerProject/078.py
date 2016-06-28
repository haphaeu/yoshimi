# Project Euler Problem 078
# Partitions
# http://en.wikipedia.org/wiki/Partition_(number_theory)#Exact_formula
#
# if n<0: p(n)=0
# if n=0: p(n)=1
# else:   p(n)=sum_k( (-1)**(k-1) * p(n-g_k) )
#         where g_k=k(3k-1)/2, for k nonzero (negative and positive)
#
# solving limits for k such that n-g_k>=0:
#       n = k(3k-1)/2
#       3k^2 - k - 2n = 0
#   =>  k = ( 1 +/- sqrt(24n+1) ) / 6
#
# That's all folks.
def part(n):
    if n==0: return 1
    _ = 0
    LIM=1+int((1+(24*n+1)**0.5)/6)
    for k in range(-LIM,LIM):
        if k==0: continue
        idx=n-k*(3*k-1)/2
        if 0<=idx<n:
            _ += int((-1)**(k-1)) * p[idx]
    return _

NUM=int(1e6)
p=[0]*NUM
for i in xrange(int(NUM)):
    p[i]=part(i)
    #print i, p[i]
    if p[i]%1000000==0: break
print i, p[i]
# 55374 36325300925435785930832331577396761646715836173633893227071086460709268608053489541731404543537668438991170680745272159154493740615385823202158167635276250554555342115855424598920159035413044811245082197335097953570911884252410730174907784762924663654000000
    
