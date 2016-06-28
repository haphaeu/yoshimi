# -*- coding: utf-8 -*-
"""

Creates a picture at the correct size to paste into a report.

Seems that 96 dpi is required to match size after pasted in MS Word.

Prefer PNG format - lossless, good for text and plots.

Created on Wed May  4 13:13:41 2016

@author: rarossi
"""

from matplotlib import pyplot as plt
import numpy as np

width = 165  # mm
height = 90  # mm

x = np.linspace(0, 2*np.pi, 100)

plt.figure(figsize=(width/25.4, height/25.4))
plt.plot(x, np.sin(x))
plt.title('This is an example picture!')
plt.savefig('test.png', dpi=96)
