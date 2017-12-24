# -*- coding: utf-8 -*-
"""
This script just prints an endless stream of dummy data to stdout

Created on Wed Oct 18 14:17:54 2017
@author: rarossi
"""
import sys
import time
import random


def run(n):
    for j in range(n):  # output n lines
        sz = random.randint(5, 30)  # each line has 5 to 30 characters
        line = ''
        for i in range(sz):
            line += str(random.randint(0, 9))  # characters are number from 0 to 9
        sys.stdout.write(line + '\n')
        sys.stdout.flush()
        time.sleep(random.random())


if __name__ == '__main__':
    n = 5
    if len(sys.argv) > 1:
        if sys.argv[1].isnumeric():
            n = int(sys.argv[1])
    run(n)
