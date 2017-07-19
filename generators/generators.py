# -*- coding: utf-8 -*-
"""

Example of piping generators


One generator reads a file for changes and yields back new lines.
The next generator acts like a filter and only yields lines containing a pattern.


@author: raf
"""
import time

def grep(pattern, lines):
    print ("Looking for %s" % pattern)
    for line in lines:
        if pattern in line:
            yield line


def follow(file):
    with open(file) as pf:
        pf.seek(0, 2)
        while True:
            line = pf.readline()
            if line:
                yield line
            time.sleep(0.1)

for hit in grep('python', follow('log.txt')):
    print(hit)
