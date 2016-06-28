from time import time
st=time()
print len(set([a**b for a in range(2,101) for b in range(2,101)])),
print "(took %.2fms)" % (1000*(time()-st))
#output:
#9183 (took 15.00ms)