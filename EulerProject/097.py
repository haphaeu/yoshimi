# project euler problem 97

n=2
e=7830457
d=10
lim=10**d
num=1
for i in range(1,e+1):
    num*=n
    if num>lim:
        num-=lim*(num/lim)
print((num*28433+1)%10000000000)
# 8739992577
