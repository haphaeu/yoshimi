# -*- coding: utf-8 -*-
"""

Confidence Intervals

Calculate the confidence interval of a sample using a bootstrapping technique.

Future improvement: worth looking at cross-validation technique.

[1] https://ocw.mit.edu/courses/mathematics/18-05-introduction-to-probability-and-statistics-spring-2014/readings/MIT18_05S14_Reading24.pdf


Created on Thu Sep 28 15:26:26 2017

@author: rarossi
"""
import math
import numpy as np


# Seed for the random generator used in the resample function.
#
_random_seed = 12343


def confidence_interval(sample, ci=0.95, repeat=1000, relative=True):
    """Returns the lower and upper confidence intervals of a sample. The intervals can be
    relative or absolute, i.e: absolute = sample + relative

    The returned array has shape (2, len(sample)).

    The interval is calculated for a 100*ci % confidence level.

    Bootstrapping technique is used for the calculation of the intervals, using a sorted resampling
    with replacement.

    Arguments:
        sample      : array with the sample values
        ci          : confidence level of the interval
        repeat      : bootstrap size
        relative    : set to True for relative intervals, False for absolute intervals, i.e.,
                      absolute intervals = sample + relative_intervals.
                      relative intervals can be seen as tolerances to sample values, while
                      absolute intervals are lower and upper bounds for the variate values.
    """
    if not isinstance(sample, np.ndarray):
            sample = np.array(sample, dtype='float64')
    try:
        sample.sort()
    except (TypeError, ValueError):
        print('Error: sample must be an iterable.')
        return

    size = len(sample)
    m_star = np.zeros(shape=(repeat, size))
    np.random.seed(_random_seed)
    for i in range(repeat):
        m_star[i] = resample(sample)  # re-sampling with replacement
        m_star[i].sort()
    delta_star = m_star - sample
    delta_star.sort(axis=0)
    ci_idx = np.array([math.floor((1.0 - ci)/2*repeat), math.ceil(repeat - (1.0 - ci)/2*repeat)])
    return delta_star[ci_idx] + (0 if relative else sample)


def resample(sample, size=False, replacement=True):
    """Re-sample of sample.
    size        : size of the output re-sampled array. Set to False to use size of input sample.
    replacement : if True, the items are put back in the sample after each draw, i.e, the re-
                  sampled output array might have repeated items from the input sample.
                  if False, drawn items are discarded, i.e, the output array will not repeat items
                  from the input sample.
                  Bootstrap technique must use replacement.

    This technique uses random resampling. A random seed is set to make sure that calls of this
    function with same arguments will return the same intervals. To change the random seed, change
    the global parameter _random_seed and re-set np.random.seed(seed). Alternatively to have
    ramdom outputs, set np.random.seed(None).

    """
    sample_size = len(sample)
    if not size:
        size = sample_size
    if replacement:
        return sample[np.random.randint(0, sample_size, size)]
    else:
        assert size <= sample_size, "Re-sampling without replacement - size must be <= sample_size"
        idx = np.arange(sample_size)
        np.random.shuffle(idx)
        return sample[idx[:size]]


def cdf(size):
    """Returns the CDF for a t-distribution"""
    return np.linspace(0.5/size, (size-0.5)/size, size)


def llcdf(size):
    """Returns the -log(-log(CDF)) for a t-distribution"""
    return -np.log(-np.log(cdf(size)))


# ################################################################################################
# ### tests ###################################
# ################

_plot = False


def test_simple():
    """
    Simple test of the implementation of bootstrap to get confidence intervals.

    Creates a Gumbel distributed random sample, calculate the confidence interval for each
    item in the sample and show as error bars in a sample x log(log(cdf)) plot.
    """
    from scipy import stats as ss
    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = 10, 5
    
    ssz = 50
    sample = ss.gumbel_r.rvs(size=ssz, loc=100, scale=3)
    # sample = np.random.randint(1, 50, size=ssz)
    sample.sort()
    ci, nboots = 0.95, 1000
    err = confidence_interval(sample, ci, nboots)
    y = llcdf(ssz)

    plt.errorbar(sample, y, fmt='o', xerr=(-err[0], err[1]), ecolor='gray')
    plt.title('%d%% Confidence Intervals - Seeds %d\nBootstrapping %d samples' %
              (100*ci, ssz, nboots))
    plt.xlabel('Variate')
    plt.ylabel('-ln(-ln(cdf))')
    plt.grid()
    if not _plot: plt.close()
    plt.show()


