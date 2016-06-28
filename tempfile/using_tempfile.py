# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:48:54 2016

@author: rarossi
"""

import os
import time
import tempfile

# creates a temporary file
pf = tempfile.NamedTemporaryFile(mode='w', dir='.', prefix='missing_', suffix='.txt', delete=False)
print('File %s created.' % pf.name)
pf.write('this is a temp\nfile')
pf.close()
print('File closed. Deleting files in 3s...', end='')
time.sleep(3)
os.remove(pf.name)
print('done.')

#creates atemporary directory
pdir = tempfile.mkdtemp(dir='.')
print('Directory created: %s' % pdir)
print('Deleting directory in 3s...', end='')
time.sleep(3)
os.rmdir(pdir)
print('done.')