from fractions import Fraction
from fractions import gcd

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

# ### MAIN ###

TURNS=15
MXRED=(TURNS-1)/2
winPlays=[]
#generate initial conditions
for i in range(MXRED+1):
    nxt='b'*(TURNS-i)+'r'*i
    while nxt:
        winPlays.append(nxt)
        nxt=nextPermLexic(nxt)

#sum the probabilities of all wins
ProbTot = Fraction(0,1)
prob    = Fraction(1,1)
for play in winPlays:
    for i,disk in enumerate(play):
        if disk=='b':
            prob *= Fraction(1,i+2)
        else:
            prob *= Fraction(i+1,i+2)
    #print ProbTot, "+", prob,
    ProbTot = ProbTot + prob
    #print "=", ProbTot
    prob = Fraction(1,1)
print "Probability of winning is", ProbTot
print "Required fund", ProbTot.denominator/ProbTot.numerator
