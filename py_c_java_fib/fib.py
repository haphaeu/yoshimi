# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 11:45:05 2017

@author: raf
"""
from time import time

def fib(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return fib(n-1)+fib(n-2)

n = 29
t0 = time()
res = fib(n)
et = (time() - t0)
print('fib({}) = {}'.format(n, res))
print('elapsed time = {} s'.format(et))
