def dagTriang(m, size):
    dist=[]
    for i in range(size):
        dist.append([])
        for j in range(i+1):
                dist[i].append(0)

    #initial setup
    dist[0][0]=m[0][0]
    for icur in range(size):
        for jcur in range(icur+1):
            try:
                #print icur, jcur
                #check neighbors
                #1: left
                if icur<size-1:
                    alt= dist[icur][jcur] + m[icur+1][jcur]
                    if alt > dist[icur+1][jcur]:
                        dist[icur+1][jcur] = alt
                #2: right
                    if jcur<=icur:
                        alt= dist[icur][jcur] + m[icur+1][jcur+1]
                        if alt > dist[icur+1][jcur+1]:
                            dist[icur+1][jcur+1] = alt
            except: #for debugging reasons
                print "error"
                print dist
                raise
    return dist

# ### MAIN

url="http://projecteuler.net/project/triangle.txt"
import urllib
page=urllib.urlopen(url)
contents=page.read()
contents=contents.split('\r\n')
contents.pop()
m=[v.split(' ') for v in contents]
for i in range(len(m)):
    for j in range(i+1):
        m[i][j]=int(m[i][j])
"""
m=[[3],[7,4],[2,4,6],[8,5,9,3]]

m=[[75],
[95, 64],
[17, 47, 82],
[18, 35, 87, 10],
[20, 04, 82, 47, 65],
[19, 01, 23, 75, 03, 34],
[88, 02, 77, 73, 07, 63, 67],
[99, 65, 04, 28, 06, 16, 70, 92],
[41, 41, 26, 56, 83, 40, 80, 70, 33],
[41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
[53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
[70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
[91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
[63, 66, 04, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
[04, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60, 04, 23]]
"""
size=len(m)
dists=dagTriang(m,size)
print max(dists[-1])

#output
#7273