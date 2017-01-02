# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 15:05:22 2017

@author: rarossi
"""

import multiprocessing as mp
import time
import random


def do_something_dummy(n):
    i = 0
    while i < n:
        a = i ** 0.497
        i += 1


def worker(q):
    while not q.empty():
        n = q.get()
        do_something_dummy(n)


def run_serial(sample):
    for s in sample:
        do_something_dummy(s)


def run_parallel(sample, num_threads):
    q = mp.Queue()
    for s in sample:
        q.put(s)

    procs = set()
    for i in range(num_threads):
        p = mp.Process(target=worker, args=(q,))
        procs.add(p)
        p.start()

    for p in procs:
        p.join()


if __name__ == '__main__':
    size = 3000
    order = 4
    sample = [random.randint(10**order, 10**(order+1)-1) for _ in range(size)]

    t0 = time.time()
    run_serial(sample)
    t1 = time.time()
    ts = t1 - t0
    print('run_serial %.3f ms' % ts)

    t0 = time.time()
    run_parallel(sample, 1)
    t1 = time.time()
    tp1 = t1 - t0
    print('mp 1 thread %.3f s' % tp1)

    t0 = time.time()
    run_parallel(sample, 2)
    t1 = time.time()
    tp2 = t1 - t0
    print('mp 2 thread %.3f s' % tp2)

    t0 = time.time()
    run_parallel(sample, 4)
    t1 = time.time()
    tp4 = t1 - t0
    print('mp 4 thread %.3f s' % tp4)

    t0 = time.time()
    run_parallel(sample, 8)
    t1 = time.time()
    tp8 = t1 - t0
    print('mp 8 thread %.3f s' % tp8)

    t0 = time.time()
    run_parallel(sample, 16)
    t1 = time.time()
    tp16 = t1 - t0
    print('mp 16 thread %.3f s' % tp16)

    t0 = time.time()
    run_parallel(sample, 32)
    t1 = time.time()
    tp32 = t1 - t0
    print('mp 32 thread %.3f s' % tp32)

'''
Input
=====
size = 3000
order = 4

Output
======
run_serial 49.866 ms
mp 1 thread 50.183 s
mp 2 thread 25.973 s
mp 4 thread 13.307 s
mp 8 thread 7.192 s
mp 16 thread 4.509 s
mp 32 thread 4.587 s
'''
