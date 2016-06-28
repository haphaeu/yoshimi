from time import time

#Returns a list with the fractional digits of the inverse
#of an integer. If fraction has recurring cycle, will
#be marked with a '_' followed by the recurring cycle
# for example
# inv(4) = [2, 5]
# inv(6) = [1,6,'_',1]
# inv(7) = [1,4,2,8,5,7,'_',6]
# ###

def inv(d):
    if d==1: return [0]
    p=0
    idx_start=0
    answer=[]
    resto_p=1
    restos=[]
    while True:
        resto_p *= 10
        decim= resto_p/d
        #print decim,  resto
        answer.append(decim)
        resto_p = resto_p%d
        restos.append(resto_p)
        if resto_p==0: #finished division
            break
        try: #check if resto_p already ocurred
            idx=restos[:-1].index(resto_p,idx_start) #raise an error if resto_p doesnt exist
            if decim==answer[idx]:
                answer.pop()
                answer.append('_')
                answer.append(p-idx)
                break
            else:
                idx_start=idx+1
                raise
        except:
            pass
        p+=1
    return answer

# ### main
st=time()
#loop to find max recurrence cycle of 1/n for n<1000
max=0
maxi=0
for i in range(1,1001):
    a=inv(i)
    if a[-1]>max:
        max=a[-1]
        maxi=i
print "Recurrence cycle of %d has %d terms" % (maxi, max)
print "Run in %.3fs" % (time()-st)

    
    


#isso nao funciona pois o float, mesmo 128bits, nao 
#tem precisao suficiente...
##from math import log
##import numpy as np
##def rec(x):
##    rec=int(log(1/x, 10)+1)
##    while True:
##        exp=10**rec
##        x1=x*exp
##        x1i=int(x1)
##        x2=(x1-x1i)*exp
##        x2i=int(x2)
##        if x2i==0:
##            return 0
##        if x2i==x1i:
##            break
##        rec+=1
##    return rec
##
##maxrec=0
##xmaxrec=0
##for i in range(1, 1001):
##    reci= rec(np.float64(1./i))
##    if reci>maxrec:
##        maxrec=reci
##        xmaxrec=i
##print xmaxrec,  maxrec
