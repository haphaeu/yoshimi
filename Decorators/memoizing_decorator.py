# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 15:10:59 2016

@author: rarossi
"""
import functools


def dec(func):
    """Simple decorator that prints 'call' every time the function is called"""
    def wrapper(n):
        wrapper.called += 1
        print('%s called %d times' % (func.__name__, wrapper.called))
        return func(n)
    wrapper.called = 0
    wrapper.__name__ = func.__name__
    return wrapper


def recursive_calls(func):
    """Memoize function calls. To be used with recursive functions."""
    global prev_call
    prev_call = {}

    def wrapper(n):
        if n not in prev_call:
            prev_call[n] = func(n)
        return prev_call[n]
    wrapper.__name__ = func.__name__
    return wrapper


@dec
def fib(n):
    """A bare recursive Fibonacci function. Expect many many function calls :)"""
    if n < 2:
        return 0
    if n < 4:
        return 1
    return fib(n-1)+fib(n-2)


@dec
@recursive_calls
def fib2(n):
    """Fibonacci function with the decorator defined above to memoize calls."""
    if n < 2:
        return 0
    if n < 4:
        return 1
    return fib2(n-1)+fib2(n-2)


@dec
@functools.lru_cache(maxsize=None)
def fib3(n):
    """Fibonacci function with the decorator from functools to memoize calls."""
    if n < 2:
        return 0
    if n < 4:
        return 1
    return fib3(n-1)+fib3(n-2)
