# -*- coding: utf-8 -*-
"""
Here is the example in Alex Martelli Python Cookbook that show how to create a memoize decorator
using cPickle for function that take mutable argument (original version) :


https://stackoverflow.com/questions/4669391/python-anyone-have-a-memoizing-decorator-that-can-handle-unhashable-arguments

adapted to python 3

Created on Mon Jul 17 16:02:15 2017

@author: rarossi
"""

import pickle


class MemoizeMutable:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args, **kwds):
        str = pickle.dumps(args, 1)+pickle.dumps(kwds, 1)
        if str not in self.memo:
            print("miss")  # DEBUG INFO
            self.memo[str] = self.fn(*args, **kwds)
        else:
            print("hit")  # DEBUG INFO

        return self.memo[str]


@MemoizeMutable
def dummy(inp):
    return inp[0]


dummy([1, 2, 3])
dummy([3, 4, 5])
dummy([1, 2, 3])
