'''
Project Euler - Problem 56

Considering natural numbers in the form a**b, a,b<100,
what is the maximum digital sum?
'''

def digSum(val):
    s=0
    for d in str(val):
        s+=int(d)
    return s

ai=bi=90 #let's start high...
af=bf=99
maxSum=0
for a in range(ai,af+1):
    for b in range(bi,bf+1):
        dSum=digSum(a**b)
        if dSum>maxSum:
            maxSum=dSum
print "Max digital sum is", maxSum

#output
#Max digital sum is 972
