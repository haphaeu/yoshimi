# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 15:57:28 2017

@author: rarossi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 15:05:22 2017

@author: rarossi
"""

import multiprocessing as mp
import time
import random


def do_something(n):
    return n

def run_something(q, r):
    while not q.empty():
        n = q.get()
        retval = do_something(n)
        r.put(retval)

def serial(sample):
    for s in sample:
        print(do_something(s))

def parallel(sample, num_threads):
    q = mp.Queue()
    r = mp.Queue()

    for s in sample:
        q.put(s)

    procs = set()
    for i in range(num_threads):
        p = mp.Process(target=run_something, args=(q, r, ))
        procs.add(p)
        p.start()

    for p in procs:
        p.join()

    while not r.empty():
        print(r.get())

if __name__ == '__main__':
    size = 3000
    order = 3
    sample = [1, 2, 3]

    serial(sample)
    parallel(sample, 2)



