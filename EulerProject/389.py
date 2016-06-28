from random import randint

def var(N):
    sz=len(N)
    sm=sum(N)
    av=1.0*sm/sz
    return sum([abs(i-av)**2 for i in N])/sz
    

#for test
# in forum, a 5-7-9 example has var 1180.0
I=[]; Ivar=[]
while True:
    T=randint(1,5)
    C=sum([randint(1,7) for _ in range(T)])
    I.append(sum([randint(1,9) for _ in range(C)]))
    Ivar.append(var(I))
    #print "%.4f" % Ivar[-1]


##while True:
##    T=randint(1,4)
##    C=sum([randint(1,6) for _ in range(T)])
##    O=sum([randint(1,8) for _ in range(C)])
##    D=sum([randint(1,12) for _ in range(O)])
##    I=[randint(1,20) for _ in range(D)]
##    In=len(I)
##    Isum=sum(I)
##    Iave=1.0*Isum/In
##    Ivar=sum([abs(i-Iave)**2 for i in I])/In
##    print "%.4f" % Ivar
