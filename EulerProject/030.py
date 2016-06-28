from time import time
st=time()
tsum=0
for n in range(2,200000): #upper bound found by trials
	if n==sum([int(c)**5 for c in str(n)]): 
		print n
		tsum+=n
print "sum is %d (took %.3fms)" % (tsum, 1000*(time()-st))
#output:
#4150
#4151
#54748
#92727
#93084
#194979
#sum is 443839 (took 1295.000ms)