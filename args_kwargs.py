# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:02:55 2015

@author: rarossi

"""


def f(*args, **kwargs):
    """Dummy example of using *args and **kwargs in a function's arguments
    args is a tuple with all the non-keyword arguments in the order they've
    been entered. kwargs is a dictionary with the names and values passed
    as keyword arguments.
    """
    print(type(args))
    print(type(kwargs))
    for arg in args:
        print(arg)
    for name, value in kwargs.items():
        print(name, value)

f(1, 2, 3.1415, 'Hello!')
f(1, 2, 3.1415, 'Hello!', a=1, color='red', mx=-2.78)
