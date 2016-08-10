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
        print('Pass! Hashes match, file is valid!')
    else:
        print("FAIL! Hashes don't match. Got:")

if __name__ == '__main__':
    fname = 'E:\\Downloadz\\ChromeDownloads\\systemrescuecd-x86-4.8.0.iso'
    sha = '06e6847384063bbb67c1c8f0824e995046c9ff125ad07a4214b129efb9b18241'
    chksha(fname, sha)
