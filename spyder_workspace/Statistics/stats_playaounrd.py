# -*- coding: utf-8 -*-
"""
Created on Wed Jul 01 10:55:07 2015

@author: rarossi
"""
from scipy import stats
from matplotlib import pyplot as plt

import numpy as np
from numpy import (arange, sort, array, around, sqrt, log)
from scipy.stats import distributions
#from scipy import optimize
# From Stephens, M A, "Goodness of Fit for the Extreme Value Distribution",
#             Biometrika, Vol. 64, Issue 3, Dec. 1977, pp 583-588.
_Avals_gumbel = array([0.474, 0.637, 0.757, 0.877, 1.038])
def anderson(x,dist='gumbel_l'):
    """
    Anderson-Darling test for data coming from a particular distribution

    The Anderson-Darling test is a modification of the Kolmogorov-
    Smirnov test `kstest` for the null hypothesis that a sample is
    drawn from a population that follows a particular distribution.
    For the Anderson-Darling test, the critical values depend on
    which distribution is being tested against.  This function works
    for Gumbel right and left skewed distributions.
    
    This is a modified version of the anderson from scipy.stats.
    This version only works for Gumbel distribution and implements
    both gumbel_l and gumbel_r.

    Parameters
    ----------
    x : array_like
        array of sample data
    dist : {'gumbel_l','gumbel_r'}, optional
        the type of distribution to test against.  The default is 'gumbel_l'

    Returns
    -------
    A2 : float
        The Anderson-Darling test statistic
    critical : list
        The critical values for this distribution
    sig : list
        The significance levels for the corresponding critical values
        in percents.  The function returns critical values for a
        differing set of significance levels depending on the
        distribution that is being tested against.

    Notes
    -----
    Critical values provided are for the following significance levels:

    Gumbel
        25%, 10%, 5%, 2.5%, 1%

    If A2 is larger than these critical values then for the corresponding
    significance level, the null hypothesis that the data come from the
    chosen distribution can be rejected.
    
    I.e, A2 the smaller A2 the better.

    References
    ----------
    .. [1] http://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm
    .. [2] Stephens, M. A. (1974). EDF Statistics for Goodness of Fit and
           Some Comparisons, Journal of the American Statistical Association,
           Vol. 69, pp. 730-737.
    .. [3] Stephens, M. A. (1976). Asymptotic Results for Goodness-of-Fit
           Statistics with Unknown Parameters, Annals of Statistics, Vol. 4,
           pp. 357-369.
    .. [4] Stephens, M. A. (1977). Goodness of Fit for the Extreme Value
           Distribution, Biometrika, Vol. 64, pp. 583-588.
    .. [5] Stephens, M. A. (1977). Goodness of Fit with Special Reference
           to Tests for Exponentiality , Technical Report No. 262,
           Department of Statistics, Stanford University, Stanford, CA.
    .. [6] Stephens, M. A. (1979). Tests of Fit for the Logistic Distribution
           Based on the Empirical Distribution Function, Biometrika, Vol. 66,
           pp. 591-595.

    """
    if not dist in ['gumbel_l', 'gumbel_r']:
        raise ValueError("Invalid distribution; dist must be 'gumbel_l', "
                            "or 'gumbel_r'.")
    y = sort(x)
    xbar = np.mean(x, axis=0)
    N = len(y)
    if dist == 'gumbel_l':
        xbar, s = distributions.gumbel_l.fit(x)
        w = (y-xbar)/s
        z = distributions.gumbel_l.cdf(w)
    else: # (dist == 'gumbel_r')
        xbar, s = distributions.gumbel_r.fit(x)
        w = (y-xbar)/s
        z = distributions.gumbel_r.cdf(w)
    
    sig = array([25,10,5,2.5,1])
    critical = around(_Avals_gumbel / (1.0 + 0.2/sqrt(N)),3)

    i = arange(1,N+1)
    S = sum((2*i-1.0)/N*(log(z)+log(1-z[::-1])),axis=0)
    A2 = -N-S
    return A2, critical, sig


