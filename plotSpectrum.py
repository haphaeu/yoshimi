# -*- coding: utf-8 -*-
"""
Created on Fri Nov 08 15:19:22 2013

@author: rarossi
"""

from numpy import sin, pi
from pylab import plot, show, xlabel, ylabel, subplot, xlim
from scipy import fft, arange

def plotSpectrum(y,Fs,cutoff):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]   
    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')
    xlim(0,cutoff)

##############################################################################



Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = arange(0,1,Ts) # time vector

ff = 5;   # frequency of the signal
y = sin(2*pi*ff*t)

subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
plotSpectrum(y,Fs,10)
show()