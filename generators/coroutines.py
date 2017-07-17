# -*- coding: utf-8 -*-
"""

See generators.py

This makes the same job as generators.py but using coroutines.

Meaning that things are pushed downstream rather than pulled upstream.

@author: raf
"""
import time

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start

@coroutine
def grep(pattern, target):
    print("Looking for %s" % pattern)
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


def follow(file, target):
    with open(file) as pf:
        pf.seek(0, 2)
        while True:
            line = pf.readline()
            if line:
                target.send(line)
            time.sleep(0.1)

@coroutine
def showline():
    while True:
        line = (yield)
        print(line)

follow('log.txt', grep('python', showline()))
