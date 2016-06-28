# # # #
# Project Euler - Problem 62
#
# The cube, 41063625 (345^3), can be permuted to produce two other cubes:
# 56623104 (384^3) and 66430125 (405^3). In fact, 41063625 is the smallest cube
# which has exactly three permutations of its digits which are also cube.
#
# Find the smallest cube for which exactly five permutations of its digits
# are cube.
# # # #

def isCube(x):
# returns True if x is a cube
# returns False otherwise
    tmp=1+int(x**0.333333333333333333333333)
    if x==tmp**3: return True
    return False

def nextPermLexic(perm):
# ###########################################################################
#The following algorithm generates the next permutation lexicographically
#after a given permutation. It changes the given permutation in-place.
#1- Find the largest index k such that a[k] < a[k + 1]. If no such index
#   exists, the permutation is the last permutation.
#2- Find the largest index l such that a[k] < a[l]. Since k + 1 is such
#   an index, l is well defined and satisfies k < l.
#3- Swap a[k] with a[l].
#4- Reverse the sequence from a[k + 1] up to and including the final
#   element a[n].
#
# Written by R.Rossi, 26th/Oct/2011
#
# Reference:
# http://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
# ###########################################################################
    #will return the next permutation
    #after 'perm' in lexicographic order
    sz=len(perm)
    #Step 1: find largest k st a[k]<a[k+1]
    k= -666
    for i in range(sz-2,-1,-1):
        if perm[i] < perm[i+1]:
            k=i
            break
    if k==-666:
        #print "\nAchieved last permutation in lexicographic order"
        return []
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
            return []
        else:
            #step 3: Swap a[k] with a[l]
            tmp=perm[0:k] + perm[l] + perm[k+1:l] + perm[k] + perm[l+1:]
            #step 4: reverse a[k+1:]
            tmp2=tmp[0:k+1] + tmp[-1:k:-1]
            #done.
            #save as perm
            nextPerm=tmp2
    return nextPerm

# ### main
n=1000
limit = 10000
while n<limit:
    count=0
    nc=n**3
    while not nc ==[]:
        nc=long(nc)
        if isCube(nc):
            count+=1
        nc=nextPermLexic(str(nc))
    if count==5:
        print n**3
    n+=1
    if not n%(100):
        print 100.*n/limit

# output
# 127035954683
#
# for n=5064
# other cubic permutations are
# 352045367981
# 373559126408
# 569310543872
# 589323567104
















    
