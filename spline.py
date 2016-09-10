# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 09:00:52 2016

@author: rarossi
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as itp

P = np.asarray([(0, 0), (0.3, 0.7), (1.0, 0), (2.0, 0), (5.0, 0.2), (7.0, 0.5)])
x = P[:, 0]
y = P[:, 1]
# Repeat first point for a closed curve
x = np.append(x, x[-1])
y = np.append(y, y[-1])

# Fits a parametric spline for both x and y
t = np.linspace(0, 1, len(x))
tckx = splx = itp.splrep(t, x, per=True)
tcky = sply = itp.splrep(t, y, per=True)

# Plot points for spline
plt.plot(x, y, 'ro', ms=5)
ts = np.linspace(0, 1, 1000)
plt.plot(itp.splev(ts, tckx), itp.splev(ts, tcky), 'g', lw=3, alpha=0.7)
plt.show()
