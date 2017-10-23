# -*- coding: utf-8 -*-
"""
This file launches a subprocess and captures its output on the run.

Created on Wed Oct 18 14:24:49 2017
@author: rarossi
"""
import sys
import subprocess

cmd = r'C:\Users\rarossi\Anaconda3\python.exe stream.py 6'

with open('out.txt', 'w') as pf:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    for linebyte in iter(p.stdout.readline, b''):
        line = linebyte.decode().replace('\r\n', '\n')
        sys.stdout.write(line)
        pf.write(line)
