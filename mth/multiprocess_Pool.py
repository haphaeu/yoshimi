# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 08:14:10 2017

@author: rarossi
"""

from multiprocessing import Pool

def f(x):
    print(x*x)


if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(f, range(10))
    r = pool.map_async(f, range(10))
    print('HERE')
    print('MORE')
    r.wait()
    print('DONE')
