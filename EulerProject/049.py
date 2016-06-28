''' Problem 49
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases
by 3330, is unusual in two ways:
(i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.
There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes,
exhibiting this property, but there is one other 4-digit increasing sequence.
What 12-digit number do you form by concatenating the three terms in this
sequence?
'''
def isPrime(n):
    #4-digit, just need to check primes < sqrt 9999
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,
              43,47,53,59,61,71,73,79,83,89,97]:
        if n%p==0: return False
    return True
def isPermutation(n1, n2):
    a=[c for c in str(n1)]
    b=[c for c in str(n2)]
    a.sort()
    b.sort()
    return a==b

### MAIN ###

#build up a set with all 4-digit primes
prime4d = {n for n in range(1000,10000) if isPrime(n)}

#brute force to find permutations

#max step of aritimethic seq:
pa=(9999-1000)/2
#working backwards:
for stp in range(pa,1,-1):
    for x1 in prime4d:
        x2=x1+stp
        x3=x2+stp
        if x2>9999 or x3>9999: continue
        if x2 in prime4d and x3 in prime4d:
               if isPermutation(x1,x2) and isPermutation(x2,x3):
                      print x1,x2,x3
'''
output:
2969 6299 9629
1487 4817 8147
'''
