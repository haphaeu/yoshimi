from sys import stdout
from math import sqrt
from time import time
Sqrt3 = 3.**.5      # constant
verboseEvery=100000 # progess report

DistSqrdStart      = 297066731052
DistSqrdEnd        = 297066781052
DistStepSqrdStart  = 3 #Distance 2b incremented with the root of this step

eps=1.e-3                         # define an error

DistanceSqrd = DistSqrdStart
DistStepSqrd = DistStepSqrdStart
while DistanceSqrd <= DistSqrdEnd:
    firstLayer   = int(DistanceSqrd**0.5 /Sqrt3)
    lastLayer    = int(2./3 * DistanceSqrd**0.5 )
    #print "for a distance of %d layer betwenn %d ans %d" % (Distance,  
    #                                                        firstLayer,  
    #                                                        lastLayer)
    ct = 0                            # counter of hexs @ Distance
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
            t=time(); tt=(t-st)/p; tr=tt-t+st #time, estimated total time, time remaining
            if tr > 60:
            	stdout.write("Found %d so far - %.3f%% (%dmin remaining)\r" % (ct,  100*p, tr/60))
            else:
            	stdout.write("Found %d so far - %.3f%% (%ds remaining)\r" % (ct,  100*p, tr))
            stdout.flush()
        layer+=1
    print "A total of %d hexagons found for a distance^2 of %d" % (ct,  DistanceSqrd)
    DistanceSqrd += DistStepSqrdStart*DistStepSqrd;
    DistStepSqrd+=2;
