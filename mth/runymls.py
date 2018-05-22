# -*- coding: utf-8 -*-
"""

Running OrcaFlex simulations using multiprocessing.Pool.

Use:

    run(ymls)
        Pass a list of yml files (or dat) and they'll be run and post processed

    run_missing(fname='missing.txt')
        Runs all files listed in fname.

    worker(yml)
        Internal worker function that runs the simulations. Don't call this function. It
        is called by the multiprocessing Pool.


Created on Thu May 03

@author: rarossi
"""

from multiprocessing import Pool, cpu_count
import OrcFxAPI as of
import os


def worker(yml):
    if not os.path.exists(yml):
        print('File not found %s' % yml)
        return False
    print('  Running %s' % yml)
    m = of.Model(yml)
    m.RunSimulation()
    m.ExecutePostCalculationActions(yml, of.atInProcPython)
    print('  Done    %s' % yml)
    return True


def run(ymls):
    pool = Pool(processes=cpu_count())
    print('Processing %d files using %d cpus.' % (len(ymls), cpu_count()))
    print(pool.map(worker, ymls))


def run_missing(fname='missing.txt'):
    if not os.path.exists(fname):
        print('File not found %s' % fname)
        return False
    with open(fname, 'r') as pf:
        ymls = pf.readlines()
    run([yml.strip() for yml in ymls])
    return True


if __name__ == '__main__':
    run_missing()
