from sys import stdout
from math import sqrt
from time import time
Sqrt3 = 3.**.5      # constant
verboseEvery=30000 # progess report

DistStart =   111111111
DistEnd   =   111111111
DistStep  =   1

Distance = DistStart
while Distance <= DistEnd:
    DistanceSqrd = Distance * Distance
    firstLayer   = int(Distance/Sqrt3)
    lastLayer    = int(2./3 * Distance)
    #print "for a distance of %d layer betwenn %d ans %d" % (Distance,  
    #                                                        firstLayer,  
    #                                                        lastLayer)
    ct = 0                            # counter of hexs @ Distance
    eps=1.e-3                         # define an error
    st=time()                         # store start time for the loop
    layer=firstLayer
    while layer <= lastLayer:
        delta   =12*DistanceSqrd-27*layer**2      # Bhaskara
        i_float =(3.*layer-sqrt(delta))/6.        # only smaller root
        i=long(round(i_float))                    # get closer integer
        if abs(i-i_float) < eps:           # check if i is close to an integer
            if DistanceSqrd==3*(layer**2-layer*i+i*i): #make sure i is integer
                if i==0:
                    ct+=6
                    #print "layer=",  layer,  ", ct=", ct
                elif not layer&1 and i==layer>>1: #even layer and i==layer/2
                    ct+=6
                    #print "layer=", layer,", ct=", ct
                else:
                    ct+=12
                    #print "layer=",  layer,  ", ct=", ct
                #print "Found a point for layer %d at i %d" % (layer,  i)
        if not layer%verboseEvery:
            p=1.*(layer-firstLayer)/(lastLayer-firstLayer)
            t=time(); tt=(t-st)/p; tr=tt-t+st
            stdout.write("Found %d so far - %.3f%% (%dmin remaining)\r" % (ct,  100*p, tr/60))
            stdout.flush()
        layer+=1
    print "A total of %d hexagons found for a distance of %d" % (ct,  Distance)
    
    Distance += DistStep
