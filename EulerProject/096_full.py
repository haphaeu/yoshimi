import copy
from time import time

one9={1,2,3,4,5,6,7,8,9}

def missing(n, i,j):
    # set with row
    row=one9-set(Games[n][i])
    # set with col
    col=one9-{Games[n][k][j] for k in range(9)}
    #set with box
    rw=(i/3)*3; cl=(j/3)*3
    box=one9-{Games[n][k][l] for k in range(rw,rw+3) for l in range(cl,cl+3)}
    #print row, col, box
    return set.intersection(row,col,box)

def check_game(n):
    # check rows
    for i in range(9):
        if not one9.issubset(set(Games[n][i])):
            return False
    #check cols
    for j in range(9):
        col={Games[n][k][j] for k in range(9)}
        if not one9.issubset(col):
            return False
    #check boxes
    for i in range(0,9,3):
        for j in range(0,9,3):
            box={Games[n][k][l] for k in range(i,i+3) for l in range(j,j+3)}
            if not one9.issubset(box):
                return False
    #is nothing is returned yet, all is fine:
    return True

#this is recursive, will guess until solved
def guess(n):
    for i in range(9):
        for j in range(9):
            if not Games[n][i][j]:
                tmp=missing(n,i,j)
                if len(tmp)==2:
                    backup=copy.deepcopy(Games[n])
                    Games[n][i][j]=tmp.pop()
                    if fillgrid(n):
                        return True
                    else:
                        if guess(n):
                            return True
                        else:
                            Games[n]=copy.deepcopy(backup)
                            Games[n][i][j]=tmp.pop()
                            if fillgrid(n):
                                return True
                            else:
                                if guess(n):
                                    return True
                                else:
                                    return False
    return False

def fillgrid(n):
    while fillgrid_onepass(n):
        pass
    if check_game(n):
        return True
    else:
        return False
def fillgrid_onepass(n):
    for i in range(9):
        for j in range(9):
            if not Games[n][i][j]:
                tmp=missing(n,i,j)
                if len(tmp)==1:
                    Games[n][i][j]=tmp.pop()
                    return True
                #chk neighbors
                rw1=3*(i/3)
                if rw1==i: rw1+=1
                rw2=rw1+1
                if rw2==i: rw2+=1
                cl1=3*(j/3)
                if cl1==j: cl1+=1
                cl2=cl1+1
                if cl2==j: cl2+=1
                row1=set(Games[n][rw1])-{0}
                row2=set(Games[n][rw2])-{0}
                col1={Games[n][k][cl1] for k in range(9)}-{0}
                col2={Games[n][k][cl2] for k in range(9)}-{0}

                tmp2=set.intersection(tmp,row1,row2,col1,col2)
                if len(tmp2)==1:
                    Games[n][i][j]=tmp2.pop()
                    return True
                    
                tmp2=set.intersection(tmp,row1,row2)
                if len(tmp2)==1 and Games[n][i][cl1] and Games[n][i][cl2]:
                    Games[n][i][j]=tmp2.pop()
                    return True
                    
                tmp2=set.intersection(tmp,col1,col2)
                if len(tmp2)==1 and Games[n][rw1][j] and Games[n][rw2][j]:
                    Games[n][i][j]=tmp2.pop()
                    return True
                    
                tmp2=set.intersection(tmp,row1,row2,col1)
                if len(tmp2)==1 and Games[n][i][cl2]:
                    Games[n][i][j]=tmp2.pop()
                    return True

                tmp2=set.intersection(tmp,row1,row2,col2)
                if len(tmp2)==1 and Games[n][i][cl1]:
                    Games[n][i][j]=tmp2.pop()
                    return True

                tmp2=set.intersection(tmp,col1,col2,row1)
                if len(tmp2)==1 and Games[n][rw2][j]:
                    Games[n][i][j]=tmp2.pop()
                    return True

                tmp2=set.intersection(tmp,col1,col2,row2)
                if len(tmp2)==1 and Games[n][rw1][j]:
                    Games[n][i][j]=tmp2.pop()
                    return True
    return False

# ### MAIN ###
t0=time()
pfile=open('sudoku.txt','r')
cont=pfile.readlines()
pfile.close
#convert file to an array of games
# M[n][i][j] so that one grid is M[n]
global Games
Games=[]
for n in range(50):
    game=[]
    for i in range(9):
        game.append([int(cont[1+10*n+i][k]) for k in range(9)])
    Games.append(game)

sumid=0
for n in range(50):
    #print " =========================== Grid %d ========================" % (n+1)
    #for _ in Games[n]: print _
    if not fillgrid(n):
        if not guess(n):
            print "!!! ERROR !!!"
    #print "solution:"
    #for _ in Games[n]: print _
    id=Games[n][0][0]*100+Games[n][0][1]*10+Games[n][0][2]
    sumid+=id
    #print id
print "=========="
print sumid
print "took %.3fs" % (time()-t0)

'''
24408+294= 24702
'''
