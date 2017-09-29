# -*- coding: utf-8 -*-
"""

Confidence Intervals

Calculate the confidence interval of a sample using a bootstrapping technique.

[1] https://ocw.mit.edu/courses/mathematics/18-05-introduction-to-probability-and-statistics-spring-2014/readings/MIT18_05S14_Reading24.pdf

Created on Thu Sep 28 15:26:26 2017

@author: rarossi
"""
import math
import numpy as np
from scipy import stats as ss
from matplotlib import pyplot as plt


def confidence_interval(sample, ci=0.95, repeat=1000, relative=True, random_seed=12343):
    """Returns the lower and upper confidence intervals of a sample. The intervals can be
    relative or absolute, i.e: absolute = sample + relative

    The returned array has shape (2, len(sample)).

    The interval is calculated for a 100*ci % confidence level.

    Bootstrapping technique is used for the calculation of the intervals, using a sorted resampling
    with replacement. Note that this technique uses random resampling. A random seed is set to make
    sure that calls of this function with same arguments will return the same intervals. To change
    the random seed, change the default argument random_seed.

    Arguments:
        sample      : array with the sample values
        ci          : confidence level of the interval
        repeat      : bootstrap size
        relative    : set to True for relative intervals, False for absolute intervals, i.e.,
                      absolute intervals = sample + relative_intervals.
                      relative intervals can be seen as tolerances to sample values, while
                      absolute intervals are lower and upper bounds for the variate values.
        random_seed : seed for the random generator used in the resample function.
    """
    sample.sort()
    size = len(sample)
    m_star = np.zeros(shape=(repeat, size))
    np.random.seed(random_seed)
    for i in range(repeat):
        m_star[i] = sample[np.random.randint(0, size, size)]  # re-sampling with replacement
        m_star[i].sort()
    delta_star = m_star - sample
    delta_star.sort(axis=0)
    ci_idx = np.array([math.floor((1.0 - ci)/2*repeat), math.ceil(repeat - (1.0 - ci)/2*repeat)])
    return delta_star[ci_idx] + (0 if relative else sample)


def cdf(size):
    """Returns the CDF for a t-distribution"""
    return np.linspace(0.5/size, (size-0.5)/size, size)


def llcdf(size):
    """Returns the -log(-log(CDF)) for a t-distribution"""
    return -np.log(-np.log(cdf(size)))


ssz = 50
sample = ss.gumbel_r.rvs(size=ssz, loc=100, scale=3)
# sample = np.random.randint(1, 50, size=ssz)
sample.sort()
ci, nboots = 0.95, 1000
err = confidence_interval(sample, ci, nboots)
y = llcdf(ssz)

plt.rcParams['figure.figsize'] = 10, 5
plt.errorbar(sample, y, fmt='o', xerr=(-err[0], err[1]), ecolor='gray')
plt.title('%d%% Confidence Intervals - Seeds %d\nBootstrapping %d samples' % (100*ci, ssz, nboots))
plt.xlabel('Variate')
plt.ylabel('-ln(-ln(cdf))')
plt.grid()
