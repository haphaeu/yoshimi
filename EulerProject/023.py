#returns the sum of the proper
#divisors of n
def sumProperDivisors(n):
    sum=1
    for i in range(2, (n>>1)+1): # n/2+1
        if n%i==0: 
            sum += i
    return sum

# list all abundant numbers up to N
# A number n is called deficient if the 
# sum of its proper divisors is less than 
# n and it is called abundant if this sum exceeds n.
def listAbundantNumbers(uptoN):
    ab=[]
    for i in range(12, uptoN):
        if i < sumProperDivisors(i): ab.append(i)
    return ab

limit=58123
numbers=[True]*limit
print "Creating list of all abundant numbers up to",  limit
abundantNumbers=listAbundantNumbers(limit)
noAb=len(abundantNumbers)
print noAb,  "abundant numbers found. Marking all possibilities of adding 2 of them together"
for a1 in abundantNumbers:
    for a2 in abundantNumbers:
        if a1+a2 <= limit:
            numbers[a1+a2-1] = False
print "And finally, calculating the sum of all number which cannot be written as the sum of 2 abundant numbers"
soma=0
for i in range(limit):
    if numbers[i]: soma+=i+1
print sum(numbers),  "numbers match criterion."
print "Their sum is",  soma
