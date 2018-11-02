# -*- coding: utf-8 -*-
"""
https://stats.stackexchange.com/questions/374973/what-is-the-most-probable-maximum-for-a-weibull-distribution

Created on Fri Nov  2 11:50:54 2018

@author: rarossi
"""

from scipy import stats
from matplotlib import pyplot as pp
from numpy import linspace

# Create a sample, right skewed to represent a distribution of maxima

sz = 10000
sample = stats.gumbel_r.rvs(loc=100, scale=3, size=sz)
sample -= min(sample)
x, eps = linspace(min(sample), max(sample), sz, retstep=True)

# Fit Weibull to the sample

# first using weibull_max
wb_mx = stats.weibull_max
params_wb_mx = wb_mx.fit(sample)
d_mx = wb_mx(*params_wb_mx)

# then using weibull_min
wb_mn = stats.weibull_min
params_wb_mn = wb_mn.fit(sample)
d_mn = wb_mn(*params_wb_mn)

# Plot everything

pp.figure(num=None, figsize=(9, 4), dpi=80, facecolor='w', edgecolor='k')
pp.plot(x, d_mx.pdf(x), label='Weibull Max')
#pp.plot(x, d_mx.cdf(x), label='Weibull Max')
pp.plot(x, d_mn.pdf(x), label='Weibull Min')
#pp.plot(x, d_mn.cdf(x), label='Weibull Min')
pp.hist(sample, bins=50, normed=True)
pp.legend(loc='best')
pp.grid()
pp.show()

print('Weibull Max {:12.1f} {:12.1f} {:12.1f}'.format(*params_wb_mx))
print('Weibull Min {:12.1f} {:12.1f} {:12.1f}'.format(*params_wb_mn))
