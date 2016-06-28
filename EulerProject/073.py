'''
Project Euler - Problem 73

totally stupdly brute force floating point error subject method o_O
but works =P
'''
a=set()
t=1./3
h=1./2
for d in xrange(2,12001):
    for n in xrange(1,d):
        b=float(n)/d
        if b>t and b<h:
            a.add(b)
print len(a)
#output
# 7295372
        
