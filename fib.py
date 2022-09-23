# Calculates Fibonacci numbers very efficiently
#
# https://r-knott.surrey.ac.uk/Fibonacci/fibtable.html
# In : f300 = 222232244629420445529739893461909967206666939096499764990979600  
# In : fib(300) - f300
# Out: 0

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    s = [0] * (n+1)
    s[0] = 0
    s[1] = 1
    for i in range(2, n+1):
        s[i] = s[i-1] + s[i-2]
    return s[n]
