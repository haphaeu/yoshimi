# -*- coding: utf-8 -*-
"""

Assess the relationship between a p99 and p90 values for a Gumbel
distribution.

Conclusion: the ratio of p99 over p90 depends on the ratio of the
distribution's scale parameter over the location parameter.

scale/location    p99/p90 ratio
    2%               1.05
    5%               1.10
   10%               1.20


Running over an analysis sample, the ratio seems to be around 1.10.


Created on Tue Jul 17 11:03:13 2018

@author: rarossi
"""
import scipy.stats as ss
import pandas as pd
dist = ss.gumbel_r


def rvs():
    num = 10
    locs = [100, 500, 1000, 5000]
    fscales = [0.02, 0.05, 0.1]

    print('loc \t ', end='')
    for f in fscales:
        print(f, end='\t')
    print()

    for loc in locs:
        print(loc, end='\t')
        for f in fscales:
            scale = f * loc
            ave = 0
            for i in range(num):
                sample = dist.rvs(size=50, loc=loc, scale=scale)
                gd = dist(*dist.fit(sample))
                p90, p99 = gd.ppf([0.9, 0.99])
                ave += p99/p90
                # print('\t 90%%: %.2f \t 99%%: %.2f \t ratio: %.2f' % (p90, p99, p99/p90))
            ave /= num
            print('%.2f' % ave, end='\t')
        print()

    '''
    out:
    loc      0.02   0.05    0.1
    100     1.04    1.11    1.19
    500     1.05    1.10    1.19
    1000    1.04    1.11    1.19
    5000    1.05    1.11    1.19
    '''


def sample_fit():
    file = (r'M:\Distributed_Orcaflex\Stavanger\devel\crane_load_criterion'
            r'\ITS splash zone - 18m radius\results.txt')
    var = 'Winch1 Max Tension'
    sample = pd.read_table(file)

    print('\nHs\\Tp', end='')
    for tp in set(sample.WaveTp):
        print('%6.1f' % tp, end='')

    hss = list(set(sample.WaveHs))
    hss.sort()
    for hs in hss:
        print('\n%5.2f' % hs, end='')
        for tp in set(sample.WaveTp):
            spli = sample[(sample.WaveHs == hs) & (sample.WaveTp == tp) &
                          (sample.WaveDirection == 195)][var]
            if not spli.empty:
                gd = dist(*dist.fit(spli))
                p90, p99 = gd.ppf([0.9, 0.99])
                print('%6.02f' % (p99/p90), end='')
            else:
                print('%6s' % '-', end='')
    '''out:
Hs\Tp   3.0   4.0   5.0   6.0   7.0   8.0   9.0  10.0  11.0  12.0  13.0  14.0
 1.00  1.05     -     -     -     -     -     -     -     -     -     -     -
 1.40     -  1.08     -     -     -     -     -     -     -     -     -     -
 1.60     -  1.08     -     -     -     -     -     -     -     -     -     -
 1.70     -  1.08     -     -     -     -     -     -     -     -     -     -
 1.80     -     -     -  1.07  1.09  1.09  1.08  1.07     -     -     -     -
 1.90     -     -     -     -     -  1.09  1.08     -     -     -     -     -
 2.00     -     -     -  1.08  1.09  1.09  1.09  1.07     -     -     -     -
 2.10     -     -     -  1.08  1.07     -     -  1.07     -     -     -     -
 2.20     -     -  1.07  1.10  1.08  1.10  1.10  1.08  1.07  1.09  1.08  1.08
 2.30     -     -  1.07     -     -     -     -     -  1.08  1.09  1.09     -
 2.40     -     -  1.08     -     -     -     -     -  1.08  1.09  1.09  1.08
 2.50     -     -     -     -     -     -     -     -     -     -     -  1.08
 2.60     -     -     -  1.14  1.14  1.13  1.12  1.09  1.09  1.10  1.10  1.09
 '''


def sample_empirical():
    file = (r'M:\Distributed_Orcaflex\Stavanger\devel\crane_load_criterion'
            r'\ITS splash zone - 18m radius\results.txt')
    var = 'Winch1 Max Tension'
    sample = pd.read_table(file)

    print('\nHs\\Tp', end='')
    for tp in set(sample.WaveTp):
        print('%6.1f' % tp, end='')

    hss = list(set(sample.WaveHs))
    hss.sort()
    for hs in hss:
        print('\n%5.2f' % hs, end='')
        for tp in set(sample.WaveTp):
            spli = sample[(sample.WaveHs == hs) & (sample.WaveTp == tp) &
                          (sample.WaveDirection == 195)][var]
            if not spli.empty:
                p90, p99 = spli.quantile([0.9, 0.99])
                print('%6.02f' % (p99/p90), end='')
            else:
                print('%6s' % '-', end='')
    '''out:
Hs\Tp   3.0   4.0   5.0   6.0   7.0   8.0   9.0  10.0  11.0  12.0  13.0  14.0
 1.00  1.06     -     -     -     -     -     -     -     -     -     -     -
 1.40     -  1.09     -     -     -     -     -     -     -     -     -     -
 1.60     -  1.05     -     -     -     -     -     -     -     -     -     -
 1.70     -  1.04     -     -     -     -     -     -     -     -     -     -
 1.80     -     -     -  1.10  1.08  1.13  1.07  1.08     -     -     -     -
 1.90     -     -     -     -     -  1.13  1.07     -     -     -     -     -
 2.00     -     -     -  1.05  1.05  1.12  1.06  1.08     -     -     -     -
 2.10     -     -     -  1.07  1.09     -     -  1.10     -     -     -     -
 2.20     -     -  1.04  1.12  1.07  1.10  1.06  1.12  1.04  1.04  1.04  1.06
 2.30     -     -  1.12     -     -     -     -     -  1.04  1.04  1.04     -
 2.40     -     -  1.25     -     -     -     -     -  1.03  1.04  1.04  1.06
 2.50     -     -     -     -     -     -     -     -     -     -     -  1.06
 2.60     -     -     -  1.12  1.15  1.12  1.05  1.16  1.02  1.03  1.05  1.06
'''


if __name__ == '__main__':
    rvs()
    sample_fit()
    sample_empirical()
