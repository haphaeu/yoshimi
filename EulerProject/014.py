def nextCollatz(i):
    if i==1: return 1
    if i&1==0: # i is even
        return i>>1
    else:
        return (i<<1)+i+1

def seqCollatz(i):
    seq=[i]
    while True:
        nxt=nextCollatz(i)
        seq.append(nxt)
        if nxt==1: break
        i=nxt
    return seq

max=0
limit=int(1e6)
for i in range(1,limit):
    L= len(seqCollatz(i))
    if L>max:
        max=L
        print "Maximum length is %d for starting number %d" % (max, i)



    
