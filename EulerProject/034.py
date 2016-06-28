from math import factorial
i=3
tsum=0
while i<50000:
    c=str(i)
    sum=0
    for d in c:
        sum+= factorial(int(d))
    if sum==i:
        tsum+=i
        print i
    i+=1
print "done"
print tsum

#output is
#145
#40585
# so here I stop and tryed 40585+145=40730 :P