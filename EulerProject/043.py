def checkProperty(n):
    strn=str(n)
    d02=int(strn[1:4])
    d03=int(strn[2:5])
    d05=int(strn[3:6])
    d07=int(strn[4:7])
    d11=int(strn[5:8])
    d13=int(strn[6:9])
    d17=int(strn[7:10])
    if d02%2==0 and d03%3==0 and d05%5==0 and \
       d07%7==0 and d11%11==0 and d13%13==0 and d17%17==0:
           return True
    return False

def permutations(first):
    perm=str(first)
    sz=len(perm)
    #list to save al permutations
    permutations=[first]
    #start loop
    while True:
        #Step 1: find largest k st a[k]<a[k+1]
        k= -666
        for i in range(sz-2,-1,-1):
            if perm[i] < perm[i+1]:
                k=i
                break
        if k==-666:
            print "\nAchieved last permutation in lexicographic order"
            break
        else:
            #Step 2: find largest index l such that a[k] < a[l]
            l=-666
            if k==sz-2:
                l=k+1
            else:
                for i in range(sz-1,k,-1):
                    if perm[k] < perm[i]:
                        l=i
                        break
            if l==-666:
                print "\nError! Oh my god, what to do?"
                break
            else:
                #step 3: Swap a[k] with a[l]
                tmp=perm[0:k] + perm[l] + perm[k+1:l] + perm[k] + perm[l+1:]
                #step 4: reverse a[k+1:]
                tmp2=tmp[0:k+1] + tmp[-1:k:-1]
                #done.
                #save as perm
                perm=tmp2
                #add element to list
                permutations.append(int(perm))
    return permutations
from time import time
st=time()
first=1023456789
pandigs=permutations(first)
print sum([p for p in pandigs if checkProperty(p)])
print "took %.3fs" % (time()-st)
#output
#16695334890
#took 35.350s
