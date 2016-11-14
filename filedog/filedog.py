# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:25:01 2016

@author: raf
"""
import time
file = open('file.txt')
while True:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        print(line, end='')
