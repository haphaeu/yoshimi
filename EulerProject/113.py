#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

https://projecteuler.net/problem=113Created on Sun Jul 29 09:57:02 2018


cheat:
https://rafal.io/posts/project-euler-113-nonbouncy-numbers.html

@author: raf
"""

f_inc_memo = dict()
def f_inc(i, k):
    global f_inc_memo
    if (i, k) in f_inc_memo:
        return f_inc_memo[(i, k)]
    
    if i == 1:
        return 1
    
    sm = 0
    for j in range(k, 10):
        sm += f_inc(i-1, j)
    
    f_inc_memo[(i, k)] = sm
    return sm

f_dec_memo = dict()
def f_dec(i, k):
    global f_dec_memo 
    if (i, k) in f_dec_memo:
        return f_dec_memo[(i, k)]
    
    if i == 1:
        return 1
    
    sm = 0
    for j in range(0, k+1):
        sm += f_dec(i-1, j)
        
    f_dec_memo[(i, k)] = sm
    return sm

def tot(n):
    sm = 0
    for i in range(1, n+1):
        for k in range(1, 10):
            sm += f_inc(i, k) + f_dec(i, k)
    return sm - 9*n
            

print(tot(100))
# 51161058134250