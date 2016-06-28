'''
GumbleBootstrap.py

This script conducts a bootstrapping of extreme data from irregular wave
simulations using Gumble distribution to fit the statistical model and
Monte Carlo method to resample the data.

The objective is to evaluate the gain in running more seeds of irregular
wave simulations by means of comparing the uncertainty band from two sets
of analysis, one with 10 seeds, the other with 20 seeds.

Input data are:

- data     - extreme data from simulation - here representing different
             analysis seeds
- target_p - Gumble target percentile - here 90%
- N        - Number of bootstraps - large number (~10000) is less affected
             by the random nature of Monte Carlo method
- m        - Size of each bootstrap
             NOTE: to get the precise uncertainty band for a set of data,
             you need to use m = len(data). BUT you can simulate the gain
             wyou would have in running more seeds by using m larger than
             len(data).

Output:
after running, the script outputs a line like below

Data size: 20 - Bootstraps: 99000 - Gumble90%: 5070.7 - Uncertainty band: 560
Data size: 10 - Bootstraps: 99000 - Gumble90%: 5070.7 - Uncertainty band: 595

Due to the random nature of Monte Carlo, the script can be run a number of times
to get an idea of the random variation of the uncertainty band.

The uncertainty band is calculated by ignoring the lowest and the largest 5% of
the target percentile from all N bootstraps.

Note that many variables are being calculated and stored but not being output.
Check the script if you need more information.

References:
[1] email from Sverre Haver to Xiao Chen, 2013.02.10, "Bootstrapping"
[2] Sverre Haver - "Uncertainties when working with samples of limited size"
[3] "Stochastic Theory of Sealoads", Sverre Haver, NTNU, August 2005

Revision History
Rev      Date      Revision description
---   ----------   ------------------------------------------------------------
0.1   2013.02.13   First issue. No insanity check implemented.
                   Need to check correct use of m. (shoud m==sz?)
                   Using my own matrix.py as numpy is not available. This 
                   script could run much faster by using nympy arrays.
0.2   2013.02.21   Use m=len(data) to get uncertainty band of data. Or also
                   you can **estimate** the gain in increasing the number of
                   seeds by using m>len(data).
                   Bug: too much memory being allocated. To be checked.

Rafael Rossi
RaRossi@external.technip.com
rossirafael@yahoo.com
'''

from math import sqrt
from math import log
from math import pi
from random import random
from matrix import leastsquares
import sys
inGUI='idlelib.run' in sys.modules

def GumbleBootstrap(data, target_p, N, m):
    ###########################################################################
    # ##### CALCULATIONS

    #calculates the size, average and standard deviation of data
    sz    = len(data)
    mean  = sum(data)/sz
    # NOTE: excel uses (sz-1) method for StDev. Doing the same here.
    # Just change it to (sz) to use the other method.
    stdev = sqrt(sum((x-mean)**2 for x in data) / (sz-1))

    #Gumble parameters
    beta = stdev * sqrt(6.0) / pi
    mi   = mean - 0.5772 * beta

    #Target percentile in Gumble probability
    target_g = -log(-log(target_p))
    #Gumble 90% of data
    X_90p    =  beta * target_g + mi

    #create arrays with
    # probabilities p, Gumble probabilities g and simulated samples X
    if inGUI: print "Creating Monte Carlo samples"
    _prog = N/100
    p = []
    g = []
    X = []
    i=0
    while i<N:
        j=0
        tmpp=[]
        tmpg=[]
        tmpX=[]
        while j<m:
            rnd = random()
            tmpp.append(rnd)
            _ = -log(-log(rnd))
            tmpg.append(_)
            tmpX.append(beta*_+mi)
            j+=1
        p.append(tmpp)
        g.append(tmpg)
        tmpX.sort()
        X.append(tmpX)
        i+=1
        if not inGUI and not i%_prog:
            sys.stdout.write("1/2 Creating Monte Carlo samples %i%%\r" %
                             (i/_prog))

    #Simulate samples
    P = [i/(m+1.0) for i in range(1,m+1)]
    G = [-log(-log(_)) for _ in P]

    # fit least squares G as y and each column in X as x
    if inGUI: print "Fitting least squares"
    a=[0]*N
    b=[0]*N
    i=0
    for i in range(N):
        _ = leastsquares(X[i],G)
        a[i]=_[1]
        b[i]=_[0]
        if not inGUI and not i%_prog:
            sys.stdout.write("2/2 Fitting least squares %i%%         \r" %
                             (i/_prog))

    Xs_90p = [(target_g - b[i])/a[i] for i in range(N)]
    Xs_90p.sort()
    band = Xs_90p[95*N/100]-Xs_90p[5*N/100+1]

    print("Data size: %i - Bootstraps: %i - Gumble 90%%: %.2f - UncertBand: %.2f" %
          (sz, N,X_90p,band))
    return [X_90p, band]

