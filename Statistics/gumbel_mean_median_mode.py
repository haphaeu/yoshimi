# -*- coding: utf-8 -*-
"""
Playing with statistics to understand the difference between
mean, median, mode and how they relate to the percentiles.

Basically, for a symmetric distribution (normal):
mean=median=mode=P50

For skewed distributions, e.g. Gumbel, which are not symmetric:
median = P50

mode, or most probable maximum MPM, is the value with largest probability of occurence, max pdf.
Equivalent to a P37

mean, or expected value, is equivalent to a P57

Created on Thu Oct 01 09:51:38 2015
@author: rarossi
"""

from scipy import stats
from matplotlib import pyplot as pp
from numpy import linspace
from math import log

'''
Weibull

    c:
        shape parameter

    loc=0:
        location parameter

    scale=1:
        scale parameter


'''
#my_dist = stats.gumbel_r
my_dist = stats.weibull_min


# my_dist = stats.norm
SZ = 10000

sample = [stats.gumbel_r.rvs() for _ in range(SZ)]

params = my_dist.fit(sample)
g = my_dist(*params)
x, eps = linspace(min(sample), max(sample), SZ, retstep=True)
pp.figure(num=None, figsize=(9, 4), dpi=80, facecolor='w', edgecolor='k')
pp.plot(x, g.pdf(x), label='pdf')
pp.plot(x, g.cdf(x), label='cdf')
ymx = pp.ylim()[1]
pp.plot([g.mean()]*2, [0, ymx], label='mean %.2f' % g.mean())
pp.plot([g.median()]*2, [0, ymx], label='median %.2f' % g.median())
pp.plot([x[g.pdf(x).argmax()]]*2, [0, ymx], label='mode %.2f' % x[g.pdf(x).argmax()])
pp.hist(sample, bins=50, normed=True)
pp.legend(loc='best')
pp.title(my_dist.__getattribute__('name') + ' ' + ', '.join(['%.1f' % e for e in params]))
pp.grid()

pp.figure()
emp_x = [-log(-log((i-0.4)/(SZ+0.4))) for i in range(1, SZ+1)]
sample.sort()
pp.plot(sample, emp_x, 'x')
pp.grid()
pp.show()

# calculations for the probability of each of these parameters

# mode, or MPM
mpm = x[g.pdf(x).argmax()]
cdf_mpm = g.cdf(mpm)
print('MPM %.2f - CFD %.2f' % (mpm, cdf_mpm))

# mean, average or expected
expected = sum(x*g.pdf(x)*eps)  # probability weighted average of the variable
cdf_exp = g.cdf(expected)
print('Expected %.2f - CFD %.2f' % (expected, cdf_exp))

# median
median = g.ppf(0.5)
cdf_median = g.cdf(median)
print('Median %.2f - CFD %.2f' % (median, cdf_median))
