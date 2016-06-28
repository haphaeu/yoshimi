"""
Project Euler - Problem 40

An irrational decimal fraction is created by concatenating the positive
integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the
following expression.

d1 x d10 x d100 x d1000 x d10000 x d100000 x d1000000
"""
#how many integers to get 1e6 digits:
nTerms=(1000000 - (8.*1 + 89*2 + 899*3 + 8999*4 + 89999*5))/6 + 99999
frac=''
for i in range(1,nTerms):
	frac+=str(i)
print int(frac[0])*int(frac[9])*int(frac[99])*int(frac[999])*int(frac[9999])*int(frac[99999])*int(frac[999999])
#output
#210