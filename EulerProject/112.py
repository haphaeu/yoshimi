#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 09:57:02 2018

@author: raf
"""

## slow string approach
def increasing(n):
    s = str(n)
    for i in range(len(s)-1):
        if int(s[i]) > int(s[i+1]):
            return False
    return True
        
def decreasing(n):
    s = str(n)
    for i in range(len(s)-1):
        if int(s[i]) < int(s[i+1]):
            return False
    return True

def bouncing2(n):
    return not (increasing(n) or decreasing(n))


# faster numeric approach (4x faster than string)
def bouncing(n):
    if (n < 101):
        return False
    
    direction = 0
    d = n % 10
    val = n // 10
    while val != 0:
        d2 = val % 10
        val //= 10
        if direction == 0:
            if d2 < d:
                direction = -1
            elif d2 > d:
                direction = 1
        if direction == -1:
            if d2 > d:
                return True
        elif direction == 1:
            if d2 < d:
                return True
        d = d2
    return False



# %%
n = 100
bounc_count = 0
while True:
    n += 1
    if bouncing(n):
        bounc_count += 1
    if bounc_count/n >= 0.99:
        break

print(n, bounc_count/n)
# 1_587_000 0.99
