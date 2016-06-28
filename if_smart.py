from time import time

NUM=10000000
print "starting"

#Firstly an IF with a very fast condition (False)
#followed by a complex condition (NUM/i+i/3...)
st=time()
for i in range(1,NUM):
    if False and (NUM/i+i/3)%33==0: p=1
print "A smart order of conditions took %.3fs to run" % (time()-st)

#Then the order of the conditions is reversed
#so that the complex comes first
st=time()
for i in range(1,NUM):
    if (NUM/i+i/3)%33==0 and False: p=1
print "A stupid order of conditions took %.3fs to run" % (time()-st)

#And finally, making sure that the complex condition
#is not evaluated if the first (fast) condition is false
st=time()
for i in range(1,NUM):
    if False:
        if (NUM/i+i/3)%33==0: p=1
print "A 'conservative' order of conditions took %.3fs to run" % (time()-st)
print "See ==> Always write the faster conditions first in an IF statement <=="
print "Or, if unsure, use concatenated IFs"