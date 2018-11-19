# -*- coding: utf-8 -*-
"""

[1] DNV GL JIP Practical Guidance to Estimation of Response Extremes
    Report No.: 2015-0684, Rev. 0
    Document No.: 186RZ20-49
    Date: 2015-09-07

[2] Theory and derivation for Weibull parameter probability weighted moment estimators
    https://books.google.no/books?id=d6OJf5SuP9YC

Created on Fri Nov  9 21:11:20 2018

@author: rarossi
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import OrcFxAPI as of
import scipy.stats as ss
from numpy import log
from scipy.special import binom
from scipy.special import gamma as gamma_function


def M(j, x):
    '''Probability Weighted Moments.

    x must be sorted.

    See [1] and eq. (32) in [2]
    '''
    n = len(x)
    return sum([x[i-1] * binom(i-1, j)/binom(n-1, j)
                for i in range(j+1, n)])/n


def weibull_fit(x):
    '''Fit Weibull parameters using PWM.

    Return (shape, location, scale).

    See section 2.2.3.1 of [1] and [2].
    '''
    M0 = M(0, x)
    M1 = M(1, x)
    M2 = M(2, x)
    M3 = M(3, x)

    delta = (4 * (M0 * (3 * M2 - M3 - M1) - M1**2) /
             (M0 - 8*M1 + 12*M2 - 4*M3))

    gamma = log(2) / log((2*M1 - M0) /
                         (2 * (5*M1 - M0 - 6*M2 + 2*M3)))

    beta = (M0 - delta) / gamma_function(1 + 1/gamma)

    return gamma, delta, beta


def weib2gumb(params, N):
    '''Explicity calculation of the parameters of a Gumbel distribution
    of extreme response for a Weibull distribution of response peaks.

    Returns
    -------
    loc, scale:
        Parameters of Gumbel distribution.

    Arguments
    ---------
    params:
        Weibull distribution parameters (shape, loc, scale).

    N:
        Size of the sample

    See [1].
    '''
    shape, loc, scale = params
    return (loc + scale * log(N)**(1/shape), scale/shape * log(N)**(1/shape-1))


def global_peaks(values, times):
    '''Detects global peaks of a signal.

    Returns the global peaks and respective times.
    '''

    # brute forcing a litte

    # shift by average to make sure there are zero crossings
    ref = sum(values)/len(values)

    # zero up-crossings
    zuc = [i for i in range(len(values)-1) if values[i] < ref and values[i+1] > ref]

    # indexes of the peaks
    index = [zuc[i] + values[zuc[i]:1+zuc[i+1]].argmax() for i in range(len(zuc)-1)]

    return values[index], times[index]


def fetch_timetrace(sim, list_vars=None):

    # very simplified fetch of timetraces
    # supports sim and txt files

    print('Loading', sim, end='.')

    if os.path.splitext(sim)[1].lower() == '.txt':
        data = np.loadtxt(sim, skiprows=1, unpack=True)
        with open(sim) as pf:
            headers = pf.readline().rstrip().split('\t')
        ttraces = {h: tt for h, tt in zip(headers, data)}
        print('Done.')
        return ttraces

    # assuming sim file here
    m = of.Model(sim)
    print(' Done.')
    ttraces = dict()
    ttraces['Time'] = m.general.TimeHistory('Time', 1)

    for var in list_vars:
        name = ' '.join(var)
        if var[1].lower() == 'enda':
            oe = of.oeEndA
        elif var[1].lower() == 'endb':
            oe = of.oeEndB
        elif var[1].lower() in ('touchdown', 'tdp', 'tdz'):
            oe = of.oeArcLength(m['Line1'].StaticResult('Arc Length', of.oeTouchdown))
        else:
            raise SystemError
        ttraces[name] = m['Line1'].TimeHistory(var[0], 1, objectExtra=oe)

    return ttraces


# See jupyter notebook...
# peak_finder_weibull_fit
