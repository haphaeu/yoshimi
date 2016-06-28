#returns the sum of the proper
#divisors of n
def sumProperDivisors(n):
    sum=1
    for i in range(2, (n>>1)+1): # n/2+1
        if n%i==0: 
            sum += i
    return sum

sum=0
for a in range(2, 10000):
    b=sumProperDivisors(a)
    if b==a: 
        continue
    if sumProperDivisors(b)==a:
        sum+= a
        print a,  "+",  
print "=",  sum
