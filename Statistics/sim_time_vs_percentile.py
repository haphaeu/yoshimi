# -*- coding: utf-8 -*-
"""
Check hipothesis that the P90 of a X minutes operation can be calculated based on Y minutes
simulations, Y > X by correcting the percentile to 0.9**(Y/X)

Created on Fri Apr 15 13:31:20 2016

@author: rarossi
"""
import OrcFxAPI as of
from scipy import stats as ss

m = of.Model()
m.general.StageDuration[1] = 10800
m.environment.WaveType = 'JONSWAP'
m.environment.UserSpecifiedRandomWaveSeeds = 'Yes'

seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sample3h = []
for seed in seeds:
    print('Running seed {0}'.format(seed))
    m.environment.WaveSeed = seed
    m.RunSimulation()
    sample3h.append(m.environment.AnalyseExtrema('Elevation',
                                                 period=1,
                                                 objectExtra=of.oeEnvironment((0, 0, 0))).Max)

m.general.StageDuration[1] = 1800
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
sample10min = []
for seed in seeds:
    print('Running seed {0}'.format(seed))
    m.environment.WaveSeed = seed
    m.RunSimulation()
    sample10min.append(m.environment.AnalyseExtrema('Elevation',
                                                    period=1,
                                                    objectExtra=of.oeEnvironment((0, 0, 0))).Max)

print('P90 from 3h simulations: %.2f' % (ss.gumbel_r(*ss.gumbel_r.fit(sample3h)).ppf(0.9)))
corr_p = 0.9**(180/30)
print('Corrected percentile for 30min operation: %.2f' % corr_p)
print('P%d from 3h simulations: %.2f' % (100*corr_p,
                                         ss.gumbel_r(*ss.gumbel_r.fit(sample3h)).ppf(corr_p)))
print('P90 from 30min simulations: %.2f' % (ss.gumbel_r(*ss.gumbel_r.fit(sample10min)).ppf(0.9)))
