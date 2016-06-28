# ###
# Note: this is too slow! See 067_dag.py
# ###

global COUNTER
COUNTER=0

def sumpath(triangle, soma, row, col):
    global COUNTER
    verbterms=False
    diff=30
    s=len(triangle)
    for c in range(row,s):
        a0=triang[c][col]
        a1=triang[c][col+1]
        if c<50 and abs(a0-a1) < diff:
            b0=sumpath(triangle, soma+a0, c+1, col)
            b1=sumpath(triangle, soma+a1, c+1, col+1)
            if b0>b1:
                soma += a0
            else:
                soma += a1
                col += 1
        elif a1>a0:
            col += 1
            soma += a1
            if verbterms: print a1,
        else: # a0>a1
            soma += a0
            if verbterms: print a0,
    COUNTER += 1
    if COUNTER%100000==0: print COUNTER, row, col, soma
    return soma

p=open('067.txt','r')
#p=open('018.txt','r')
tmp=p.read()
p.close()
tmp=[t.split(' ') for t in tmp.split('\n')]
triang=[]
for line in tmp:
    triang.append([int(i) for i in line])
del tmp

s=len(triang)

# o triangulo tem 100 linhas, a cada passo
# existem 2 possibilidades, ou seja,
# 2**(100-1) = balaios!!!
# impossivel na forca bruta...

print sumpath(triang, triang[0][0], 1, 0)
#show path
#print "\nPath with max sum:",
#for i in range(0,s):
#    print triang[i][path[i]],
#print "\nThe sum is %d" % soma
