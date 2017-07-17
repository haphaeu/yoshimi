# -*- coding: utf-8 -*-
"""

Metocean data gives Weibull parameters for extreme Hs.

This script implements the Weibull parameters and converts extremes into operability
given a limiting Hs for an operation.


Created on Fri Jul  7 15:14:33 2017

@author: rarossi
"""

from scipy import stats as ss
import numpy as np

# #####################################
# Gullfaks metocean
# August
shape, scale, loc = 1.190, 1.09, 0.56
r = np.array((5.1, 6.7, 8.2))
# September
shape, scale, loc = 1.272, 1.70, 0.72
r = np.array((7.2, 9.3, 11.2))
# #####################################

w = ss.weibull_min(c=shape, loc=loc, scale=scale)

hs_lim = 2.25  # meters
print('Hs %.2f m - Operability %.2f' % (hs_lim, w.cdf(hs_lim)))


# ###########################################################################################
# This below is just for cross checking the extreme values from metocean
# against the fitted Weibull in the script. They must match.

event_t = 3  # event duration, in hours
return_t = np.array((1, 10, 100))*365*24  # return periods, hours in 1, 10 and 100 years
sector_p = 1/12  # sector or seasonal probability. 1 for annual/omni. 1/12 for monthly...
p = 1-event_t/return_t/sector_p  # event cumulative probability of non-exceedance
# print(r)
# print(w.ppf(F))
if np.allclose(r, w.ppf(p), rtol=1e-2, atol=1e-3):
    print('Check ok.')
else:
    print('Check FAILED.')
