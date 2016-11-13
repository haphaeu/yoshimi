# -*- coding: utf-8 -*-
"""

Calculates sha256sum for a file and compares against input.

Created on Sat Jul  9 11:49:16 2016

@author: raf
"""
import hashlib

def chksha(fname, sha):
    try:
        f = open(fname, 'rb')
    except:
        print('Error: Unable to open %s' % fname)
        return 0
    print('File  : %s' % fname)
    print('Input :', sha)
    out = hashlib.sha256(f.read()).hexdigest()
    print('Output:', out)
    if sha == out:
        print('Pass. Hashes match, file is valid.')
    else:
        print("FAIL. Hashes don't match.")

if __name__ == '__main__':
    fname = 'E:\\sysrecd\\iso\\systemrescuecd-x86-4.8.3.iso'
    sha = '1a4a1d35e32a812f42415596695e4dec9f50781c251d034579a45df1e9049e3e'
    chksha(fname, sha)
