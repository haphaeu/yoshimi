# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 19:54:39 2013

@author: rafael
"""
from matrix import multimatrix, itermatrix, random_m, iterate_results
import matrix
import timeit

if __name__ == '__main__':
    a = [[1, 3], [-5, 6], [2, 4]]
    b = [[1, 4], [8, 7]]
    adotb = [[25, 25], [43, 22], [34, 36]]
    A = multimatrix(a)
    B = multimatrix(b)
    prod = A * B
    assert(adotb == prod)
    print prod, "multi test OK"
    A = itermatrix(a)
    B = itermatrix(b)
    iterprod = A * B
    listprod = iterate_results(iterprod)
    assert(adotb == listprod)
    print listprod, "iter test OK" 
 
    t = timeit.Timer("p = itermatrix(a) * itermatrix(a)", "from matrix import itermatrix, random_m; a = random_m(500, 500)")
    print "iterable product time:", t.timeit(number=1)
    
    t = timeit.Timer("p = itermatrix(a) * itermatrix(a); iterate_results(p)", "from matrix import itermatrix, random_m, iterate_results; a = random_m(500, 500)")
    print "list product time:", t.timeit(number=1)
 
    t = timeit.Timer("p = multimatrix(a) * multimatrix(a)", "from matrix import multimatrix, random_m, iterate_results; a = random_m(500, 500)")
    print "multi product time:", t.timeit(number=1)
    