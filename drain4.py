# -*- coding: utf-8 -*-
"""
Time to drain the water from a horizontal pipe through an orifice at the bottom.

[1] http://www.codecogs.com/library/engineering/fluid_mechanics/orifice/flow_from_tanks/circular-horizontal.php

Created on Thu Dec 14 07:31:42 2017

@author: rarossi
"""
import numpy as np
from numpy import pi
from matplotlib import pyplot as plt

# gravity
g = 9.806


def chord(r, d):
    """Return the length of the chord of a circle of radius r at a distance d
    from the centre."""
    return 2 * r * (1 - (d/r)**2)**0.5


def fill_ratio(r, h):
    """Horizontal pipe of radius r, filled with water at a height h.
    Return the water fill ratio"""
    c = chord(r, h-r)
    theta = 2 * np.arcsin(c / (2*r))
    factor = (theta - np.sin(theta)) / (2*pi)
    return factor if h < r else 1-factor


class msls_pipe():
    def __init__(self, OD, WT, lo, do, l, Cd):
        self.OD = OD                       # mm
        self.WT = WT                       # mm
        self.ID = OD - 2*WT                # mm
        self.R = self.ID/2000              # m
        self.lo = lo/1000                  # m
        self.do = do/1000                  # m
        self.a = (lo*do + pi/4*do**2)/1e6  # m2
        self.l = l/1000                    # m
        self.Cd = Cd
        self.calc_plot_data()
        
    def calc_plot_data(self):
        self.h = np.linspace(2*self.R, 0, 100)
        self.m = np.array([1-fill_ratio(self.R, x) for x in self.h])
        self.t = np.array([self.drain_time(x, 0) for x in self.h])
        
    def drain_time(self, h1=-99, h2=0.0):
        if h1 == -99:
            h1 = 2 * self.R
        l, Cd, a, R = self.l, self.Cd, self.a, self.R
        return 4*l / (3*Cd*a*(2*g)**0.5) * ((2*R-h2)**1.5 - (2*R-h1)**1.5)
    
    def table(self, header=False):
        x = np.array([1, 0.75, 0.5, 0.25])
        h = 2 * self.R * x
        t = [self.drain_time(_, 0) for _ in h]
        if header:
            print('OD', end='')
            for _ in x:
                print('\th%.2f' % _, end='')
            for _ in x:
                print('\tm%.2f' % _, end='')
            print('')
        print('%d' % self.OD, end='')
        for _ in t:
            print('\t%.2f' % _, end='')
        for _ in x:
            print('\t%.2f' % self.t[np.argmin(np.abs(self.m-(1-_)))], end='')
        print('')

    def plot_height(self):
        plt.plot(self.t, 1-self.h/max(self.h), label='%dmm' % self.OD)
        plt.title('Draining MSLS pipe')
        plt.xlabel('Time [s]')
        plt.ylabel('Water height / diameter')
        plt.yticks([0, 0.25, 0.5, 0.75, 1])
        plt.grid(b=True)        
        plt.legend(loc='best')

    def plot_mass(self):
        plt.plot(self.t, self.m, label='%dmm' % self.OD)
        plt.title('Draining MSLS pipe')
        plt.xlabel('Time [s]')
        plt.ylabel('Mass of water filling ratio')
        plt.yticks([0, 0.25, 0.5, 0.75, 1])
        plt.grid(b=True)        
        plt.legend(loc='best')


p324 = msls_pipe(323.9, 15.88, 145, 45, 1355, 0.8)
p406 = msls_pipe(406, 19.05, 160, 60, 1340, 0.8)
p508 = msls_pipe(508, 19.05, 190, 70, 1310, 0.8)
#p660 = msls_pipe(660, 25.4, 190, 70, 1310, 0.8)  # orifice TBC

p324.plot_height()
p406.plot_height()
p508.plot_height()
#p660.plot_height()
plt.show()

p324.plot_mass()
p406.plot_mass()
p508.plot_mass()
#p660.plot_mass()
plt.show()

print('\nHeight and mass filling ratios')
#p660.table(header=True)
p508.table(header=True)
p406.table()
p324.table()

p406.drain_time(p406.R, 0)
