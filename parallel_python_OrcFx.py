"""
Created on Mon Nov 18 14:26:20 2013
@author: rarossi
"""
# Desc: This script demonstrates parallel runs with pp module and OrcFxAPI
# It calculates the output significant wave height ( 4*stDev ) for different 
# wave seeds for realizations of 200s duration, Hs of 2.5m and Tp of 10s.
# Parallel Python Software: http://www.parallelpython.com

import time, pp, OrcFxAPI

def runSeed(n):
    m=OrcFxAPI.Model()
    m.general.SetData('StageDuration',1,200)
    m.environment.SetData('WaveType',0,'Torsethaugen')
    m.environment.SetData('WaveHs',0,2.5)
    m.environment.SetData('WaveTp',0,10.0)
    m.environment.SetData('UserSpecifiedRandomWaveSeeds',0,'Yes')
    m.environment.SetData('WaveSeed',0,n)
    m.RunSimulation()
    tt=m.environment.TimeHistory('Elevation',
                                 OrcFxAPI.Period(1),
                                 OrcFxAPI.oeEnvironment(0,0,0))
    sz = len(tt)
    mean = sum(tt)/sz
    stdev = (sum((x-mean)**2 for x in tt) / (sz-1))**0.5
    Hs_chk = 4*stdev
    return Hs_chk

##############################################################################
##############################################################################

ncpus=2

ppservers = ()
job_server = pp.Server(ncpus, ppservers=ppservers)
print "Starting pp with", job_server.get_ncpus(), "workers"
start_time = time.time()
seeds = (5412, 8652, 3945, 1284, 5632, 1985, 8563, 1954,
          6548, 2197, 4652, 2598, 6548, 9754, 7652, 4895)
jobs = [(seed, job_server.submit(runSeed, (seed,), (), ("OrcFxAPI",))) for seed in seeds]

for input, job in jobs:
    print "For seed ", input, ", Hs is", job()

print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()
