"""
 check how amazingly faster a set is in an 'in' statement

 when doing 
            'if x in iterable'
 
 set is considerably faster than list
 by a factor of more than 100 for a few
 thousands elements and increasing 
 for larger sizes of iterables,
 reaching up to 5000x for 100thousand elements
 
 see end of code for benchmarking results
"""

from time import times

SIZE=100000

ls=[i for i in range(SIZE)]
st=set(ls)

start=time()
for i in range(SIZE):
  if i in st: dummy=1
st_time=time()-start
print "set took %.3fs" % st_time

start=time()
for i in range(SIZE):
  if i in ls: dummy=1
ls_time=time()-start
print "list took %.3fs" % ls_time

print "set is %.2f times faster" % (ls_time/st_time)


#output:

#for SIZE=1000
#set took 0.000s
#list took 0.015s
#set is 63.56 times faster

#for SIZE=10000
#set took 0.003s
#list took 1.346s
#set is 502.19 times faster

#for SIZE=20000
#set took 0.005s
#list took 5.461s
#set is 1002.92 times faster

#for SIZE=30000
#set took 0.008s
#list took 12.096s
#set is 1512.43 times faster

#for SIZE=100000
#set took 0.027s
#list took 145.176s
#set is 5387.09 times faster
