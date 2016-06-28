# -*- coding: utf-8 -*-
"""
Created on Mon Jan 05 13:24:41 2015

@author: rarossi
"""
import scipy as sp
from scipy import stats
def printppf(model, rv):
    print '%s\t%.2f\t%.2f\t%.2f\t%.2f' % (model, rv.ppf(0.9),rv.ppf(0.99),rv.ppf(0.999),rv.ppf(0.9999))
    
data = sp.loadtxt('data25h.txt',skiprows=1, usecols= (1,))
data -= data.mean()

print 'Model\t90%\t99%\t99.9%\t99.99%'

l, s = stats.rayleigh.fit(data)
ray = stats.rayleigh(scale=s, loc=l)
printppf('Rayleigh', ray)

sp, l, s = stats.weibull_max.fit(data)
wei = stats.weibull_max(scale=s, loc=l, c=sp)
printppf('Weibull', wei)

l, s = stats.gumbel_r.fit(data)
gum = stats.gumbel_r(scale=s, loc=l)
printppf('Gumbel',gum)