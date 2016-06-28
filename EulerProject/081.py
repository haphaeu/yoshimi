"""Problem 81

In the 5 by 5 matrix below, the minimal path sum from the top left to the
bottom right, by only moving to the right and down, is indicated as _xxx_
and is equal to 2427.

        _131_  673   234  103     18
        _201_  _96_ _342_ 965    150
         630   803  _746_ _422_  111
         537   699   497  _121_  956
         805   732   524   _37_ _331_

Find the minimal path sum, in matrix.txt, a 31K text file containing
a 80 by 80 matrix, from the top left to the bottom right by only
moving right and down.

file matrix.txt: http://projecteuler.net/project/matrix.txt

#built to use as a test
m=[[131, 673, 234, 103,  18],
   [201,  96, 342, 965, 150],
   [630, 803, 746, 422, 111],
   [537, 699, 497, 121, 956],
   [805, 732, 524 , 37, 331]]

!!!!!
NOTE: This algo here do not work as it is too slow! See 081_dijkstra.py

The number of possibilities (all possible paths to cover) is too high.
For a squared matrix with size n, the number of possibilities is
m=n-1 -> CentralBinomialCoefficient(2m,m)=(2m)!/(m!)^2
which gives:
n  possibilities
2    2
3    6
4   20
5   70
6  252
7  924

"""
# ##############################################################
def randomPath(size):
#this function creates a random path
#let's try and find that minimum in a very stupid way
    halfsize=size/2
    ctR=0
    ctD=0
    path=''
    while True:
        #randomly chooses between 'R' and 'D'
        #assuming 'D' as 0 and 'R' as 1
        a=randrange(0,2)
        if a==0:
            path+='D'
            ctD+=1
        else:
            path+='R'
            ctR+=1
        if ctR==halfsize:
            path+='D'*(halfsize-ctD)
            break
        if ctD==halfsize:
            path+='R'*(halfsize-ctR)
            break
    return path

def subMatrix(m,stRw,stCl,dRw,dCl):
    sm=[]
    for rows in m[stRw:stRw+dRw]:
        sm.append(rows[stCl:stCl+dCl])
    return sm


def sumPath(m,path):
# this functions sum a path in matrix m
# path is string with R's and D's
# meaning Right and Down
    row=0
    col=0
    soma = m[0][0]
    for c in path:
        if c=='R': col+=1
        elif c=='D': row+=1
        else: raise #error check tabajara
        soma += m[row][col]
    return soma



def nextPermLexic(perm):
# ###########################################################################
#The following algorithm generates the next permutation lexicographically
#after a given permutation. It changes the given permutation in-place.
#1- Find the largest index k such that a[k] < a[k + 1]. If no such index
#   exists, the permutation is the last permutation.
#2- Find the largest index l such that a[k] < a[l]. Since k + 1 is such
#   an index, l is well defined and satisfies k < l.
#3- Swap a[k] with a[l].
#4- Reverse the sequence from a[k + 1] up to and including the final
#   element a[n].
#
# Written by R.Rossi, 26th/Oct/2011
#
# Reference:
# http://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
# ###########################################################################
    #will return the next permutation
    #after 'perm' in lexicographic order
    sz=len(perm)
    #Step 1: find largest k st a[k]<a[k+1]
    k= -666
    for i in range(sz-2,-1,-1):
        if perm[i] < perm[i+1]:
            k=i
            break
    if k==-666:
        #print "\nAchieved last permutation in lexicographic order"
        return []
    else:
        #Step 2: find largest index l such that a[k] < a[l]
        l=-666
        if k==sz-2:
            l=k+1
        else:
            for i in range(sz-1,k,-1):
                if perm[k] < perm[i]:
                    l=i
                    break
        if l==-666:
            print "\nError! Oh my god, what to do?"
            return []
        else:
            #step 3: Swap a[k] with a[l]
            tmp=perm[0:k] + perm[l] + perm[k+1:l] + perm[k] + perm[l+1:]
            #step 4: reverse a[k+1:]
            tmp2=tmp[0:k+1] + tmp[-1:k:-1]
            #done.
            #save as perm
            nextPerm=tmp2
    return nextPerm
def findMinPath(matrix):
# #####
# find the path with minimum sum in matrix
# considers that the path starts in the
# top left corner and finishes at the
# bottom right corner
    m = len(matrix)    #num of rows
    n = len(matrix[0]) #num of columns
    path='D'*(m-1)+'R'*(n-1) #initial path (1st in lexic. order)
    minSum=9999*(m+n)
    minPath=''
    while path:
        soma=sumPath(matrix,path)
        if soma<minSum:
            minSum=soma
            minPath=path
        path=nextPermLexic(path)
    return minSum, minPath
