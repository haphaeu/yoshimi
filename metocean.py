# -*- coding: utf-8 -*-
"""

Metocean scatter diagram for Åsgard given as joint Hs Tp probability.


TODO:
    - implement joint CDF(Hs, Tp)
      need to think how to use this in practice
    - read weather window, return operability

Created on 2018 2 Feb Fri 14:53:20
@author: rarossi
"""

from scipy import stats as ss
import numpy as np
import scipy as sp
from math import pi, sqrt, exp, log
import matplotlib.pyplot as plt

# #####################################################################
# Åsgard metocean
# annual omni direction joint distribution Hs, Tp
gamma, theta, eta, zeta, nu = 1.35, 2.513, 4.691, 0.563, 0.818
a1, a2, a3, b1, b2, b3 = 1.713, 0.396, 0.39, 0.005, 0.086, 0.28
# #####################################################################


def f_Hs(hs):
    """Probability density function of Hs."""
    if hs < 1e-3:
        return 0
    elif hs <= eta:
        return 1/(hs*zeta*sqrt(2*pi))*exp(-((log(hs)-nu)**2)/(2*zeta**2))
    else:
        return gamma/theta*(hs/theta)**(gamma-1)*exp(-(hs/theta)**gamma)


def F_Hs(hs):
    """Cumulative probability function of Hs"""
    return sp.integrate.quad(f_Hs, 0, hs)[0]


def f_Tp_Hs(tp, hs):
    """Probability density function of Tp conditioned to Hs."""
    mi = a1 + a2 * hs**a3
    sigma = sqrt(b1 + b2 * exp(-b3*hs))
    return 1/(tp*sigma*sqrt(2*pi))*exp(-((log(tp)-mi)**2)/(2*sigma**2))


def f_HsTp(hs, tp):
    """Joint probability density function for Hs and Tp."""
    return f_Hs(hs) * f_Tp_Hs(tp, hs)


# plot PDF of Hs
x = np.linspace(0.1, 10, 100)
y = np.array([f_Hs(hs) for hs in x])
plt.plot(x, y)
plt.title('PDF of Hs')
plt.show()


# plot PDF of Tp for a few Hs
x = np.linspace(3, 20, 100)
for hs in [1.5, 2.5, 3.5]:
    plt.plot(x, np.array([f_Tp_Hs(tp, hs) for tp in x]), label='%.1f' % hs)
plt.legend()
plt.title('PDF of Tp for some Hs')
plt.show()