###########################################################################
# ### MAIN 
# Gumble target percentile
target_p =  0.9
#number of bootstraps
N = 987123
#bootstrap size - using same size as sample, hard coded in function calls
######### COMPRESSOR MAX TENSION ##########################################
# extreme samples - as a list
data = [4339.976563, 4270.911621, 4995.431152, 4283.808105, 4262.713379,
        4381.712402, 4698.893555, 4961.325195, 5129.991699, 4862.354492,
        4624.565918, 4345.947266, 4477.729004, 4437.67334,  4236.550781,
        4110.188965, 4350.5625,   4627.514648, 5207.353027, 4354.126953]
print "*"*80
print "Compressor - Maximum effective tension at main connection"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)
######### COMPRESSOR MIN TENSION ##########################################
# extreme samples - as a list
data = [-984.6950,  -1204.1523, -850.5280,  -1189.3187, -756.0923,
        -415.9360,  -789.8019,  -427.0775,  -1169.0717, -927.9854,
        -1076.8383, -566.5051,  -1055.6049, -891.0147,  -779.6164,
        -1193.1031, -771.5768,  -1059.8966,  95.0703,   -462.8052]
print "*"*80
print "Compressor - Minimum effective tension at main connection"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)
######### COMPRESSOR SHEAR ##########################################
# extreme samples - as a list
data = [1431.8957, 1630.0894, 1464.1618, 1526.7459, 1765.3682,
        1709.0967, 1587.7972, 1571.9683, 1292.4624, 2120.9711,
        1574.5180, 1864.0572, 1570.9784, 1464.5363, 1411.2262,
        1676.5229, 2180.4785, 1601.3473, 2009.6282, 1621.8598]
print "*"*80
print "Compressor - Maximum shear force at main connection"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)
######### COMPRESSOR MOMENT ##########################################
# extreme samples - as a list
data = [8225.5127, 8297.4673, 8593.8542, 8971.3237, 9478.3166, 
        8950.1942, 8932.1757, 8828.7573, 7980.4684, 11750.4142, 
        9073.2825, 9726.2425, 8376.7581, 8393.4201, 8617.9011, 
        9495.9654, 10873.2136, 8352.7622, 10046.6398, 9398.6324]
print "*"*80
print "Compressor - Maximum bending moment at main connection"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)
######### COMPRESSOR PADEYE MAX TENSION ##########################################
# extreme samples - as a list
data = [1294.0143, 1345.4635, 1455.1007, 1336.6749, 1316.7030, 
        1298.8822, 1445.2759, 1404.2415, 1465.4714, 1597.8373, 
        1334.3900, 1332.4111, 1333.3663, 1370.8279, 1399.0524, 
        1361.9554, 1436.2157, 1412.2134, 1513.2198, 1307.8976]
print "*"*80
print "Compressor - Maximum effective tension at padeyes"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)
######### COMPRESSOR PADEYE MIN TENSION ##########################################
# extreme samples - as a list
data = [ -17.4435,   8.4811, -16.9382,  23.5891, 169.2133,
         126.2505, 146.0501, 156.8544, -84.9210, 108.3121,
         -60.1750, 226.3938, -50.6913,  93.8097,  24.5477,
         -15.9876,  44.4492, -11.0535, 199.9087, 131.6297]
