'''
matrix.py

Basic operations with matrixes:
- multiply
- transpose
- invert

And a simple linear least squares solver,
performing a linear fit between two vectors
yi = a+b.xi

Revision History
rev      Date      Description
0.1   2013.02.13   first issue, basic insanity check


Rafael Rossi
RaRossi@external.technip.com
rossirafael@yahoo.com
'''

#importing deepcopy to copy list and make sure the
#original lists are not altered
from copy import deepcopy

'''
matrix A with m rows and n columns
matrix B with o rows and p columns
AB = A.B with m rows and o columns
constraint: n==o
'''
def mmult(A,B):
    n=len(A)
    m=len(A[0])
    p=len(B)
    o=len(B[0])
    if not n==o: return 0
    AB=[[0.0 for i in range(m)] for j in range(p)]
    for i in range(m):
        for j in range(p):
            AB[j][i]=0.0
            for k in range(n):
                AB[j][i]+=A[k][i]*B[j][k]
    return AB

'''
returns the transpose of a matrix
matrix A with m rows and n columns
'''
def transpose(A):
    n=len(A)
    m=len(A[0])
    B=[[0.0 for i in range(n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            B[i][j]=A[j][i]
    return B

'''
returns the inverse of a *square* matrix
'''
def minverse(Ao):
    A=deepcopy(Ao)
    m = len(A)
    if not m==len(A[0]): return 0
    #create zero matrix
    AI=[[0.0 for i in range(m)] for j in range(m)]
    #fill identity matrix
    for i in range(m): AI[i][i]=1.0
    #invert - Gaussian elimination
    for k in range(m):
        for i in range(k,m):
            tmp = 1.0 * A[k][i]
            for j in range(k,m):
                A[j][i] /= tmp
            for j in range(m):
                AI[j][i] /= tmp
        for i in range(k+1,m):
            for j in range(k,m):
                A[j][i]-= A[j][k]
            for j in range(m):
                AI[j][i] -= AI[j][k]
    for i in range(m-2, -1, -1):
        for j in range(m-1, i, -1):
            for k in range(m):
                AI[k][i] -= A[j][i] * AI[k][j]
            for k in range(m):
                A[k][i] -= A[j][i]*A[k][j]
    return AI

'''
perform linear least squares fit between
2 vectors xo and yo.
returns coefficients a and b such that
yoi = a+b.xoi
constraints: both xo and yo need to be a row
vector xo=[n,n,n,n] with same size.
'''
def leastsquares(xo,yo):
    n=len(xo)
    if not n==len(yo): return 0
    y=[deepcopy(yo)]
    x=[[1]*n,deepcopy(xo)]
    return mmult(mmult(minverse(mmult(transpose(x),x)),transpose(x)),y)[0]
    

