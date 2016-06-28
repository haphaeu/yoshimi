"""
Project Euler Problem 206
=========================

Find the unique positive integer whose square has the form
1_2_3_4_5_6_7_8_9_0, where each _ is a single digit.
"""
from math import sqrt
upper = int(sqrt(1929394959697989990) / 10) * 10
lower = int(sqrt(1020304050607080900))
#square ends with zero => num ends with zero => step of 10
for i in xrange(upper, lower, -10):
    if str(i*i)[0::2] == '1234567890': break
print i
#1389019170