print "*"*80
print "Compressor - Minimum effective tension at padeyes"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)
######### COMPRESSOR PADEYE SHEAR ##########################################
# extreme samples - as a list
data = [373.6528, 410.2533, 378.8976, 385.2573, 472.0238, 
        436.0278, 402.7468, 404.7263, 329.2544, 548.8464, 
        404.3984, 473.5333, 398.9153, 378.9018, 367.0016, 
        435.2415, 554.1097, 434.8316, 522.9304, 414.2979]
print "*"*80
print "Compressor - Maximum shear force at padeyes"
s10 = GumbleBootstrap(data[:10], target_p, N, 10)
s20 = GumbleBootstrap(data     , target_p, N, 20)
print "Uncertainty band reduction: %.2f%%" % ((1-s20[1]/s10[1])*100)

'''
RUN OUTPUT

THIS WAS RUN USING m=20 FOR BOTH SAMPLES
and number of boostraps arounf 1e6

C:\Users\rarossi\Documents\Python_Source_Codes\GumbleBootstrap>GumbleBootstrap.py
********************************************************************************
Compressor - Maximum effective tension at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 5070.67 - UncertBand: 595.41
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 4971.26 - UncertBand: 558.52
Uncertainty band reduction: 6.20%
********************************************************************************
Compressor - Minimum effective tension at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: -496.96 - UncertBand: 494.29
Data size: 20 - Bootstraps: 987123 - Gumble 90%: -387.61 - UncertBand: 573.93
Uncertainty band reduction: -16.11%
********************************************************************************
Compressor - Maximum shear force at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 1904.39 - UncertBand: 388.43
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 1958.65 - UncertBand: 402.57
Uncertainty band reduction: -3.64%
********************************************************************************
Compressor - Maximum bending moment at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 10384.79 - UncertBand: 1825.81
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 10341.69 - UncertBand: 1614.89
Uncertainty band reduction: 11.55%
********************************************************************************
Compressor - Maximum effective tension at padeyes
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 1521.81 - UncertBand: 166.11
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 1491.49 - UncertBand: 136.52
Uncertainty band reduction: 17.81%
********************************************************************************
Compressor - Minimum effective tension at padeyes
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 178.87 - UncertBand: 154.50
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 181.64 - UncertBand: 160.31
Uncertainty band reduction: -3.76%
********************************************************************************
Compressor - Maximum shear force at padeyes
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 493.32 - UncertBand: 104.42
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 505.36 - UncertBand: 104.46
Uncertainty band reduction: -0.04%

THIS WAS RUN USING m=size of sample

C:\Users\rarossi\Documents\Python_Source_Codes\GumbleBootstrap>GumbleBootstrap.py
********************************************************************************
Compressor - Maximum effective tension at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 5070.67 - UncertBand: 880.88
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 4971.26 - UncertBand: 558.96
Uncertainty band reduction: 36.55%
********************************************************************************
Compressor - Minimum effective tension at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: -496.96 - UncertBand: 728.40
Data size: 20 - Bootstraps: 987123 - Gumble 90%: -387.61 - UncertBand: 575.79
Uncertainty band reduction: 20.95%
********************************************************************************
Compressor - Maximum shear force at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 1904.39 - UncertBand: 572.79
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 1958.65 - UncertBand: 402.84
Uncertainty band reduction: 29.67%
********************************************************************************
Compressor - Maximum bending moment at main connection
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 10384.79 - UncertBand: 2684.16
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 10341.69 - UncertBand: 1613.69
Uncertainty band reduction: 39.88%
********************************************************************************
Compressor - Maximum effective tension at padeyes
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 1521.81 - UncertBand: 244.65
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 1491.49 - UncertBand: 136.64
Uncertainty band reduction: 44.15%
********************************************************************************
Compressor - Minimum effective tension at padeyes
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 178.87 - UncertBand: 227.69
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 181.64 - UncertBand: 160.46
Uncertainty band reduction: 29.52%
********************************************************************************
Compressor - Maximum shear force at padeyes
Data size: 10 - Bootstraps: 987123 - Gumble 90%: 493.32 - UncertBand: 153.86
Data size: 20 - Bootstraps: 987123 - Gumble 90%: 505.36 - UncertBand: 104.29
Uncertainty band reduction: 32.22%

'''
