import sys
from time import time
st=time()

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

#set to true to get a list of all terms found
#be aware that too much verbosity makes it run significantly slower
verbose=True
#set how many terms to skip when verbose
#set to 1 to show all terms
verbose_every= 10000

#First item in the sequence
perm="0123456789"
sz=len(perm)

#List to save all permutations
#Note that this algorithm is generic and will work also for a mix of
#numbers and letters.
#However, the pourpose of this exercise is sum all the first permutations
#of 0,1,2,3,4,5,6,7,8,9, so make sure you do the appropriate changes
#is you want to sort alphanumerical terms.
#!!!# DISABLED TO MAKE IT QUICKER
#!!!#permutations=[int(perm)]

#counter of how many permutations have been found
ct=1

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
            #see note before loop where this list is defined
            #!!!# DISABLED TO MAKE IT QUICKER
            #!!!#permutations.append(int(perm))
            ct+=1
            if verbose:
                if ct%verbose_every==0:
                    sys.stdout.write("Element %dth - %s\r" % (ct, perm))
            #criteria to finish search
            #increase or removed this to search all possible permutations
            if ct==1000000:
                if not verbose: print "Element %dth - %s\r" % (ct, perm)
                break
print "\nRun time is %.3fs" % (time()-st)

#output:
#Element 1000000th - 2783915460
#Run time is 4.8s
