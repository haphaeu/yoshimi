# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 14:51:33 2014

@author: rarossi
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def readdraw(file):
    """ Read a text file with the vertices coordinates in 3D 
    followed by the edges connectivity.
    
    Returns a list [vertices, edges].
    
    Format of the file to be read:
    First, list all vertices. Each coordinate separated by 
    any white space and one vertex per line.
    Then, right after the list of vertices, list all the edges 
    connectivity fromVertex toVertex, separated by any white
    space, one edge per line.
    
    Example of format for a unit cube:
    0. 0. 0.
    1. 0. 0.
    1. 1. 0.
    0. 1. 0.
    0. 0. 1.
    1. 0. 1.
    1. 1. 1.
    0. 1. 0.
    1 2
    2 3
    3 4
    4 1
    5 6
    6 7
    7 8
    8 5
    1 5
    2 6
    3 7
    4 8
    """
    p = open(file, 'r')
    cont = p.readlines()
    p.close()
    verts=[]
    edges=[]
    for c in cont:
        tmp = [float(_) for _ in c.split()]
        if len(tmp)==3: verts.append(tmp)
        if len(tmp)==2: edges.append([int(i) for i in tmp])
    return [verts, edges]

files = ['poly1.txt','poly2.txt','poly3.txt','poly4.txt']    
shift = [-6,0,0,0]
color=  ['red', 'orange', 'blue', 'brown']


fig = plt.figure()
ax = fig.gca(projection='3d')
for i, f in enumerate(files):
    print (f)
    verts, edges = readdraw(f)    
    for e in edges:
        ax.plot([verts[e[0]-1][0],verts[e[1]-1][0]],
                [verts[e[0]-1][1],verts[e[1]-1][1]],
                [verts[e[0]-1][2]+shift[i],verts[e[1]-1][2]+shift[i]],
                color[i])
plt.show()

