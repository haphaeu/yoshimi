'''
Partition (number theory)
http://en.wikipedia.org/wiki/Integer_partition
'''

# Base sequence for pentagonal numbers
#http://en.wikipedia.org/wiki/Pentagonal_numbers
def BaseSeq(limit):
    bs = []
    for i in range(1,limit):
        bs.append(i)
        bs.append(-i)
    return bs

# List of the generalised pentagonal numbers
#http://en.wikipedia.org/wiki/Pentagonal_numbers
def GeneralPenta(BaseSeq):
    return [k*(3*k-1)/2 for k in BaseSeq]

#Formula for Partition of a number
#http://en.wikipedia.org/wiki/Integer_partition#Exact_formula
#
#This is a recursive approach, not good
#Too many calls will be made for the same number
#again and again...
def Partition(n):
    if n<0: return 0 # p(negative)=0
    if n==0: return 1 # p(0)=p(1)=1
    i=0
    p=0
    while g[i]<=n:
        p+=int((-1)**(k[i]-1)) * Partition(n-g[i])
        i+=1
    return p

#OK! This version does not use recursion
#It just starts from 1 and saves all the
#partitions of the smaller numbers
def Partition2(n):
    p=[1] #p(0)=1
    for m in range(1,n+1):
        pm=0
        i=0
        while g[i]<=m:
            pm+=int((-1)**(k[i]-1)) * p[m-g[i]]
            i+=1
        p.append(pm)
    return p[-1]
    
k = BaseSeq(20)
g = GeneralPenta(k)

#Check - should return the following:
'''
first element is p(0)
check=[1,1,2,3,5,7,11,15,22,30,42,56,77,101,135,176,231,
 297,385,490,627,792,1002,1255,1575,1958,2436,3010,
 3718,4565,5604,6842,8349,10143,12310,14883,17977,
 21637,26015,31185,37338,44583,53174,63261,75175,
 89134,105558,124754,147273,173525]
'''

print Partition2(100)
# p(100)=190569292
# Note that the real answer of the problem 76 is p(100)-1
#so, 190569291

    
