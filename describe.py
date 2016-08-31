# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:22:52 2016

@author: rarossi
"""


def describe(obj):
    for key in dir(obj):
        try:
            val = getattr(obj, key)
        except AttributeError:
            continue
        if callable(val):
            help(val)
        else:
            print('{k} => {v}'.format(k=key, v=val))
        print('-'*80)
