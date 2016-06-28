"""
Project Euler Problem 4
=======================

A palindromic number reads the same both ways. The largest palindrome made
from the product of two 2-digit numbers is 9009 = 91 * 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""


def isPalindromic(n):
    if int(str(n)[::-1])==n: return True
    return False

maxPali=0
for n1 in range(999,100,-1):
    for n2 in range(999,100,-1):
        n=n1*n2
        if isPalindromic(n) and n>maxPali:
            maxPali=n
print maxPali
