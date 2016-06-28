#class for fraction
# n / ( sqrt(N) - b )
class myFrac():
    def __init__(self,N,n,b,I):
        self.N=N
        self.n=n
        self.b=b
        self.I=I

# this function does the job to
# find the next continued fraction
# by using algebra
def nextFrac(f):
    I=int(f.n/(f.N**0.5-f.b))
    n=(f.N-f.b**2)/f.n
    b=-((f.n+I*f.b)*f.b-I*f.N)/f.n
    return myFrac(f.N,n,b,I)

def getSeq(N):
    a=int(N**0.5)
    chk=[]
    seq=[a]
    f=myFrac(N,1,a,0)
    while True:
        f=nextFrac(f)
        t=tuple([f.n,f.b])
        if t in chk:
            break
        seq.append(f.I)
        chk.append(t)
    return seq

# ### main ###
from time import time
st=time()
ct=0
for i in range(2,10001):
    if int(i**0.5)==i**0.5: continue
    if len(getSeq(i))%2==0: #if is even => period is odd
        ct+=1
print(ct)
print(time()-st)
# output 1332


