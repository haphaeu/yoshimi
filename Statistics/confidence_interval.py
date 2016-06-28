# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:27:04 2016
@author: rarossi

Confidence interval
-------------------
Example: a 95% confidence interval means that for N randomly generated samples with the same
population parameters, 95% of the calculated confidence intervals for these N samples will contain
the true value (mean, P90, ...)

http://stackoverflow.com/questions/28242593/correct-way-to-obtain-confidence-interval-with-scipy

"""
from scipy import stats as ss
from numpy import sqrt


def within_confidence_interval_gumbel(*args):
    """Using a standard Gumbel distribution - location=0, scale=1"""

    # Calculates the true value for the population parameter of interest,
    # in this case, the 90-percentile of a right skewed Gumbel distro.
    true_value = ss.gumbel_r.ppf(0.9)

    # Generates a random Gumble distributed sample with 100 points.
    sample = ss.gumbel_r.rvs(size=100)

    # P90 fitted from the generated sample.
    fit_value = ss.gumbel_r.ppf(0.9, *ss.gumbel_r.fit(sample))

    # Calculates the 95% confidence interval.
    a, b = ss.gumbel_r.interval(0.95, loc=fit_value, scale=sample.std()/sqrt(100))

    # Returns True if the confidence interval contains the true value.
    return a < true_value < b


def conf_interval():
    n = 10000
    p = 0.9
    cl = 0.95

    p90_tru = ss.gumbel_r.ppf(p)
    sample = ss.gumbel_r.rvs(size=n)
    p90_fit = ss.gumbel_r.ppf(p, *ss.gumbel_r.fit(sample))
    sample.sort()
    p90_emp = sample[int(p*n)]

    # method 1
    # Using gumbel distribution. Not sure is scale should be sample.std or gumbel.std ?
    Rg = ss.gumbel_r.interval(cl, loc=p90_fit, scale=ss.gumbel_r.std()/sqrt(n))

    # method 2
    Rt = ss.t.interval(cl, n-1, loc=p90_emp, scale=sample.std()/sqrt(n))

    if False:
        print('P90 true valie: %.2f' % p90_tru)
        print('P90 empirical: %.2f' % p90_emp)
        print('P90 Gumbel fit: %.2f' % p90_fit)
        print('Confidence interval Gumbel:', Rg, ' - note that this is not symmetric')
        print('Confidence interval Student-T:', Rt, ' - this is symmetric')

    return p90_tru, p90_emp, p90_fit, Rg, Rt


if __name__ == '__main__':

    # This should return something close to 95
    sum(map(within_confidence_interval_gumbel, range(100)))

#    cg, ct, i = 0, 0, 0
#    N = 100
#    while i < N:
#        p90, _, _, Rg, Rt = conf_interval()
#        if Rg[0] <= p90 <= Rg[1]: cg += 1
#        if Rt[0] <= p90 <= Rt[1]: ct += 1
#        i += 1
#    print(cg/i, ct/i)
