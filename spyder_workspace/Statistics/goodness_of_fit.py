# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:07:01 2016

@author: rarossi
"""
from numpy import log, linspace
from scipy import stats as ss
from matplotlib import pyplot as plt

good_sample = (7.70918,
                7.764769,
                7.803875,
                7.831189,
                7.874452,
                8.010608,
                8.017121,
                8.158852,
                8.244635,
                8.313324,
                8.410653,
                8.466218,
                8.528385,
                8.639894,
                8.75744,
                8.762812,
                8.811596,
                8.854147,
                8.942195,
                8.947851,
                8.99963,
                9.105935,
                9.240189,
                9.315297,
                9.681533)
plt.plot(good_sample,
         -log(-log(linspace(1/len(good_sample), (len(good_sample)-1)/len(good_sample),
         len(good_sample)))), '*')

bad_sample = (8.198005,
                8.317582,
                8.322514,
                8.348242,
                8.356763,
                8.428341,
                8.441114,
                8.479216,
                8.479752,
                8.512101,
                8.523893,
                8.625937,
                8.630313,
                8.639903,
                8.651816,
                8.653922,
                8.716469,
                8.991851,
                9.162272,
                10.1382,
                10.530066,
                10.670705,
                11.318553,
                12.906569,
                13.87566)
plt.plot(bad_sample,
         -log(-log(linspace(1/len(bad_sample), (len(bad_sample)-1)/len(bad_sample),
         len(bad_sample)))), '*')

##
## Using Kolmogorov-Smirnov test
## The D statistic is the absolute max distance (supremum) between the CDFs of the two samples.
## The closer this number is to 0 the more likely it is that the two samples were drawn from the
## same distribution.
## The p-value returned by the k-s test has the same interpretation as other p-values. You reject
## the null hypothesis that the two samples were drawn from the same distribution if the p-value
## is less than your significance level. You can find tables online for the conversion of the
## D statistic into a p-value if you are interested in the procedure.
##
##
stats, pvalue = ss.kstest(rvs=good_sample, cdf=ss.gumbel_l(*ss.gumbel_l.fit(good_sample)).cdf)
print('The maximumdistance between CDFs is %.2f.' % stats, end='')
print('The sample is Gumbel distributed for a significance level of %.2f' % pvalue)

stats, pvalue = ss.kstest(rvs=bad_sample, cdf=ss.gumbel_l(*ss.gumbel_l.fit(bad_sample)).cdf)
print('The maximumdistance between CDFs is %.2f.' % stats, end='')
print('The sample is Gumbel distributed for a significance level of %.2f' % pvalue)

##
## Using Anderson-Darling test
## The assumption regarding the distribution of the sample is rejected if the output value
## is larger than the critical values for the required significance level.
## For gumbel distributions, the critical values and significance levels are:
##     [0.456, 0.612, 0.728, 0.843, 0.998]
##     [25.0, 10.0, 5.0, 2.5, 1.0]
## I.e, for a sample to be assumed Gumbel distributed with a significant level of 25%,
## the output values must be < 0.456.
##

stats, critical_values, sign_level = ss.anderson(good_sample, dist='gumbel')
if stats > max(critical_values):
    print('Sample is not Gumbel distributed')
else:
    for i, cv in enumerate(critical_values):
        if stats < cv:
            print('Sample is gumbel distributed for a significance level of %d%%' % sign_level[i])
            break

stats, critical_values, sign_level = ss.anderson(bad_sample, dist='gumbel')
if stats > max(critical_values):
    print('Sample is not Gumbel distributed')
else:
    for i, cv in enumerate(critical_values):
        if stats < cv:
            print('Sample is gumbel distributed for a significance level of %d%%' % sign_level[i])
            break
