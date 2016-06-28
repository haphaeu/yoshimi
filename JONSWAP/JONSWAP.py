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
from math import pi as Pi
from math import exp
from math import sqrt
from math import cos
from random import random as rand

### INPUTS ###
g=9.81 #m/s2 - gravity

Tz=8.0 #s 
Hs=4.5 #m

#define frequency domain
wo=0.01   #rd/s - starting range of angular frequency
wf=3.5   #rd/s - ending range of angular frequency
dw=0.001   #rd/s - angular frequency step
n=int(1+(wf-wo)/dw) #number of frequency components

#define time domain
to=0.0     #s - initial time for wave train
tf=2000.0 #s - final time
dt=0.1     #s - time step

#initial phases
#phi=[1.5,0.9,3.8,2.6,5.2,0.2,3.9,6.2,0.9,4.2,2.9,0.6,5.3,6.1,1.1]
phi=[rand()*2*Pi for i in range(n)]

### CALCULATIONS ###
print "Calculating wave spectrum"
#calculate domain of angular frequencies
w=[wo+i*dw for i in range(n)]

#calculate parameters of spectrum, as per Isherwood
if 2*Pi*Hs/g/Tz**2>=0.037:
    gamma=10.54-1.34/sqrt(2*Pi*Hs/g/Tz**2)-exp(-19+3.775/sqrt(2*Pi*Hs/g/Tz**2))
else:
    gamma=0.9+exp(18.86-3.67/sqrt(2*Pi*Hs/g/Tz**2))
Tp=Tz/(0.6063+0.1164*sqrt(gamma)-0.01224*gamma) #s
wp =2*Pi/Tp #rd/s
alpha=(2.964+0.4788*sqrt(gamma)-0.343*gamma+0.04225*gamma**1.5)*(2*Pi*Hs/g/Tz**2)**2

#calculate JONSWAP spectrum
S=[]
for wi in w:
    if wi<wp: sigma=0.07
    else: sigma=0.09
    S.append(alpha*g**2/wi**5*exp(-5.0/4.0*(wp/wi)**4.0)*gamma**exp(-0.5*(wi-wp)**2/(sigma*wp)**2))

#calculate wave amplitude for each wave component
#also also calculate spectral moments
A=[]
m0=m1=m2=m3=m4=0.0
for i in range(n):
    if i==0:
        Sdw=(w[1]-w[0])/2.0 * (S[1]+S[0])/2.0
    elif i==n-1:
        Sdw=(w[i]-w[i-1])/2.0 * (S[i]+S[i-1])/2.0
    else:
        Sdw=(w[i]-w[i-1])/2.0 * (S[i]+S[i-1])/2.0 + (w[i+1]-w[i])/2.0 * (S[i+1]+S[i])/2.0
    A.append(sqrt(2.0*Sdw))
    m0+=Sdw
    m1+=Sdw*w[i]
    m2+=Sdw*w[i]**2
    m3+=Sdw*w[i]**3
    m4+=Sdw*w[i]**4

#double check some wave parameters based on spectral moments
chkHs=4.0*sqrt(m0)
chkTz=2*Pi*sqrt(m0/m2)

#now go to time domain and build the wave train as a sum of all the components
print "Calculating wave components"
#time domain
m=int(1+(tf-to)/dt)
t=[to+i*dt for i in range(m)]

#calculates wave train
#and counts up-crossings
h=[]
upX=0
for ti in t:
    hi=0
    for i in range(n):
        hi+=A[i]*cos(w[i]*ti+phi[i])
    h.append(hi)
    try:
        if h[-1]>0 and h[-2]<0: upX+=1
    except:
        pass

#calculates mean and stdev of wave elevation
mean = sum(h)/m
stdev = sqrt(sum((x-mean)**2 for x in h) / (m-1))
chk2Hs = 4*stdev
chk2Tz = (tf-to)/upX

### PRINT OUT RESULTS TO FILE
if True:
    pFile = open('output.txt','w')
    pFile.write("JONSWAP Spectrum and Wave Train\n")
    pFile.write("===============================\n")
    pFile.write("\nInputs:\n")
    pFile.write("Hs=%.2fm\nTz=%.2fs\n" % (Hs, Tz))
    pFile.write("Freq=[%.2f, %.2f, step %.2f] rd/s\n" % (wo, wf, dw))
    pFile.write("Time=[%.2f, %.2f, step %.2f] s\n" % (to, tf, dt))
    pFile.write("\nSpectral Parameters:\n")
    pFile.write("gamma=%.2f\nTp=%.2f s\nwp=%.2f rd/s\nalpha=%.2f\n" % (gamma, Tp, wp, alpha))
    pFile.write("\nSpectral Moments:\n")
    pFile.write("m0=%.3f m^2\nm1=%.3f m^2.rd/s\nm2=%.3f m^2.(rd/s)^2\nm3=%.3f m^2.(rd/s)^3\nm4=%.3f m^2.(rd/s)^4\n" % (m0,m1,m2,m3,m4))
    pFile.write("\nWave Elevation Statictics:\n")
    pFile.write("Max: %.2fm\nMin: %.2fm\nMean: %.2fm\nStDev: %.2fm\n" % (max(h), min(h), mean, stdev ))
    pFile.write("\nDouble Check Spectrum:\n")
    pFile.write("Hs=4*sqrt(m0)=%.2f m (%+.0f%%)\n" % (chkHs, 100.*(chkHs-Hs)/Hs))
    pFile.write("Tz=2*Pi*sqrt(m0/m2)=%.2f s (%+.0f%%)\n" % (chkTz, 100.*(chkTz-Tz)/Tz))
    pFile.write("\nDouble Check Wave Train:\n")
    pFile.write("Hs=4*stdev(elevation)=%.2f m (%+.0f%%)\n" % (chk2Hs, 100.*(chk2Hs-Hs)/Hs))
    pFile.write("Tz=duration/upCrossings=%.2f s (%+.0f%%)\n" % (chk2Tz, 100.*(chk2Tz-Tz)/Tz))
    pFile.write("\nSpectrum and wave components:")
    pFile.write("\nomega\tS(w)\tAmpl\tphi\n")
    pFile.write("rd/s\tm2s/rd\t m  \trd\n")
    for i in range(n):
        pFile.write("%.2f\t%.3f\t%.3f\t%.2f\n" % (w[i], S[i], A[i], phi[i]))
    pFile.write("\nWaveTrain:")
    pFile.write("\ntime\televation\n [s]\t[m]\n")
    for i in range(len(t)):
        pFile.write("%.2f\t%.2f\n" % (t[i], h[i]))
    pFile.close()

print "Done"
