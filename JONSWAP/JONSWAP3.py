'''
JONSWAP.py

- Calculates the JONSWAP spectrum
- Discretisation of the spectrum in frequency domain
- Build the wave components
- Calculate the resultant wave train

Inputs:
- Wave height
- Wave zero up crossing period
- Frequency domain
- Time domain
- Initial phases of wave components

'''
import numpy as np
from numpy import pi, exp, log, sqrt

g = 9.806  # m/s2 - gravity


def angular_frequency_domain(wo, wf, num=100):
    """Return array of angular frequency from wo to wf with num points."""
    return np.geomspace(wo, wf, num)


def gamma_DNV(hs, tp):
    """JONSWAP gamma as per DNV-H103"""
    if hs < 0.1:
        return 1.0
    alpha = tp/sqrt(hs)
    if alpha >= 3.6 and alpha <= 5.0:
        return exp(5.75-1.15*alpha)
    if alpha < 3.6:
        return 5.0
    if alpha > 5.0:
        return 1.0


def spectral_moment(S, w, m=0):
    """Return mth spectral moment of S(w)."""
    return np.trapz(S * w**m, w)


def jonswap(Hs, Tp, w, fgamma=gamma_DNV):
    """JONSWAP spectrum [m².rd/s].

    Hs: significant wave height

    Tp: peak period

    w: angular frequency domain [rd/s]

    fgamma: function of (Hs, Tp) to calculate JONSWAP gamma factor
    """

    wp = 2 * pi / Tp  # rd/s
    gamma = fgamma(Hs, Tp)
    alpha = 5 / 16 / g**2 * Hs**2 * wp**4 * (1 - 0.287 * log(gamma))
    sigma = np.where(w < wp, 0.07, 0.09)
    S = (
            alpha * g**2 / w**5 * exp(-5.0 / 4.0 * (wp / w)**4.0) *
            gamma**exp(-0.5 * (w - wp)**2 / (sigma * wp)**2)
         )

    return S


def test():
    w = angular_frequency_domain(2*pi/25, 2*pi/2)
    Hs = 2.5
    S = jonswap(Hs, 10, w)
    assert abs(Hs - 4*sqrt(spectral_moment(S, w))) < 1e-2
