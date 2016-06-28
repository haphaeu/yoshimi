''' Problem 86
A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3,
and a fly, F, sits in the opposite corner. By travelling on the surfaces
of the room the shortest "straight line" distance from S to F is 10 and
the path is shown on the diagram.

However, there are up to three "shortest" path candidates for any given
cuboid and the shortest route doesn't always have integer length.

By considering all cuboid rooms with integer dimensions, up to a maximum
size of M by M by M, there are exactly 2060 cuboids for which the shortest
route has integer length when M=100, and this is the least value of M for
which the number of solutions first exceeds two thousand; the number of
solutions is 1975 when M=99.

Find the least value of M such that the number of solutions first exceeds
one million.


---
Solution:

taking a cube of size (x y z) with x <= y <= z,
the shortest path will always be
path(x,y,z) = sqrt( (x+y)^2 + z^2 )

so the result for any M is counting all the different instances for x y z
satisfying 1 <= x <= y <= z <= M 
where path(x,y,z) is an integer

there are a lot of combinations of x and y where path
computes essentially the same value, so to save time, j = x + y can be
substituted and the results multiplied by the number of combinations
of x and y that can make j

sum = 0
loop for i from 1 to M
  loop for j from 2 to 2*i
    if path_is_integral (i j) then sum = sum + (combinations i j)

where combinations (i j) is the number of ways to choose x and y
satisfying 1 <= x <= y <= i and x + y = j

the number of combinations can be expressed as
int(j/2) - max(j-1,1) + 1

****

Note: there might be some other fancy math solution involving
Pythagorean triples, coprimes, totient... check:
http://en.wikipedia.org/wiki/Integer_triangle#Pythagorean_triangles
http://en.wikipedia.org/wiki/Coprime
http://en.wikipedia.org/wiki/Coprime#Generating_all_coprime_pairs

'''

'''runs in few seconds'''
M=5000 #upper limit for checking
ct=0
for i in range(1,M+1):
    for j in range(2,2*i+1):
        path = (j**2+i**2)**0.5
        if path==int(path):             #number of ways to choose x and y satisfying
            ct+=int(j/2)-max(j-i,1)+1   # 1 <= x <= y <= i and x + y = j
    if ct>1e6:
        print i, ct
        break

'''
# old, works, but totally brute force one
# ==> takes 5-10min to run            
M=10
ct=0
for i in range(1,M+1):
    for j in range(i,M+1):
        for k in range(j,M+1):
            path = (k**2+(i+j)**2)**0.5 #always k>j>i
            if path==int(path):
                print i,j+k
                ct+=1
print ct
'''
