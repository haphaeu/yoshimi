# -*- coding: utf-8 -*-
"""

Example running OrcaFlex using multiprocessing.Pool.

This is simplest implementation if we don't care about "communicating"
with the simulations.

We just create a pool and send all the simulation there. The pool takes
care of chunking the number of jobs according to the number of processes.

The worker function could potentially trigger post-processing as well.

The disadvantage of using this is that we can't get thing back from the
processes to use further in the code. But generally for running sims this
is not needed.


Created on Wed Aug 30 08:14:10 2017

@author: rarossi
"""

from multiprocessing import Pool
import OrcFxAPI as of
from random import random


def f(Id):
    sim_t = 800 + random()*400
    print('Initialising id {} for {:.1f} s'.format(Id, sim_t))
    m = of.Model()
    m.general.StageDuration[1] = sim_t
    m.CreateObject(of.otLine)
    m.CreateObject(of.otVessel)
    print('Running id ', Id)
    m.RunSimulation()
    print('Done id ', Id)


if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(f, range(10))
    # difference between map and map_async is that async won't
    # wait for execution to finish. in this example this is not needed.
    # r = pool.map_async(f, range(10))
    # r.wait()
