# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 13:53:38 2016

@author: rarossi
"""

from matplotlib import pyplot as plt
from scipy import stats as ss
from numpy import linspace

g = ss.gumbel_r(loc=0, scale=1)
n=1000
x = linspace(-2, 5, n)
plt.plot(x, g.pdf(x), label='pdf', lw=3)
plt.plot(x, 0.5*g.cdf(x), label='cdf', lw=3)
plt.xticks([])
plt.yticks([])
plt.xlabel('variate')
plt.ylabel('probability')
plt.legend(loc='best')
