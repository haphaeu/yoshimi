# -*- coding: utf-8 -*-
"""
Playing with statistics to understand if we can play with the samples to
get a better fit.

SOmetimes fitting x isn't a good fit, then we try to fit x^2 or sqrt(x)
and the fit gets better.

This script just checks if for a perfect sample
ppf(x) == ppf(x**2)**0.5 == ppf(x**0.5)**2

Created on Thu Oct 22 2015

@author: rarossi
"""

from scipy import stats

# using a gumbel_r distribution
my_dist = stats.gumbel_r

# size of the sample
SZ=100

# sample draw from the theoretical distribution
sample_x = [my_dist.rvs(loc=2500, scale=25) for _ in range(SZ)]

# get the sqrt of the sample
sample_sqrt = [x**0.5 for x in sample_x]

# and get sqr sample^2
sample_sqr = [x*x for x in sample_x]

# now fit back the distributions
g_x    = my_dist(*my_dist.fit(sample_x))
g_sqrt = my_dist(*my_dist.fit(sample_sqrt))
g_sqr  = my_dist(*my_dist.fit(sample_sqr))

print(g_x.ppf(0.9))
print(g_sqrt.ppf(0.9)**2)
print(g_sqr.ppf(0.9)**0.5)

