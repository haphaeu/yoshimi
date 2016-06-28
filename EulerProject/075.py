from time import time
from math import ceil
from sys  import stdout
st=time()
L=1000000
countOne = 0
while L>1:
    count=0
    a=1
    a_lim = int(ceil(L/3.)-1)
    while a<=a_lim:
        b=(L-a)/2
        while a<b:
            c=L-a-b
            if a*a+b*b==c*c: count+=1
            b-=1
        a+=1
    if count==1:
        countOne+=1
        print "Found L %d" % L
    L-=1
    if L%100==0: stdout.write("%.3f%%\r" % (100.*L/1500000))
print countOne
print time()-st

