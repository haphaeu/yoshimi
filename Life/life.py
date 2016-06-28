from random import randint
import time
import os
import sys

#initialise (random) the field to run life
def InitialiseField(dim):
    init_life=[]
    for i in range(dim):
        init_life.append([])
        for j in range(dim):
            init_life[i].append(randint(0,1))
    return init_life

#print the field of life to stdout
def PrintFieldScreen(life,dim):
    os.system('cls')
    for i in range(dim):
        for j in range(dim):
            if life[i][j]==1: sys.stdout.write('#')
            if life[i][j]==0: sys.stdout.write('.')
        sys.stdout.write('\n')
#print the field of life to file
def PrintFieldFile(pfile, life,dim):
    for i in range(dim):
        for j in range(dim):
            if life[i][j]==1: pfile.write('#')
            if life[i][j]==0: pfile.write('.')
        pfile.write('\n')
#generate next generation
def ProgressLife(currGen,dim):
    MIN_NEIGHBORS=3
    MAX_NEIGHBORS=4
    nextGen=[]
    for i in range(dim):
        nextGen.append(currGen[i][:])
    for i in range(dim):
        for j in range(dim):
            if i==0: io=0; ie=1
            if i>0: io=i-1; ie=i+1
            if i==dim-1:io=i-1;ie=i
            if j==0: jo=0; je=1
            if j>0: jo=j-1; je=j+1
            if j==dim-1:jo=j-1;je=j
            neighbors=0
            for ii in range(io,ie+1):
                for jj in range(jo,je+1):
                    if ii==jj: continue
                    neighbors += currGen[ii][jj]
            if neighbors<MIN_NEIGHBORS or neighbors>MAX_NEIGHBORS:
                nextGen[i][j]=0
            else:
                nextGen[i][j]=1
    #copy back this shit
    currGen=[]
    for i in range(dim):
        currGen.append(nextGen[i][:])
    return currGen

#main program
if len(sys.argv)==3:
    if sys.argv[2]=="screen" or sys.argv[2]=="file":
        DIM=int(sys.argv[1])
        life=InitialiseField(DIM)
        gen=0
        while True:
            if sys.argv[2]=="file":
                #open file to save field life
                pFile=open(format(gen,"05")+".txt",'w')
                PrintFieldFile(pFile,life,DIM)
                pFile.close()
            else:
                time.sleep(0.1)
                #print field life in screen
                PrintFieldScreen(life,DIM)
            #calculate next generation
            life=ProgressLife(life,DIM)
            gen+=1
            #print progress in stdout
            sys.stdout.write("Generation %i\r" % gen)
else:
    print "Use: life DIM [screen; file]"