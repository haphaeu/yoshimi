# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 07:49:05 2016

@author: rarossi
"""
from random import randint

_c = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def rand_char():
    return _c[randint(0, len(_c)-1)]


def get_contents(size):
    contents = list()
    for i in range(size):
        string = ''
        for i in range(25):
            string += rand_char()
        contents.append(string)
    return contents


def approach1(contents):
    """Easy way - write list to file on the fly"""
    with open('file1.txt', 'w') as fd:
        for line in contents:
            fd.write('%s\n' % line)


def approach2(contents):
    """Buffer way - first write list to string, then dump string to file"""
    file_contents = ''
    for line in contents:
        file_contents += '%s\n' % line
    with open('file2.txt', 'w') as fd:
            fd.write(file_contents)


def main():
    large = get_contents(5000)
    small = get_contents(150)

    approach1(large)
    approach2(large)
    approach1(small)
    approach2(small)

"""
In:
%timeit approach1(large)
%timeit approach2(large)
%timeit approach1(small)
%timeit approach2(small)
Out:
100 loops, best of 3: 12.9 ms per loop
100 loops, best of 3: 3.79 ms per loop
1000 loops, best of 3: 1.11 ms per loop
1000 loops, best of 3: 845 µs per loop

Conclusion:
Calling a file write only once makes the same contents to be saved 3.4x faster for large files
and 1.3x faster for small files.
"""
