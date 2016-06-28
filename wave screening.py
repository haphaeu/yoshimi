from OrcFxAPI import *
from numpy import std, diff, array
from sys import stdout

'''
This is script to extract wave elevation rises and falls
above a threshold level, for various wave seeds.

At the moment, supported spectra are:
 - Torsethaugen                - input Tp
 - JONSWAP Automatic           - input Tz
 - JONSWAP Partially Specified -  input Tp, Gamma

Directionality is also supported.

RFR - 28/08/2012

'''

# ### INPUT DATA: START
WaveType = 'Torsethaugen'
#WaveType = 'JONSWAP'
WaveSeeds = [12345, 23451, 34512, 45123, 51234, 54321, 43215, 32154, 21543, 15432]
WaveHs = 4.5
#this is:
#   Tp for Torsethaugen,
#   Tp for JONSWAP Partially Specified, and
#   Tz for JONSWAP Automatic
WaveT = 6
SimulationDuration = 21600
WaveRiseThreshold = 1.8*WaveHs
#data specific for JONSWAP spectrum:
JONSWAPParameters = 'Partially Specified'
#JONSWAPParameters = 'other'
WaveGamma = 1.89
#data specific for when directinality is on
NumberWaveDirections = 1
SpreadingExponent    = 12
# ### INPUT DATA: END

#echo of the input data
print "\nINPUT DATA:\n**********"
print "WaveType      %s" % WaveType
print "Hs        [m] %.2f" % WaveHs
if WaveType == 'JONSWAP' and JONSWAPParameters == 'Partially Specified':
    print "Parameters    %s" % JONSWAPParameters
    print "Tp        [s] %.2f" % WaveT
    print "Gamma     [-] %.3f" % WaveGamma
elif WaveType == 'JONSWAP':
    print "Tz        [s] %.2f" % WaveT
else: #Torsethaugen
    print "Tp        [s] %.2f" % WaveT
if NumberWaveDirections>1:
    print "num Dirs: [-] %d" % NumberWaveDirections
    print "Exponent  [-] %d" % SpreadingExponent
print "Seeds     [-]",; print WaveSeeds
print "Duration  [s] %.2f" % SimulationDuration
print "Threshold [m] %.2f" % WaveRiseThreshold

print "\nRESULTS:\n*******"
stdout.write("Loading OrcaFlex.\r")
m=Model()
obj=m.environment
obj.SetData('WaveType',0,WaveType)
obj.SetData('UserSpecifiedRandomWaveSeeds',0,'Yes')
obj.SetData('WaveHs',0,WaveHs)
if NumberWaveDirections>1:
    obj.SetData('WaveNumberofSpectralDirections',0,NumberWaveDirections)
    obj.SetData('WaveDirectionSpreadingExponent',0,SpreadingExponent)
if WaveType == 'JONSWAP' and JONSWAPParameters == 'Partially Specified':
    obj.SetData('WaveJONSWAPParameters',0,JONSWAPParameters)
    obj.SetData('WaveGamma',0,WaveGamma)
    obj.SetData('WaveTp',0,WaveT)
elif WaveType == 'JONSWAP':
    obj.SetData('WaveTz',0,WaveT)
else: #Torsethaugen
    obj.SetData('WaveTp',0,WaveT)
    
m.general.SetData('StageDuration',1,SimulationDuration)

for WaveSeed in WaveSeeds:
    print "Wave Seed %d" % WaveSeed
    obj.SetData('WaveSeed',0,WaveSeed)
    stdout.write("Running simulation.\r")
    m.Reset()
    m.RunSimulation()
    wt=obj.TimeHistory('Elevation',Period(1),oeEnvironment(0,0,0))
    tt=m.general.TimeHistory('Time',Period(1))
    stdev=std(wt)

    #peak search - all peaks and troughs
    stdout.write("Peak search.\r")
    wpeaks=[]
    tpeaks=[]
    for i in range(1,len(wt)-1):
        x1=wt[i-1]
        x2=wt[i]
        x3=wt[i+1]
        if x1<=x2>x3: #peak
            wpeaks.append(x2)
            tpeaks.append(tt[i])
        elif x1>=x2<x3: #trough
            wpeaks.append(x2)
            tpeaks.append(tt[i])
    stdout.write("Searching false peaks.\r")
    #now, remove consequent peaks with same signal
    i=1
    i_lim=len(wpeaks)-1
    idx_2bRemoved=[]
    while i<i_lim:
        if wpeaks[i-1] * wpeaks[i] > 0:
            #firstly, counts how many consecutive peask have same signal
            for j in range(i-1,i+1000):
                if j==i_lim-1 or wpeaks[j] * wpeaks[j+1]<0:
                    final_i=j
                    break
            #then, finds the maximum peaks, which will be kept
            max_j=i-1
            for j in range(i-1, final_i+1):
                if abs(wpeaks[max_j]) < abs(wpeaks[j]):
                    max_j=j
            #finally, save a list of the indexes of the peaks to be removed
            for j in range(i-1,final_i+1):
                if not j==max_j:
                    idx_2bRemoved.append(j)
            #jump the peaks removed
            i=final_i+1
        else:
            i+=1
    #remove peaks
    idx_2bRemoved.reverse()
    for i in idx_2bRemoved:
        wpeaks.remove(wpeaks[i])
        tpeaks.remove(tpeaks[i])
    #done. print results
    ##print "Time[s]\tPeak[m]"
    ##for i, w in enumerate(wpeaks):
    ##    print "%f\t%f" % (tpeaks[i], w)

    #get raises and falls above threshold
    rises  = diff(wpeaks)
    periods = diff(tpeaks)
    th_rises  = rises [(rises<-WaveRiseThreshold)+(rises>WaveRiseThreshold)]
    th_period = periods[(rises<-WaveRiseThreshold)+(rises>WaveRiseThreshold)]
    th_times  = array(tpeaks)
    th_times  = th_times[(rises<-WaveRiseThreshold)+(rises>WaveRiseThreshold)]
    print "Rises and falls above threshold"
    print "Rise\tPeriod\tTime"
    print "[m]\t[s]\t[s]"
    for i, r in enumerate(th_rises):
        print "%+.2f\t%.2f\t%.2f" % (r, 2*th_period[i], th_times[i])
    print "(negative rise means a fall)\n"

