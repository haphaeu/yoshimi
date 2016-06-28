def isPermutation(n1, n2):
    a=[c for c in str(n1)]
    b=[c for c in str(n2)]
    a.sort()
    b.sort()
    if a==b: return True
    return False
x=1
while True:
    if isPermutation(x,  2*x) and \
       isPermutation(x,  3*x) and \
       isPermutation(x,  4*x) and \
       isPermutation(x,  5*x) and \
       isPermutation(x,  6*x):
           break
    x+=1
print x
