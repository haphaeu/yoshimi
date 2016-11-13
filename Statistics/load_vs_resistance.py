# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 13:07:02 2015

@author: rarossi

A structure will fail if subjected to a load greater then its own resistance:
failure := load > resistance
We can safely assume that the load and the resistance are independent.
By means of probability density functions (pdf) and cumulative density
functions (cdf) of the load and of the resistance, is it correct to say that
the probability of failure, can be calculated by the integral of
load_pdf * resistance_cdf ?

Confirmed at
http://stats.stackexchange.com/questions/183743/probability-of-failure
"""
import numpy as np
import scipy as sp
from scipy import stats as ss
from matplotlib import pyplot as plt


# %%
# This below double checks the p_failure calcs.
# Calculate the probability of failure as the integral of the convolution
# of load_pdf and resistance_pdf.
# see http://stats.stackexchange.com/questions/183743/probability-of-failure
# ==> I'm sure this could be done using the numpy convolve function but I
# still don't know how to do it.
def pfail_dblchk(fl, fr, x):
    """fl, fr: pdf functions of load and resistance
    x: domain
    return the probability of failure
    """
    return sp.integrate.quad(
          lambda tau: sp.integrate.cumtrapz(fl(x)*fr(tau+x), dx=x[1]-x[0])[-1],
          x[0]-(x[-1]-x[0]), 0)[0]
# %% #########################################################


def pfail(fl, Fr, x, dx):
    """Probability of failue given load and resistance.
    pfail = integral of load_pdf * resistance_cdf
    fl: pdf function of the load
    Fr: cfd function of the resistance
    x, dx: domain
    """
    return sp.integrate.cumtrapz(fl(x)*Fr(x), dx=dx)[-1]
# %%


def optimize_loc(res_loc, res_scale, load_distro, conf_target, eps):
    """Auxiliary function to be used with the scipy.optimize.bisect function
    to find the location parameters of the resistance distribution that
    matches a required confidence level.
    res_loc, res_scale: locations and scale parameters of the distribution
    load_distro: load distribution (frozen scipy.stats distribution)
    conf_target: confidence level target
    eps: limit integration domain where load and resistance pdfs are > eps"""
    res_distro = ss.gumbel_l(loc=res_loc, scale=res_scale)
    x, dx = np.linspace(
                   min(load_distro.ppf(eps), res_distro.ppf(eps)),
                   max(load_distro.ppf(1-eps), res_distro.ppf(1-eps)),
                   2000, retstep=True)
    confidence = 1.0 - pfail(load_distro.pdf, res_distro.cdf, x, dx)
    return confidence - conf_target
# %%


if __name__ == '__main__':
    # input data
    conf_target = 0.99  # confidence level of non-failure
    load_loc = 100          # location parameter for the load distribution
    load_scale = 10      # scale parameter for the load distribution
    res_scale = 8     # scale parameter for the resistance distribution
    eps = 1e-3           # domain = pdf > eps, for load and resistance

    # frozen load distribution
    load_distro = ss.gumbel_r(loc=load_loc, scale=load_scale)
    # finds the location parameter for the resistance distribution that
    # gives the required conf_target
    res_loc = sp.optimize.bisect(optimize_loc, load_loc,
                                 load_distro.ppf(1-eps),
                                 args=(res_scale, load_distro,
                                       conf_target, eps))
    # frozen resistance distribution
    res_distro = ss.gumbel_l(loc=res_loc, scale=res_scale)
    # recalculates the domain and the confidence level
    x, dx = np.linspace(min(load_distro.ppf(eps), res_distro.ppf(eps)),
                        max(load_distro.ppf(1-eps), res_distro.ppf(1-eps)),
                        200, retstep=True)
    confidence = 1.0 - pfail(load_distro.pdf, res_distro.cdf, x, dx)
    # %% plotting
    plt.plot(x, load_distro.pdf(x), label='load pdf')
    plt.plot(x, res_distro.pdf(x), label='resistance pdf')
    plt.grid()
    plt.title('Load x Resistance')
    plt.legend(loc='best')
    plt.xticks(())
    plt.yticks(())
    plt.show()

    print('Confidence %.3f%%' % (100*confidence))
    pfailure = pfail_dblchk(load_distro.pdf, res_distro.pdf, x)
    print('Dbl check %.3f%%' % (100*(1-pfailure)))


"""
Tentando resolver integral load_pdf * res_cdf analiticamente...

\\
\\\text{Assuming Gumbel distribution.} \\
f: PDF \\
F: CDF \\
\\\text{The load is likely to be right skewed:}
\\
f_l(x) = \frac{1}{\beta} e^{-(z+e^{-z})}  \\
F_l(x) = e^{-e^{-z}} \\
z = \frac{x-\mu}{\beta}
\\\\\text{The resistance is likely to be left skewed:} \\
f_r(x)= \frac{1}{\beta} e^{(z-e^z)}  \\
F_r(x) = 1 - e^{-e^z} \\
\\\\\text{The probability of failure is:} \\
p_{fail} = \int_{-\infty}^\infty f_{load}(x) F_{res} (x) dx \\
= \int_{-\infty}^\infty
                     \frac{1}{\beta_l} e^{-(z+e^{-z_l})}
                      \big( 1 - e^{-e^z_r} \big) dx \\
= \int_{-\infty}^\infty
                     \frac{1}{\beta_l} e^{-(\frac{x-\mu_l}{\beta_l}
                                           +e^{-\frac{x-\mu_l}{\beta_l}})}
                      \big( 1 - e^{-e^\frac{x-\mu_r}{\beta_r}} \big) dx
"""
