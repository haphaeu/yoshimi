# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 20:20:31 2017

@author: raf
"""
import numpy as np
from scipy import stats as ss
from matplotlib import pyplot as plt
import quantilelib as ql

n = 50

sample = ss.gumbel_l.rvs(size=n, loc=100, random_state=1234)
sample.sort()

y = ql.llsurvivals(n)
plt.plot(sample, y, 'o')


# fit that shit
params = ss.gumbel_l.fit(sample)
fitted_gumbel = ss.gumbel_l(*params)

# get two points for plotting
x = sample.min(), sample.max()
y = -np.log(-fitted_gumbel.logsf(x))

# plot this shit
plt.plot(x, y)
