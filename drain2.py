# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:46:53 2015

@author: rarossi

see spreadsheet 'Flooded member drain.xlsx' in Docs/Technical

slightly reordered to input volume of water and output drainage over time
"""
from matplotlib import pyplot as plt
pi    =  3.141592653589793
g     =  9.806     # m/s^2
flood =  36        # te of water
delta =  0.001     # m - orifice diameter
num   =  400       # number of orifices
h0     = 16        # m - water column height
dt    =  1         # s
t     =  0.0       # s
ID    =  (4*flood/pi/1.025/h0)**0.5 # equiv ID to give flood water
time, drain = [0], [0]
h=h0
while h>0.01:
    t+=dt
    h-=dt*(2*g*h)**0.5*num*delta**2/ID**2
    time.append(t)
    drain.append(0.01*int(100*(h0-h)*1.025*pi/4*ID**2))
print '%.1f seconds to empty the pipe' % t
plt.plot(time, drain)
print('to drain 5 te took %.2fs' % time[drain.index(5)])