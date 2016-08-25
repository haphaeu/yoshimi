# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 12:23:41 2015

@author: rarossi
"""

x = 1 # seed
p1 = 16807 
N = 2**31-1
count = 0
while count<100:
    x = p1*x % N
    print x
    count+=1

