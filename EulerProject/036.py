def isPalindromic(n):
    if int(str(n)[::-1])==n: return True
    return False

n10=1
tsum=0
while n10<=1e6:
	n02=int(bin(n10)[2:])
	if isPalindromic(n10) and isPalindromic(n02):
		tsum+=n10
	n10+=1
print tsum
#output
# 872187