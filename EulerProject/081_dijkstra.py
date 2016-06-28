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

!!!
This code implements the Dijkstra algorithm for minimum path finder.
"""
global MINIMUM
MINIMUM = 999999

def nextVertex(dist, size, unvisited):
    min=MINIMUM
    for i in range(size):
        for j in range(size):
            if unvisited[i][j] and dist[i][j]<min:
                min=dist[i][j]
                imin=i
                jmin=j
    return imin,jmin

def dijkstraMatrix(m, size):
    dist=[]
    unvisited=[]
    for i in range(size):
        dist.append([])
        unvisited.append([])
        for j in range(size):
            dist[i].append(MINIMUM)
            unvisited[i].append(True)

    #initial setup
    dist[0][0]=m[0][0]
    while sum([sum(_) for _ in unvisited]): 
        icur, jcur = nextVertex(dist, size, unvisited)
        #print icur, jcur
        unvisited[icur][jcur]=False
        #check neighbors
        #1: icur+1,jcur
        if icur<size-1:
            alt= dist[icur][jcur] + m[icur+1][jcur]
            if alt < dist[icur+1][jcur]:
                dist[icur+1][jcur] = alt
        #2: icur,jcur+1
        if jcur<size-1:
            alt= dist[icur][jcur] + m[icur][jcur+1]
            if alt < dist[icur][jcur+1]:
                dist[icur][jcur+1] = alt
    return dist


                
# ### MAIN
"""
m=[[131,	673,	234,	103,	18],
[201,	96,	342,	965,	150],
[630,	803,	746,	422,	111],
[537,	699,	497,	121,	956],
[805,	732,	524,	37,	331]]
"""

url="http://projecteuler.net/project/matrix.txt"
import urllib
page=urllib.urlopen(url)
contents=page.read()
contents=contents.split('\n')
contents.pop()
m=[v.split(',') for v in contents]
for i in range(len(m)):
    for j in range(len(m)):
        m[i][j]=int(m[i][j])

size=len(m)
dists=dijkstraMatrix(m,size)
print dists[-1][-1]
