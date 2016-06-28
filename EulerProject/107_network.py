cont=[_.split(',') for _ in open('network.txt','r')]
network=[]
for rw in cont:
    _=[]
    for n in rw:
        try:
            v=int(n)
        except:
            v=0
        _.append(v)
    network.append(_)

'''
#          A  B   C   D   E   F   G
network=[[ 0, 16, 12, 21,  0,  0,  0],#A
         [16,  0,  0, 17, 20,  0,  0],#B
         [12,  0,  0, 28,  0, 31,  0],#C
         [21, 17, 28,  0, 18, 19, 23],#D
         [ 0, 20,  0, 18,  0,  0, 11],#E
         [ 0,  0, 31, 19,  0,  0, 27],#F
         [ 0,  0,  0, 23, 11, 27,  0]]#G
'''

SZ=len(network)

#check if all nodes in the 
#network are connected
def connected():
    visited=[False]*SZ
    visit(0,visited)
    return all(visited)
def visit(node,visited):
    if not visited[node]:
        visited[node]=True
        for n in range(SZ):
            if not node==n and network[node][n]:
                visit(n,visited)

def optimise_network():
    forbid_nk=set()
    mudou=True
    ct=0
    while mudou:
        mudou=False
        mx=0
        for n in range(SZ):
            for k in range(n+1,SZ):
                if network[n][k]>mx and (n,k) not in forbid_nk:
                    mx=network[n][k]
                    nx=n
                    kx=k
        #try to remove max
        if mx:
            network[nx][kx]=0
            network[kx][nx]=0
            if not connected():
                network[nx][kx]=mx
                network[kx][nx]=mx
                forbid_nk.add((nx,kx))
            mudou=True
        if not ct%100:
           print sum([sum(_) for _ in network])/2
        ct+=1
# ### MAIN ###

weight0=sum([sum(_) for _ in network])/2
print weight0
optimise_network()
weight1=sum([sum(_) for _ in network])/2
saving=weight0-weight1
print saving

