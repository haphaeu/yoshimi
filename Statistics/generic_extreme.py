# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:05:13 2015

@author: rarossi
"""

from scipy import stats as ss
from numpy import linspace
from matplotlib import pyplot as plt
from math import log, exp
sz = 1000
mydistro = ss.gumbel_r
myparams = (0, 1)
myfunc = lambda x: -log(-log(x))
# myfunc = lambda x: -log(x)
# myfunc = lambda x: x
# myfunc = lambda x: exp(x)


sample = [mydistro.rvs(*myparams) for _ in range(sz)]
sample.sort()
emp = [(i+0.6)/(sz+0.4) for i in range(sz)]
dist_emp = list(map(myfunc, emp))
ge = ss.genextreme(*ss.genextreme.fit(sample))
x = linspace(min(sample), max(sample), 100)


plt.subplot(211)
plt.hist(sample, normed=True, bins=20)
plt.plot(x, ge.pdf(x))

plt.subplot(212)
plt.plot(sample, dist_emp, '.')
plt.plot(sample, list(map(myfunc, ge.cdf(sample))))
