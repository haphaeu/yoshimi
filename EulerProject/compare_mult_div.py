from time import time

i=0
limit=10000000
st=time()
while i < limit:
    p=i/3.
    i+=1
print "divisao levou %f" % (time()-st)
i=0
st=time()
f = 1.0/3.0
while  i<limit:
    p=i*f
    i+=1
print "mult levou %f" % (time()-st)