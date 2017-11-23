# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:46:53 2015

@author: rarossi

see spreadsheet 'Flooded member drain.xlsx' in Docs/Technical
"""

pi    =  3.141592653589793
g     =  9.806     # m/s^2
ID    =  0.35      # m - hollow beam ID
delta =  0.001     # m - orifice diameter
num   =  100         # number of orifices
h     = 16         # m - water column height
dt    =  10       # s
t     =  0.0       # s
plot=True
if plot:
    from matplotlib import pyplot as plt
    ts, hs = [0], [h]
while h>0.01:
    t+=dt
    h-=dt*(2*g*h)**0.5*num*delta**2/ID**2
    if plot:
        ts.append(t)
        hs.append(h)
print('%.1f seconds to empty the pipe' % t)
if plot: plt.plot(ts, hs)