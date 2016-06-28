def isPalindromic(n):
    if int(str(n)[::-1])==n: return True
    return False

maxPali=0
for n1 in range(999,100,-1):
    for n2 in range(999,100,-1):
        n=n1*n2
        if isPalindromic(n) and n>maxPali:
            maxPali=n
            print("maximum so far is", maxPali)
print("maximum found is", maxPali)
