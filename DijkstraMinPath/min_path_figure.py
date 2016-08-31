# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:31:04 2016

@author: rarossi
"""

from matplotlib import pylab
import numpy as np
import DijkstraMinPath
from DijkstraMinPath import Edge, Vertex


def ascii_print(m):
    for rw in m:
        for p in rw:
            print('#' if p > 1 else '.', end='')
        print('')





def save_fig(fig, min_path, width, name='minpath.bmp'):
    for p in min_path:
        i, j = div(p, width)
        fig[i][j] = np.array([255, 0, 0], dtype=np.uint8)
    pylab.imshow(fig)


# fig = pylab.imread('beta.bmp')
fig = pylab.imread('beta_3x4.bmp')
# fig = pylab.imread('beta_75x100.bmp')
height, width = len(fig), len(fig[0])

matrix = np.ones((height, width), dtype=int)

# Converts the image into a matrix
# Anything darker than medium grey will be a "wall"
# The rest is "walkable" area
for i in range(height):
    for j in range(width):
        matrix[i][j] = int(99) if fig[i][j][0] < 128 else 1

# Set-up all the edges
edges = list()
for i in range(height):
    for j in range(width):
        if i < height-1:
            edges.append(Edge(vid(i, j, width), vid(i+1, j, width), max(matrix[i][j],
                                                                        matrix[i+1][j])))
        if j < width-1:
            edges.append(Edge(vid(i, j, width), vid(i, j+1, width), max(matrix[i][j],
                                                                        matrix[i][j+1])))

num_vertex = height*width
vertexes = [Vertex(_, DijkstraMinPath.MINIMUM, True, 0, div(_, width)) for _ in range(num_vertex)]

for i in range(len(edges)):
        vertexes[edges[i].v1].edges.append(i)
        vertexes[edges[i].v1].otherVert.append(edges[i].v2)
        vertexes[edges[i].v2].edges.append(i)
        vertexes[edges[i].v2].otherVert.append(edges[i].v1)

# calculate minimum distances to each vertex
init_vertex = vid(0, 0, width)
# init_vertex = vid(1, 0, width)
DijkstraMinPath.dijkstraGraph(vertexes, edges, init_vertex, verbose=True)

# get the minimum path from InitialVertex to TargetVertex
target_vertex = vid(height-1, width-1, width)
# target_vertex = vid(0, 2, width)
n = target_vertex
MinPath = [n]
i, iter_limit = 0, 999
while n and i < iter_limit:
    n = vertexes[n].nearest
    MinPath.append(n)
    i += 1
if i == iter_limit:
    print('Warning: reached maximum number of iteractions.')
MinPath.reverse()

# show results
print("Minimum distance from vertex", init_vertex, "to vertex ", end='')
print(target_vertex, "is", vertexes[target_vertex].distance)
print("The path for minimum distance is through vertexes:")
print(MinPath)

save_fig(fig, MinPath, width)


came_from, cost_so_far = DijkstraMinPath.a_star(edges, vertexes, vertexes[0], vertexes[2], True)