def best_fit(tail):
    """Uses anderson() to find if the data fit better to a gumbel_l or gumbel_r distribution.
    """
    if anderson(tail, 'gumbel_l')[0] < anderson(tail, 'gumbel_r')[0]:
        return stats.gumbel_l
    else:
        return stats.gumbel_r


tailmax = [63.96574, 97.298988, 94.909447, 68.972389, 66.959663, 65.273926, 84.017792,
151.969101, 102.427635, 89.193542, 166.099564, 242.734909, 108.961304,
92.404419, 66.82309, 75.563385, 57.813889, 105.774223, 67.279755,
86.967712, 74.676308, 75.610916, 76.830391, 116.130943, 74.360512,
180.654968, 103.529533, 111.010529, 149.957794, 70.670921, 129.729172,
169.322662, 67.288033, 171.149643, 164.885376, 83.445435, 97.363678,
91.548149, 133.007599, 94.024841, 180.025314, 152.898285, 98.16478,
102.753448, 121.835167, 123.101646, 69.144646, 83.610756, 66.493416,
123.173607, 79.628456, 67.263359, 83.174103, 88.059792, 112.641327,
80.654366, 73.827545, 68.375336, 61.010174, 125.977417, 99.530197,
131.255432, 71.376617, 97.577362, 211.96611, 66.308861, 228.915405,
77.390526, 143.579269, 61.86153, 100.229225, 103.135757, 85.798904,
165.273346, 72.525803, 68.17765, 105.367897, 108.670799, 288.688293,
140.604355, 109.679535, 95.767075, 105.137451, 93.383766, 186.602676,
119.793755, 90.300858, 66.34745, 83.441994, 107.981186, 127.843536,
133.305923, 84.114273, 117.124664, 69.92189, 91.000229, 187.557693,
73.156982, 92.472664, 115.126579]

tailmin=[12.778043, 7.1879, 13.314878, 8.776149, 9.805628, 6.535013, 11.488866, 2.293265, 8.724171,
         0.516041, 7.964844, 7.569489, 14.650825, 3.988805, 12.13273, 15.306945, 15.383864,
         2.656031, 15.595515, 7.864027, 16.6761, 16.082186, 13.647097, 5.082881, 12.534531, 
         5.564847, 7.260636, 3.754782, 0.453892, 10.34429, 0.477659, 13.715585, 6.424349, 5.42458, 
         18.09203, 12.374338, 7.28268, 5.973233, 7.73395, 3.02955, 16.93425, 6.616414, 1.377988,
         16.089392, 4.625199, 11.124841, 7.413293, 12.457375, 0.074295, 19.787035, 7.31939, 
         2.731352, 10.156926, 8.684792, 11.394233, 14.931318, 11.838491, 2.556698, 15.741388,
         1.014213, 0.480564, 14.461552, 7.140567, 3.386644, 18.038301, 4.436148, 12.638147,
         9.086492, 0.373772, 10.272347, 6.930659, 2.091561, 6.558409, 14.133745, 17.415342,
         5.365997, 9.676363, 12.914423, 10.606887, 17.576532, 12.987781, 2.375166, 1.529086, 
         11.657972, 5.48551, 18.472898, 4.56945, 7.49713, 9.266244, 15.596133]

for tail in [tailmax, tailmin]:
    plt.figure()
    title('TEST TITLE')
        
    plt.subplot(221)
    plt.hist(tail)
    
    gumbel = best_fit(tail)
    loc, scale = gumbel.fit(tail)
    mygl = gumbel(loc=loc, scale=scale)
    plt.subplot(222)
    stats.probplot(tail,dist=mygl,plot=plt)
    title('bets fit gumbel')
    
    loc, scale = stats.gumbel_l.fit(tail)
    mygl = stats.gumbel_l(loc=loc, scale=scale)
    plt.subplot(223)
    stats.probplot(tail,dist=mygl,plot=plt)
    title('gumbel l')
    
    loc, scale = stats.gumbel_r.fit(tail)
    mygr = stats.gumbel_r(loc=loc, scale=scale)
    plt.subplot(224)
    stats.probplot(tail,dist=mygr,plot=plt)
    title('gumbel r')

