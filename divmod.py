from time import time
def test1(n):
    i=1
    while i<1e7:
        a,b=n//i,n%i
        i+=1
    return 0
def test2(n):
    i=1
    while i<1e7:
        a,b=divmod(n,i)
        i+=1
    return 0
N=[66,837,1847,1852437]
t1=[]
t2=[]
print "Testing // and % operators"
for n in N:
    st=time()
    test1(n)
    ft=time()
    print ft-st
    t1.append(ft-st)
print "Testing divmod"
for n in N:
    st=time()
    test2(n)
    ft=time()
    print ft-st
    t2.append(ft-st)
print "Operators are %.2f faster than divmod" % (sum(t2)/sum(t1))

'''output
Testing // and % operators
3.31699991226
3.47600007057
3.47699999809
3.52600002289
Testing divmod
4.94500017166
5.15799999237
5.17200016975
5.16799998283
Operators are 1.48 faster than divmod
'''
    
