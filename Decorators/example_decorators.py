# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 14:39:34 2016

@author: rarossi
"""
from math import log, exp, sqrt
import random

#
# some simple decorators as examples
#


def list_args(func):
    """Decorator to print the list of arguments passed to a function.
    Generic implementation that works with any function with any number of arguments.
    This is because *args and **kwargs is being used.
    If done for a specific function, the specific arguments could have been used.
    In this case, just pass the same list of arguments from the functions to be decorated
    to the wrapper inside the decorator.
    """
    def wrapper(*args, **kwargs):
        print('Listing the arguments passed to %s' % func.__name__)
        print('Arguments:')
        for arg in args: print(arg)
        print('Keyword arguments:')
        for key in kwargs.keys(): print('%s: %s' % (key, kwargs[key]))
        return func(*args, **kwargs)
    return wrapper


def benchmarking(func):
    """Decorator to calculate the time required to run a function.
    See comments abour generic arguments in the decorator list_args().
    """
    import time

    def wrapper(*args, **kwargs):
        print('Starting benchmarking function %s.' % func.__name__)
        t = time.time()
        res = func(*args, **kwargs)
        t = time.time() - t
        print('Function %s took %fs to run.' % (func.__name__, t))
        return res
    return wrapper


#
# this is a decorator for decorators, allowing to pass arguments to the decorated decorators
#


# http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python/1594484#1594484
def decorator_with_args(decorator_to_enhance):
    """
    This function is supposed to be used as a decorator.
    It must decorate an other function, that is intended to be used as a decorator.
    Take a cup of coffee.
    It will allow any decorator to accept an arbitrary number of arguments,
    saving you the headache to remember how to do that every time.
    """
    def decorator_maker(*args, **kwargs):
        def decorator_wrapper(func):
            # pitfall: the decorator must have this specific signature or it won't work:
            return decorator_to_enhance(func, *args, **kwargs)
        return decorator_wrapper
    return decorator_maker


#
# and the decorated decorator, which will have its own argument
#


@decorator_with_args
def say_hello(func, hello='\n- Hello!\n'):
    """Example of a decorator with an argument.
    Note that it actually doesn nothing to the function rather than saying a message as
    it starts.
    """

    def wrapper(*args, **kwargs):
        print(hello)
        return func(*args, **kwargs)
    return wrapper


#
# and here starts the example functions to be decorated
#


@say_hello('\n ---------\n Hi there!\n ---------\n')  # decorator passing argument
@list_args
@benchmarking
def project_euler_p004():
    """Project Euler problem 4"""
    maxPali = 0
    for n1 in range(999, 100, -1):
        for n2 in range(999, 100, -1):
            n = n1*n2
            if int(str(n)[::-1]) == n and n > maxPali:
                maxPali = n
                print("maximum so far is", maxPali)
    print("maximum found is", maxPali)


@benchmarking
def do_stuff(num_log=100, num_exp=100, num_sqrt=100):
    for i in range(num_log): tmp = log(random.randrange(1, 12345))
    for i in range(num_exp): tmp = exp(random.randrange(1, 123))
    for i in range(num_sqrt): tmp = sqrt(random.randrange(1, 12345))
    return tmp


def undecorated_do_stuff(num_log=100, num_exp=100, num_sqrt=100):
    for i in range(num_log): tmp = log(random.randrange(1, 12345))
    for i in range(num_exp): tmp = exp(random.randrange(1, 123))
    for i in range(num_sqrt): tmp = sqrt(random.randrange(1, 12345))
    return tmp


if __name__ == '__main__':
    project_euler_p004()
    do_stuff(1234, num_exp=5678)
    # note that this is the same as
    benchmarking(undecorated_do_stuff)(12345, num_exp=43221)
