# -*- coding: utf-8 -*-
"""
https://stats.stackexchange.com/questions/374973/what-is-the-most-probable-maximum-for-a-weibull-distribution


Weibull parameters:
    shape, k:
        k > 0
        distribution only has a mode for k > 1

    location:

    scale, lambda:

The mode (MPM) is:
    lambda * ((k-1)/k)**(1/k)
    scale * ((shape-1)/shape)**(1/shape)


Created on Fri Nov  2 11:50:54 2018

@author: rarossi
"""

from scipy import stats
from matplotlib import pyplot as pp
from numpy import linspace

# Create a sample, right skewed to represent a distribution of maxima

sz = 1000
#sample = stats.gumbel_r.rvs(loc=100, scale=3, size=sz)
#sample = stats.norm.rvs(loc=100, scale=3, size=sz)
sample = stats.weibull_min.rvs(c=5, loc=100, scale=3, size=sz)
#sample -= min(sample)
x, eps = linspace(min(sample), max(sample), sz, retstep=True)

# Fit Weibull to the sample

## first using weibull_max
#wb_mx = stats.weibull_max
#params_wb_mx = wb_mx.fit(sample)
#k, loc, lbd = params_wb_mx
#mode_mx = lbd * (1-1/k)**(1/k) + loc
#d_mx = wb_mx(*params_wb_mx)

# then using weibull_min
wb_mn = stats.weibull_min
params_wb_mn = wb_mn.fit(sample)
k, loc, lbd = params_wb_mn
mode_mn = lbd * (1-1/k)**(1/k) + loc
d_mn = wb_mn(*params_wb_mn)

# Plot everything

pp.figure(num=None, figsize=(9, 4), dpi=80, facecolor='w', edgecolor='k')

#pp.plot(x, d_mx.pdf(x), label='Weibull Max')
## pp.plot(x, d_mx.cdf(x), label='Weibull Max')

pp.plot(x, d_mn.pdf(x), label='Weibull Min')
# pp.plot(x, d_mn.cdf(x), label='Weibull Min')
pp.hist(sample, bins=50, normed=True)
pp.legend(loc='best')
pp.grid()
pp.show()

print('            {:>12s} {:>12s} {:>12s} {:>12s} {:>12s}'.format('Shape', 'Loc', 'Scale', 'Mode', 'cdf(Mode)'))
#print('Weibull Max {:12.1f} {:12.1f} {:12.1f} {:12.1f} {:12.2f}'.format(*params_wb_mx, mode_mx, d_mx.cdf(mode_mx)))
print('Weibull Min {:12.1f} {:12.1f} {:12.1f} {:12.1f} {:12.2f}'.format(*params_wb_mn, mode_mn, d_mn.cdf(mode_mn)))
