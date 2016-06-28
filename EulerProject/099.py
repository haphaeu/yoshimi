#project euler problem 99
#
# given n1**e1 and n2**e2, which one is larger?
#     n1**e1 > n2**e2
# e1*log(n1) > e2*log(n2)
#
from math import log
cont=[_.split(',') for _ in open("base_exp.txt",'r').readlines()]
base_exp=[]
for i in range(1000):
    base_exp.append([i, int(cont[i][0]), int(cont[i][1])])
del cont

max_i=0
for i in range(1,1000):
    if base_exp[max_i][2]*log(base_exp[max_i][1]) < base_exp[i][2]*log(base_exp[i][1]):
        max_i=i
print max_i+1
# 709
