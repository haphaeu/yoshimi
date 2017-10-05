# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 19:12:01 2017

@author: raf
"""
import numpy as np


def quantile(k, n, approach=1):
    """Returns the quantile of rank k of a sample with size n.

    1 <= k <= n

    k can be an iterable.

    Approach 1:
            q = (k-0.5)/n

    Approach 2:
            q = k/(n+1)
    """
    if hasattr(k, '__iter__'):
        if not isinstance(k, np.ndarray):
            k = np.array(k)
        assert all(k > 0), 'Rank must be larger than zero.'
        assert all(k <= n), 'Rank must be less than or equal to the sample size.'
    else:
        assert k > 0, 'Rank must be larger than zero.'
        assert k <= n, 'Rank must be less than or equal to the sample size.'

    if approach == 1:
        return (k-0.5)/n
    else:
        return k/(n+1)


def rank(q, n, approach=1, interval=False):
    """Inverse of the function quantile.

    Note that this is an one based rank:

        1 <= k <= n
    """
    if hasattr(q, '__iter__'):
        if not isinstance(q, np.ndarray):
            q = np.array(q)
        assert all(q > 0), 'Quantiles must be larger than zero.'
        assert all(q < 1), 'Quantiles must be larger than zero.'
    else:
        assert q > 0, 'Quantiles must be larger than zero.'
        assert q < 1, 'Quantiles must be larger than zero.'

    def _rank(_q):
        if approach == 1:
            return _q*n+0.5
        else:
            return _q*(n+1)

    if not interval:
        return np.round(_rank(q)).astype(int)
    else:
        s = (1-q)/2
        qlo, qhi = s, 1-s
        return np.array(np.round(list(map(_rank, (qlo, qhi)))), dtype=int)

def quantiles(n, approach=1):
    """Return all quantiles of a sample of size n.
    See quantile() for a description of the approaches.
    """
    ranks = np.array((range(1, n+1)))
    return quantile(ranks, n, approach)

def survivals(n, approach=1):
    """Return 1 - quantiles()"""
    return 1 - quantiles(n, approach)

def llquantiles(n, approach=1):
    """Return -log(-log(quantiles()))"""
    return -np.log(-np.log(quantiles(n, approach)))

def llsurvivals(n, approach=1):
    """Return -log(-log(survivals()))"""
    return -np.log(-np.log(survivals(n, approach)))
