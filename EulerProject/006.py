def sqsumsq(n):
    sumsq=0
    sqsum=0
    for i in range(n+1):
        sqsum += i
        sumsq += i**2
    return sqsum**2, sumsq

a,b= sqsumsq(100)
print a-b

