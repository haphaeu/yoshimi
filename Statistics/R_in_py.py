# -*- coding: utf-8 -*-
"""

Playing with R inside Python

http://rpy2.readthedocs.io/en/version_2.8.x/introduction.html

Created on Mon Oct  9 13:14:17 2017

@author: rarossi
"""
import sys
import time
from scipy import stats as ss
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import itertools

# Import my modules
import quantilelib as ql
sys.path.append(r'C:\Users\rarossi\Documents\git\yoshimi\Qt\ResultsVisualiser')
import confidence_interval_bootstrap as cib

# Import of R objects
from rpy2 import robjects
from rpy2.robjects.packages import importr
rfitdistrplus = importr('fitdistrplus')
rstats = importr('stats')
rbase = importr('base')

# R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R
# Define the Gumbel distribution in R
robjects.r('''
        # create functions for `gumbel`
        dgumbel <- function(x, a, b) 1/b*exp((a-x)/b)*exp(-exp((a-x)/b))
        pgumbel <- function(q, a, b) exp(-exp((a-q)/b))
        qgumbel <- function(p, a, b) a-b*log(-log(p))
        dgumbelmin <- function(x, a, b) 1/b*exp((x-a)/b)*exp(-exp((x-a)/b))
        pgumbelmin <- function(q, a, b) 1-exp(-exp((q-a)/b))
        qgumbelmin <- function(p, a, b) a+b*log(-log(1-p))
        ''')
#  R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R


def log(s, mode='a'):
    """Logging function - writes to stdout and to file"""
    s += '\n'
    pf = open(r'R_in_py\log.txt', mode)
    outs = [sys.stdout.write, pf.write]
    for out in outs:
        out(s)
    pf.close()


log('[' + time.asctime() + '] ', mode='w')

# Load a Results.txt to use as test sample
# resfile = r'C:\Users\rarossi\Documents\git\yoshimi\Qt\ResultsVisualiser\Results.txt'
resfile = r'T:\Temp\AOA\ITS IDC\ITS splash zone - 18m radius\Results.txt'
log(resfile)
df = pd.read_table(resfile)

variables = df.columns[3:]
hss = set(df.WaveHs)
tps = set(df.WaveTp)
wds = set(df.WaveDirection)

# critical sea states for the ITS deployment
seastates = [(2.4, 5, 165), (2.4, 5, 180), (2.4, 5, 195),
             (2.2, 6, 165), (2.2, 6, 180), (2.2, 6, 195),
             (2.2, 7, 165), (2.2, 7, 180), (2.2, 7, 195),
             (2.0, 8, 165), (2.0, 8, 180), (2.0, 8, 195),
             (2.0, 9, 165), (2.0, 9, 180), (2.0, 9, 195),
             (2.2, 10, 165), (2.2, 10, 180), (2.2, 10, 195),
             (2.4, 11, 165), (2.4, 11, 180), (2.4, 11, 195),
             (2.4, 12, 165), (2.4, 12, 180), (2.4, 12, 195),
             (2.4, 13, 165), (2.4, 13, 180), (2.4, 13, 195),
             (2.6, 14, 165), (2.6, 14, 180), (2.6, 14, 195)]


# count, tot = 0, len(variables)*len(hss)*len(tps)*len(wds)
count, tot = 0, len(variables)*len(seastates)

# for var, hs, tp, wd in itertools.product(variables, hss, tps, wds):
for var, seast in itertools.product(variables, seastates):
    hs, tp, wd = seast

    count += 1

    # hs, tp, wd = 3.5, 12, 195
    # var = 'Link1 Min Tension'

    sample = df[(df.WaveHs == hs) & (df.WaveTp == tp) & (df.WaveDirection == wd)][var]

    if sample.empty:
        continue

    log('#'*80)
    log('{}/{} - {} - Hs {} - Tp {} - wd {}'.format(count, tot, var, hs, tp, wd))
    tail = 'upper' if 'Max' in var else 'lower'

    sample = np.array(sample)
    # Convert the sample into a R vector
    rsample = robjects.FloatVector(sample)

    # Show sample
    # plt.hist(sample, bins=7)
    # plt.show()

    # R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R
    #  R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R
    # Now move into R and fit statistics on sample...

    # use method of moments for first estimate of parameters
    b = np.std(sample)*np.sqrt(6)/np.pi
    a = np.mean(sample) - b * np.euler_gamma
    # Use R fitdist to fit a Gumbel distribution to sample
    Rfun = "gumbel" if tail == 'upper' else "gumbelmin"
    rfit = rfitdistrplus.fitdist(rsample, Rfun, start=rbase.list(a=a, b=b))
    # Use R confint to calculate the confidence intervals for the fitted
    # distro parameters
    rci = np.array(rstats.confint(rfit)).transpose()
    rfit = tuple(rfit[0])

    # ATTENTION HERE
    # Last time run I'M SURE R returned (loc, scale), but now it seems to be returning (scale, loc)
    # Therefore I'm flipping it around to match output of cib...
    rfit = tuple(np.flipud(rfit))
    rci = np.fliplr(rci)

    #  R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R
    # R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R R

    # Now fit the same statistics using scipy and my modules
    stats_fun = ss.gumbel_r.fit if tail == 'upper' else ss.gumbel_l.fit
    pfit = stats_fun(sample)
    pci = cib.confidence_interval(sample, stats_fun, relative=False, repeat=2000)

    # ###
    # Compare what has been done so far
    log('Pack \t Loc    \t Scale')
    log('R \t %.3f \t %.3f' % (rfit))
    log('Scipy \t %.3f \t %.3f' % (pfit))
    log('Confidence Interval from R')
    log(' 2.5%%\t %.4f\t%.4f' % tuple(rci[0]))
    log('97.5%%\t %.4f\t%.4f' % tuple(rci[1]))
    log('Confidence Interval from cib')
    log(' 2.5%%\t %.4f\t%.4f' % tuple(pci[0]))
    log('97.5%%\t %.4f\t%.4f' % tuple(pci[1]))
    log('Relative % differences')
    log(str((100 - 100*pci/rci).round(2)))

    # ###
    # Show graphically the differences

    def get_y(params, x, tail):
        if tail == 'upper':
            return -np.log(-ss.gumbel_r(*params).logcdf(x))
        else:
            return -np.log(-ss.gumbel_l(*params).logsf(x))

    # plot sample
    sample.sort()
    y = ql.llquantiles(len(sample)) if tail == 'upper' else ql.llsurvivals(len(sample))
    plt.plot(sample, y, 'o', label='sample')

    # plot best fit and confidence intervals from cib
    x = sample.min(), sample.max()
    y = get_y(pfit, x, tail).transpose()
    plt.plot(x, y, '--b', label='cib')
    y = np.array([get_y(p, x, tail) for p in pci]).transpose()
    plt.plot(x, y, '--b')

    # plot confidence intervals from R
    y = get_y(rfit, x, tail).transpose()
    plt.plot(x, y, 'r', label='R')
    y = np.array([get_y(p, x, tail) for p in rci]).transpose()
    plt.plot(x, y, 'r')
    plt.title('{} - Hs {} - Tp {} - wd {}'.format(var, hs, tp, wd))
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(r'R_in_py\{}-Hs{}-Tp{}-wd{}.png'.format(var, hs, tp, wd))
    plt.show()
    plt.close()
