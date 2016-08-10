# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:14:20 2016

@author: rarossi
"""

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy import optimize as opt
import numpy as np


def myfun(X):
    x, y = X[0]+np.pi, X[1]+2*np.pi
    ret = x**2+150*np.abs(np.sin(3*x))+y**2
    return ret 


def surf(func):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.linspace(-10, 10, 100)
    Y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(X, Y)
    Z = func((X, Y))
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


#surf(myfun)

#ret = opt.differential_evolution(myfun, ((-10, 10), (-5, 5)))
#print('Minimum of {0:.2f} found at ({1:.3f}, {2:.3f})'.format(
#      ret['fun'], ret['x'][0], ret['x'][1]))

for i in range(10):
    ret = opt.basinhopping(myfun, (-900, 467), niter=100, disp=False)
    print('Minimum of {0:.2f} found at ({1:.3f}, {2:.3f}) - function calls {3}'.format(
          ret['fun'], ret['x'][0], ret['x'][1], ret['nfev']))