def findMinPath2(matrix):
# #####
# find the path with minimum sum in matrix
# considers that the path starts in the
# top left corner and finishes ANYWHERE
# ALONG THE BOTTOM OR RIGHT EDGE
    m = len(matrix)    #num of rows
    n = len(matrix[0]) #num of columns
    #build all possible start paths
    #to iterate lexicographically
    #
    #finishing along bottom edge
    stPath=[]
    for i in range(n):
        stPath.append( 'D'*(m-1) + 'R'*i )
    #finishing along right edge
    for i in range(m):
        stPath.append( 'D'*i + 'R'*(n-1) )
    minSum=9999*(m+n)
    minPath=''    
    #now iterate through these paths
    for path in stPath:
        nextpath=path
        while nextpath:
            soma=sumPath(matrix,nextpath)
            if soma<minSum:
                minSum=soma
                minPath=nextpath
            nextpath=nextPermLexic(nextpath)
    return minSum, minPath            
# ##### MAIN #######################################################
import sys
from time import time
from random import randrange

#doesnt work under proxy
#import urllib
#url='http://projecteuler.net/project/matrix.txt'
#page=urllib.urlopen(url)
#matrix=page.read()

#read matrix from file
pfile=open('081_matrix.txt','r')
matrix=pfile.read()
pfile.close()
#break lines
matrix=matrix.split('\n')
#remove last empty element
matrix.pop()
#break rows
matrix_str=[row.split(',') for row in matrix]
#convert to int
m=[]
for i in range(len(matrix_str)):
    m.append([])
    for j in range(len(matrix_str[0])):
        m[i].append(int(matrix_str[i][j]))
del matrix, matrix_str

"""
m=[[131, 673, 234, 103,  18],
   [201,  96, 342, 965, 150],
   [630, 803, 746, 422, 111],
   [537, 699, 497, 121, 956],
   [805, 732, 524 , 37, 331]]
"""

m_size=len(m)
m_path_len=2*(m_size-1)
#possible number of permutations - for a 80x80 matrix, this is 10^46
#so now way it is going to solve with brute force
from math import factorial
numPerms= factorial(2*m_path_len) / factorial(m_path_len)**2


# #####
# the idea is to create small sub-matrixes of
# size m x n (m rows, n columns) and
# find the path with minimum sum in these
# sub-matrixes, and then go on from that point
st=time()
#size of submatrixes
initOrder_rw=3
initOrder_cl=3
subM_row_sz=initOrder_rw
subM_col_sz=initOrder_cl
row=col=0
minSum=0
minPath=''
while True:
    sm = subMatrix(m,row,col,subM_row_sz,subM_col_sz)
    if col+subM_row_sz==m_size or row+subM_row_sz==m_size:
        #reached an edge, end path must the bottom
        #right corner of submatrix
        tmpSum, tmpPath = findMinPath(sm)
    else:
        #no edge yet, exit can be any point along bottom and
        #right edger of submatrix
        tmpSum, tmpPath = findMinPath2(sm)
    #minSum+=tmpSum
    row += tmpPath.count('D')
    col += tmpPath.count('R')
    minPath+=tmpPath
    if col == m_size-1 and row == m_size-1:
        break
    if col+subM_col_sz > m_size:
        subM_col_sz=m_size-col
    if row+subM_row_sz > m_size:
        subM_row_sz=m_size-row
print "For a submatrix of order %d x %d, the minimum is %d (took %.1fms)" % (initOrder_rw, initOrder_cl, sumPath(m,minPath), 1000*(time()-st))

"""
output:
min is 506359 (order=7x7)
For a submatrix of order 2, the minimum is 548877 (took 0.000000s)
For a submatrix of order 3, the minimum is 554442 (took -0.016000s)
For a submatrix of order 4, the minimum is 539768 (took -0.031000s)
For a submatrix of order 5, the minimum is 547676 (took -0.047000s)
For a submatrix of order 6, the minimum is 581545 (took -0.172000s)
For a submatrix of order 7, the minimum is 506359 (took -0.624000s) ***
For a submatrix of order 8, the minimum is 565323 (took -1.919000s)
For a submatrix of order 9, the minimum is 538268 (took -5.304000s)
For a submatrix of order 10, the minimum is 582770 (took -24.835000s)
For a submatrix of order 11, the minimum is 589818 (took 77.0s)
"""



##let's try in a brute and stupid way
minSum=999999
ct=0
##flag to choose random or lexic path builder
useRandom=False
if useRandom:
    path=randomPath(m_path_len)
    maxIter=100000
else:
    path='D'*(m_path_len/2) + 'R'*(m_path_len/2)
    maxIter=numPerms
while ct<maxIter:
    soma=sumPath(m,path)
    if soma<minSum:
        minSum=soma
        print minSum , path
    if useRandom: 
        path=randomPath(m_path_len)
    else:         
        path=nextPermLexic(path)
        if path==[]: break
    ct+=1

#run for a couple of hours
#last minimum found
#735097 DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDRRDRRRRRRRRRRRRRRRRRRRRRRRDRRRRRRRRRRDRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRDDDR