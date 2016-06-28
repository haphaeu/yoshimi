# -*- coding: utf-8 -*-
"""

Monte carlo simulation of random inputs.
Inputs can be normal or gumbel distributed.
A flexible number of inputs can be set.

Pass a function to convert the set of inputs into an output.

Monte Carlo method uses a large number of sets of inputs and creates
a sample of output. The output sample is looked at as a statistical
distribution.



Created on Mon Dec 14 20:09:28 2015

@author: raf
"""
from scipy import stats as ss
from scipy import euler_gamma
from math import gamma
import numpy as np
from numpy import sqrt, pi, sign
from matplotlib import pyplot as plt


class weibull():
    def weibull_parameters(self, mean, stdev, loc):
        """Given the distribution mean, standard deviation and
        location, returns the Weibull shape and scale parameters.
        """
        mean -= loc
        shape0 = 0.1
        step = 1
        erro1 = 99
        i = 0
        while i < 1000:
            scale0 = mean / gamma(1 + 1 / shape0)
            scale1 = stdev / sqrt(gamma(1 + 2 / shape0) - gamma(1 + 1 / shape0)**2)
            erro0 = erro1
            erro1 = scale0 - scale1
            if abs(erro1) < 1e-8: break  # tolerance for the solver
            if not sign(erro0) == sign(erro1): step /= -2
            shape0 += step
            i += 1
        return (shape0, scale0, erro1)

    def __init__(self, mean, stdev, loc=0):
        self.loc = loc
        self.shape, self.scale, err = self.weibull_parameters(mean, stdev, loc)

    def rvs(self, size):
        # This is working and matching the spreadsheet
        # But not sure why _min had to be used here...
        return ss.weibull_min(c=self.shape, loc=self.loc, scale=self.scale).rvs(size=size)


class Input():
    """Defines one input, given a name, mean, stdev and the type of
    distribution.
    !
    Maybe need to think in other ways to define an input, i.o. mean and stdev,
    it could be flexible to input other parameters, for example P90.
    !
    """
    def __init__(self, mean, stdev, dtype='normal', weib_loc=0):
        if dtype == 'normal':
            self.dist = ss.norm(loc=mean, scale=stdev)
        elif dtype == 'gumbel_r':
            beta = stdev*sqrt(6)/pi
            mu = mean - euler_gamma * beta
            self.dist = ss.gumbel_r(loc=mu, scale=beta)
        elif dtype == 'gumbel_l':
            beta = stdev*sqrt(6)/pi
            mu = mean + euler_gamma * beta
            self.dist = ss.gumbel_l(loc=mu, scale=beta)
        elif dtype == 'weibull':
            self.dist = weibull(mean, stdev, weib_loc)
        else:
            print('Error dtype.')


class InputSet():
    """Gathers a set of Input-class variables and calculated a sample of
    input sets.
    """
    def __init__(self, list_inputs, sample_size):
        self.num_inputs = len(list_inputs)
        self.sample_size = sample_size
        self.inputs = list_inputs
        self.set_rvs(size=sample_size)

    def set_rvs(self, size=1):
        rvs = np.zeros((self.num_inputs, size))
        for i, inp in enumerate(self.inputs):
            rvs[i] = inp.dist.rvs(size=size)
        self.rvs = rvs


class MonteCarlo():
    """Monte Carlo method using a sample of input sets from the class InputSet.
    The argument 'funtion' must be a function returning a single value.
    A set of single-values is calculated and statistics calculated for it.
    """
    def __init__(self, input_set, function):
        self.sample = np.fromiter(map(function, *input_set.rvs), float)
        self.mean = self.sample.mean()
        self.std = self.sample.std()
        self.size = len(self.sample)

    def hist(self, bins=10, show=False):
        plt.hist(self.sample, bins=bins, normed=True)
        if show: plt.show()

    def fractile(self, confidence):
        if 1/(1-confidence) > self.size:
            print('Sample too small.')
            return 0
        return sorted(self.sample)[int(round(confidence*self.size, 0))]


def dummy_calc(*args):
    # must return one value
    return (args[0]+args[1])*args[2]

if __name__ == '__main__':

    w = weibull(10, 1)

    samples = int(1e6)

    input1 = Input(5.2, 1, 'gumbel_r')
    input2 = Input(14, 3, 'normal')
    input3 = Input(100, 2, 'weibull', 1)
    input_set = InputSet((input1, input2, input3), samples)
    mc = MonteCarlo(input_set, dummy_calc)
    mc.hist(bins=100, show=True)
    print('Mean: %.2f\nStDev: %.2f\nP50: %.2f\nP90: %.2f' % (mc.mean, mc.std, mc.fractile(0.5),
                                                             mc.fractile(0.9)))
