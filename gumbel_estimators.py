# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 08:33:39 2014

@author: rarossi
"""

from numpy import mean, std, pi, exp, log, square, reshape

data	= [4893.18457,	5112.021484,	6231.851563,	5056.416992,	5220.287598,	5525.234375]

""" 
    Paramter Estimators for Gumbel Fit 
    MOM - Method Of Moments
    MLM - Maximum Likelihood Method
    MLS - Method of Least Squares
    OSA - Order Statistics Approach
    PME - Principle of Maximum Entropy
    PWM - Probability Weighted Moments
    
    [http://www.engineerspress.com/pdf/WSJ/2013-02/a2_WSJ-131202_.pdf] 
    [spreadsheet with methos implemented for checking]
"""

def MOM(data):
    """ alpha, beta <- MOM(data) Method Of Moments """
    beta  = 6**0.5 / pi * std(data)
    alpha = mean(data) - 0.5772 *  beta
    return alpha, beta

def MLM(data):
    """ alpha, beta <- MLM(data) Maximum Likelihood Method """
    sd = std(data)
    N  = len(data)
    mn = mean(data)
    beta0 = sd #initial estimate
    while True:
        beta = ( mn - sum(map(lambda x: x*exp(-x/beta0), data)) / 
                         sum(map(lambda x:   exp(-x/beta0), data)) )
        if abs(beta-beta0)<1e-6: break
        else: beta0=beta        
    alpha = -beta*log(sum(map(lambda x: exp(-x/beta), data))/N)
    return alpha, beta    
def MLM2(data):
    """ alpha, beta <- MLM(data) Maximum Likelihood Method (using scipy) """
    """note that it returns the same as the MLM above (luckly :)"""
    from scipy import stats
    return stats.gumbel_r.fit(data)

def MLS(data):
    """ alpha, beta <- MLS(data) Method of Least Squares """
    mn = mean(data)
    N = len(data)
    Pi = [(i-0.44)/(N+0.12) for i in range(1,N+1)]
    beta = (sum(data)**2 - N*sum(square(data)))/((N*sum([data[i]*log(-log(Pi[i])) for i in range(N)]))
                                                 -sum(data)*sum([log(-log(Pi[i])) for i in range(N)]))
    alpha = mn+sum([log(-log(Pi[i])) for i in range(N)])*beta/N
    return alpha, beta

def OSA(data):
    """ alpha, beta <- OSA(data) Order Statistics Approach """
    """
    forget about this fucking shity method ...
    N=len(data)
    k=m=int(data**0.5) #this is the assumed new shape, needs refinement
    mp=N-k*m
    t  = 1.0 * k*m/N
    tp = 1.0 * mp/N
    Y = reshape(data[:k*m], (k,m))
    for i in range(k): Y[i].sort()
    S=[]
    for k in range(m):
        s=0
        for i in range(k):
            s+=Y[i][j]
        S.append(s)"""
    
    
    
                                                 