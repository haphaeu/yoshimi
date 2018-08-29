# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:05:27 2018
@author: rarossi
"""
import os
import sys
import glob
import random


def get_random_files(ext, top):
    '''Return the name of a random file within a top path.

    Works recursivelly in subdirectories.

    Note that a full list of files could be got with
        glob(top + '/**/*.' + ext, recursive=True)

    However that would be extremely slow for large directories.
    '''
    _top = top
    ct, limit = 0, 50000
    while True:

        if ct > limit:
            return 'No file found after %d iterations.' % limit
        ct += 1

        try:
            dirs = next(os.walk(top))[1]
        except StopIteration:  # access denied and other exceptions
            top = _top
            continue

        i = random.randint(0, len(dirs))
        if i == 0:  # use .
            files = glob.glob(top + '/*.' + ext)
            if not files:
                top = _top
                continue
            i = random.randint(0, len(files)-1)
            return files[i]

        top += '/' + dirs[i-1]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(get_random_files(sys.argv[1], os.getcwd()))
    else:
        print(get_random_files('*', os.getcwd()))
