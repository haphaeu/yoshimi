from numpy import zeros

# Fill a matrix like this:
#   21 22 23 24 25
#   20  7  8  9 10
#   19  6  1  2 11
#   18  5  4  3 12
#   17 16 15 14 13
def spiral(n):
    #make sure n is odd
    if n&1==0: return []
    M=zeros((n, n))
    r=c=n/2
    dirs_rc=[(0, 1), (1, 0), (0, -1), (-1, 0)]
    dirn=0
    ct=1
    M[r][c]=ct
    for i in range(1, n):
        for k in range(2):
            dir=dirn%4
            for j in range(1, i+1):
                r += dirs_rc[dir][0]
                c += dirs_rc[dir][1]
                ct+=1
                M[r][c]=ct
            dirn +=1
    #fill top most row
    for i in range(1, n):
        ct += 1
        M[0][i]=ct
    return M

#sum the diagonals of a matrix
def sumDiagonal(M):
    n=len(M)
    #check if len is odd
    if n&1==0: return 0
    #start with negative ofthe central element
    #as it will be accounted for twice in the loop
    soma= -M[n/2][n/2]
    for i in range(n):
        soma += M[i][i] + M[i][n-i-1]
    return soma

# ### main ###
print sumDiagonal(spiral(1001))
