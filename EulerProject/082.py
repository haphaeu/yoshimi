"""Problem 82

Note: This problem is a more challenging version of Problem 81.

The minimal path sum in the 5 by 5 matrix below, by starting in 
any cell in the left column and finishing in any cell in the 
right column, and only moving up, down, and right, is 
indicated in *x; the sum is equal to 994.

 131   673   234*  103*   18*
 201*   96*  342*  965   150
 630   803   746   422   111
 537   699   497   121   956
 805   732   524    37   331

Find the minimal path sum, in matrix.txt, containing a 80 by 80 matrix, 
from the left column to the right column.
http://projecteuler.net/project/matrix.txt

"""

#This code implements the Dijkstra algorithm for minimum path finder.
#
# Modification from problem 81:
# Function dijkstraMatrix()-
# - choice of initial row i0 along the first column, where path starts
#   this changed function arguments and inital setup of dist[][]
# - added 'neighbor' number 3, to allow for moving up in the matrix
#
# No modifications needed for function nextVertex()
#
global MINIMUM
MINIMUM = 999999

def nextVertex(dist, size, unvisited):
#this function returns the next vertex
#which is still unvisited and which
#has a distance already set as smaller
#than MINIMUM.
    min=MINIMUM
    for i in range(size):
        for j in range(size):
            if unvisited[i][j] and dist[i][j]<min:
                min=dist[i][j]
                imin=i
                jmin=j
    return imin,jmin

def dijkstraMatrix(m, size,  i0):
#
#   For a selected starting point, returns a matrix 'dist'
# containing the minimum distances between this
# starting point and all the other points in the matrix.
#
#   So, to find the minimum distance to a point, just pick
# the value of the returned matrix 'dist' at that point. 
#
#   Note that the distance from the starting point to itself
# is its own value.
#
#   In this speficif problem82, the starting point is assumed
# to be anywhere in the first column of the matrix. The input
# 'i0' gives in which row the starting point is located. 
#
# http://en.wikipedia.org/wiki/Dijkstra's_algorithm
#
    # Initialisation of dist and unvisited,
    # 2 matrixes of size m.
    # . unvisited is filled with True and marks the vertices
    #   not yet computated by the algorithm
    # . dist is filled with MINIMUM and each element represents
    #   the distance of that element to the initial node.
    dist=[]
    unvisited=[]
    for i in range(size):
        dist.append([])
        unvisited.append([])
        for j in range(size):
            dist[i].append(MINIMUM)
            unvisited[i].append(True)

    #initial setup
    #this is the starting point of the path searching algorithm
    dist[i0][0]=m[i0][0]
    
    while sum([sum(_) for _ in unvisited]): 
        icur, jcur = nextVertex(dist, size, unvisited)
        unvisited[icur][jcur]=False
        # check neighbors - the if's below represent the pattern
        # and constraints of 'walking' through the matrix, i.e.,
        # for a current selected cell, the if's below describe the
        # possible connected nodes, or neighbors.
        #
        #1: icur+1,jcur - move down
        if icur<size-1:
            alt= dist[icur][jcur] + m[icur+1][jcur]
            if alt < dist[icur+1][jcur]:
                dist[icur+1][jcur] = alt
        #2: icur,jcur+1 - move left
        if jcur<size-1:
            alt= dist[icur][jcur] + m[icur][jcur+1]
            if alt < dist[icur][jcur+1]:
                dist[icur][jcur+1] = alt
        #3: icur-1, jcur - move up
        if icur>0:
            alt= dist[icur][jcur] + m[icur-1][jcur]
            if alt < dist[icur-1][jcur]:
                dist[icur-1][jcur] = alt
    return dist

### MAIN
'''
m=[
[131,	673,	234,	103,	18],
[201,	96,	342,	965,	150],
[630,	803,	746,	422,	111],
[537,	699,	497,	121,	956],
[805,	732,	524,	37,	331]]
'''

#reading the file:
filename="082_matrix.txt"
pfile=open(filename, 'r')
contents=pfile.readlines()
pfile.close()
m=[v.split(',') for v in contents]
for i in range(len(m)):
    for j in range(len(m)):
        m[i][j]=int(m[i][j])

size=len(m)
dists=MINIMUM
#the algorithm is generic and can start anywhere
#in the first column, so, just running it
#for all elements in the first column and
#picking up the minimum:
for i0 in range(size):
    print i0,  size
    ret=dijkstraMatrix(m,size, i0)
    ret=min([r[size-1] for r in ret])
    if ret<dists: dists=ret

print dists

#output
#260324

'''
to get the minimum path, you can work on the matrix dists
starting from the target cell, just go back following the
neighbor with the smalles value.
'''