#import pandas
#
##list with the path to various results files from repeated lowering analyses
#with open('list_results.txt', 'r') as pf:
#    list_results = pf.readlines()
#
##write statistics to this file
#global_statistics_file = open('global_statistics.txt','w')
#global_statistics_file.write('File \t Total Cases \t Max \t Min \t Max_l \t Max_r \t ')
#global_statistics_file.write('Min_l \t Min_r \t Max_bad \t Min_bad\n')
#
#for resfile in list_results:
#    print resfile    
#    global_statistics_file.write('%s \t ' % resfile[:-1])
#    try:
#        res = pandas.read_table(resfile[:-1])
#        range_hs = set(res['WaveHs'])
#        range_tp = set(res['WaveTp'])
#        range_wd = set(res['WaveDirection'])
#        counter = 0
#        counter_max = 0
#        counter_min = 0
#        counter_max_bad = 0
#        counter_min_bad = 0
#        counter_max_r = 0
#        counter_min_l = 0
#        for wd in range_wd:
#            res_wd = res[res['WaveDirection'] == wd]
#            for hs in range_hs:
#                res_hs = res_wd[res_wd['WaveHs'] == hs]
#                for tp in range_tp:
#                    res_tp = res_hs[res_hs['WaveTp'] == tp]
#                    for col in res.columns[3:]:
#                        A2_l, critical_l, lvls_l = anderson(res_tp[col],'gumbel_l')
#                        A2_r, critical_r, lvls_r = anderson(res_tp[col],'gumbel_r')
#                        if False:
#                            print '%ddeg \t %.2fm \t %ds \t ' % (wd, hs, tp),
#                            print '{:<30s} \t '.format(col),
#                            print '%.2f \t %.2f \t ' % (min((A2_l, A2_r)), max(critical_l)),
#                            if A2_l < A2_r: print 'l \t ',
#                            else: print 'r \t ',
#                            if min((A2_l, A2_r)) > max(critical_r): print 'not ok'
#                            else: print ''
#        
#                        counter += 1
#                        if col.lower().find('max') is not -1:
#                            counter_max += 1
#                            if min((A2_l, A2_r)) < max(critical_r): 
#                                if A2_r < A2_l: counter_max_r += 1
#                            else: counter_max_bad += 1
#                        else:
#                            counter_min += 1
#                            if min((A2_l, A2_r)) < max(critical_r): 
#                                if A2_l < A2_r: counter_min_l += 1
#                            else: counter_min_bad += 1
#    except:
#        global_statistics_file.write('fail\n')
#        print 'fail'
#        continue
#
#    #write to a file
#    global_statistics_file.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' %
#                                 (counter, counter_max, counter_min, 
#                                  counter_max-counter_max_r-counter_max_bad, counter_max_r,
#                                  counter_min_l, counter_min-counter_min_l-counter_min_bad,
#                                  counter_max_bad, counter_min_bad))
#    global_statistics_file.flush()                    
#    #write to screen
#    print 'Out of a total of %d cases, %d are max and %d are min' % (counter, counter_max, counter_min)
#    print 'Max cases: %d fit gumbel_r, %d fit gumbel_l and %d didn\'t fit.' % (
#           counter_max_r, counter_max-counter_max_r-counter_max_bad, counter_max_bad) 
#    print 'Min cases: %d fit gumbel_r, %d fit gumbel_l and %d didn\'t fit.' % (
#           counter_min-counter_min_l-counter_min_bad, counter_min_l, counter_min_bad) 
#    print ''
#    print ''
#
#global_statistics_file.close()