def test_true():
    """
    This is a more complex of the confidence interval calculations implemented in this module.

    Here the confidence intervals of the confidence intervals are calculated.

    The sample confidence intervals are calcluated using the bootstrap method.

    The ci of the ci is calculated in a simplified manner just by repeating the process and
    looking at the spread of all trials. Maybe there's room for improvement here by using the
    same bootstrap technique at this step (this is addessed in test_true2() below).

    Here is what is implemented:

    1. Builds a large, size 50_000,  population based on a Gumbel distribution.

    2. Sub-sample this popuplation using sample size of around 50.

    3. For each sample, calculate the 95% confidence intervals and saves the P90 intervals.

    4. Repeat step 2-3 a number of times.

    5. Calculate statistics on the saved P90 intervals, like show lower and upper bounds and
       the 90% intervals, i.e., the 90% interval of the 95% intervals of P90.
    """
    from scipy import stats as ss
    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = 10, 5
    
    # Sample size
    ssz = 50

    # Population size
    psz = 50000

    # Confidence interval, Confidence interval of the confidence interval and bootstrap size
    ci, cici, nboots = 0.95, 0.9, 1000

    # Target percentile
    p_target = 0.9

    # Number of trials to repeat the bootstrap and to calculate the
    # confidence interval of the confidence intervals
    trials = 20

    assert psz > ssz, "Population size must be larger than sample size."
    assert 1/(1-p_target) < ssz, "Sample size not large enough for target percentile."
    assert 1/(1-cici) < trials, "Number of trials not large enough for confidence interval."

    # Switch off fix seed to have variability between runs
    np.random.seed(None)

    population = ss.gumbel_r.rvs(size=psz, loc=100, scale=3)
    plt.plot((min(population), max(population)), 2*[-np.log(-np.log(p_target))], 'r')
    x_target_trials = np.zeros(shape=(trials, 2))
    idx_p_target = int(np.ceil(p_target * ssz))
    y = llcdf(ssz)
    for i in range(trials):
        sample = resample(population, ssz, replacement=False)
        sample.sort()
        err = confidence_interval(sample, ci, nboots)
        x_target_trials[i] = (sample+err)[:, idx_p_target]
        plt.errorbar(sample, y, fmt='o', xerr=(-err[0], err[1]), ecolor='gray')
    plt.title('%d%% Confidence Intervals - Population %d - '
              'Sample size %d - Bootstrap %d samples' % (100*ci, psz, ssz, nboots))
    plt.xlabel('Variate')
    plt.ylabel('-ln(-ln(cdf))')
    plt.grid()
    if not _plot: plt.close()
    plt.show()
    lower = x_target_trials[:, 0]
    upper = x_target_trials[:, 1]
    lower.sort()
    upper.sort()
    ilow, iup = int(np.floor((1-cici)*trials)), int(np.ceil(cici*trials))
    print('%d %% Interval of the %d %% interval of P%d: %.2f - %.2f' %
          (100*cici, 100*ci, 100*p_target, lower[ilow], upper[iup]))


def test_true2():
    """
    See description of test_true() above.

    This is the same here, but using confidence_interval() again for the returned confidence
    interval.
    """
    from scipy import stats as ss
    from matplotlib import pyplot as plt
    plt.rcParams['figure.figsize'] = 10, 5
    
    # Sample size
    ssz = 50

    # Population size
    psz = 50000

    # Confidence interval, Confidence interval of the confidence interval and bootstrap size
    ci, cici, nboots = 0.95, 0.9, 1000

    # Target percentile
    p_target = 0.9

    # Number of trials to repeat the bootstrap and to calculate the
    # confidence interval of the confidence intervals
    trials = 20

    assert psz > ssz, "Population size must be larger than sample size."
    assert 1/(1-p_target) < ssz, "Sample size not large enough for target percentile."
    assert 1/(1-cici) < trials, "Number of trials not large enough for confidence interval."

    np.random.seed(None)
    population = ss.gumbel_r.rvs(size=psz, loc=100, scale=3)
    plt.plot((min(population), max(population)), 2*[-np.log(-np.log(p_target))], 'r')
    x_target_trials = np.zeros(shape=(trials, 2))
    idx_p_target = int(np.ceil(p_target * ssz))
    y = llcdf(ssz)
    for i in range(trials):
        sample = resample(population, ssz, replacement=False)
        sample.sort()
        err = confidence_interval(sample, ci, nboots)
        x_target_trials[i] = (sample+err)[:, idx_p_target]
        plt.errorbar(sample, y, fmt='o', xerr=(-err[0], err[1]), ecolor='gray')
    plt.title('%d%% Confidence Intervals - Population %d - '
              'Sample size %d - Bootstrap %d samples' % (100*ci, psz, ssz, nboots))
    plt.xlabel('Variate')
    plt.ylabel('-ln(-ln(cdf))')
    plt.grid()
    if not _plot: plt.close()
    plt.show()
    lower = x_target_trials[:, 0]
    upper = x_target_trials[:, 1]
    err_lower = confidence_interval(lower, ci=cici)
    err_upper = confidence_interval(upper, ci=cici)
    ilow, iup = int(np.floor((1-cici)/2*trials)), int(np.ceil((cici+(1-cici)/2)*trials))
    print('%d %% Interval of the %d %% interval of P%d: %.2f - %.2f' %
          (100*cici, 100*ci, 100*p_target, lower[ilow], upper[iup]))
