# Recursive implementation
# of the Fibonnacci sequence
def fib(n):
    if n==0:
        return 0L
    elif n==1:
        return 1L
    else:
        return long(fib(n-1)+fib(n-2))

add=0L
i=1L
while True:
    i += 1
    n = fib(i)
    if n >= 4000000L:
        break
    if n%2==0:
        add += n
print i, add
        
    
