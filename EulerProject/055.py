def isPalindromic(n):
    if int(str(n)[::-1])==n: return True
    return False
#main
from time import time
i=10
numLychrel=0
st=time()
while i<10000:
  ct=0
  ri=i
  flag=True
  while ct<50:
    ri+=int(str(ri)[::-1])
    if isPalindromic(ri):
      flag=False
      break
    ct+=1
  if flag:
    numLychrel+=1
  i+=1
print "found %d (took %.1fms)" % (numLychrel, 1000*(time()-st))
#output
#249