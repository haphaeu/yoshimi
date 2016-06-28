import numpy as np


g   =9.80665

"""
Data from Metocean Design Basis for Aasgard Field (2013)
Temperature taken from an average month - October
Salinity taken from an average month - May
"""
def temperature(depth):
    """ depth [m] -> temperature [C] """
    z = [0, -10, -20, -30, -40, -50, -60, -70, -80, -90, -100,
         -125, -150, -175, -200, -250, -300]
    t = [9.72, 9.72, 9.71, 9.65, 9.46, 9.27, 9.07, 8.87, 8.71, 
         8.57, 8.43, 8.16, 7.95, 7.75, 7.56, 7.25, 6.83]
    z.reverse() #need to reverse for np.interp
    t.reverse()
    return np.interp(depth, z, t)

def salinity(depth):
    """ depth [m] -> salinity [C] """
    z = [0, -10, -20, -30, -40, -50, -60, -70, -80, -90, -100,
         -125, -150, -175, -200, -250, -300]
    S = [34.74, 34.80, 34.87, 34.94, 34.99, 35.03, 35.06, 35.10, 
         35.12, 35.13, 35.14, 35.16, 35.18, 35.19, 35.19, 35.17, 35.15]
    z.reverse()
    S.reverse()
    return np.interp(depth, z, S)

"""
Equation for water density with salinity level, temperature and pressure
Taken from:
http://www-pord.ucsd.edu/~ltalley/sio210/readings/gill_appendix3_ppsw.pdf
"""
def density(S=0, t=0, p=0):
    """ Salinity [psu], Temperature [C], Pressure [bar] -> Density [kg/m3] """
    return ((999.842594+0.06793952*t-0.00909529*t**2+0.0001001685*t**3
             -0.000001120083*t**4+0.000000006536332*t**5)+S*(0.824493
             -0.0040899*t+0.000076438*t**2-0.00000082467*t**3
             +0.0000000053875*t**4)+(S**1.5)*(-0.00572466+0.00010227*t
             -0.0000016546*t**2)+0.00048314*S**2)/(1-p/(((19652.21
             +148.4206*t-2.327105*t**2+0.01360477*t**3-0.00005155288*t**4)
             +S*(54.6746-0.603459*t+0.0109987*t**2-0.00006167*t**3)
             +(S**1.5)*(0.07944+0.016483*t-0.00053009*t**2))+p*(3.239908
             +0.00143713*t+0.000116092*t**2-0.000000577905*t**3)+p*S*(0.0022838
             -0.000010981*t-0.0000016078*t**2)+0.000191075*p*(S**1.5)
             +(p**2)*(0.0000850935-0.00000612293*t+0.000000052787*t**2)
             +(p**2)*S*(-0.00000099348+0.000000020816*t+0.00000000091697*t**2)))

def densityWD(WD=-300, S=salinity, t=temperature, delta=1.0):
    """ Water Depth [m], Salinity [psu], Temperature [C] -> Density [kg/m3] """
    z=p=0
    rho = density(S(0),t(0),0)
    dgbar=delta*g/1.0e5
    depth=[0]
    salin=[S(0)]
    tempe=[t(0)]
    press=[0]
    densi=[rho]
    while z>WD:
        p   += rho * dgbar
        rho  = density(S(z),t(z),p)
        depth.append(z-delta)
        salin.append(S(z))
        tempe.append(t(z))
        press.append(p)
        densi.append(rho)
        z   -= delta
    return depth, salin, tempe, press, densi


""" ********************************** """
"""              MAIN                  """
""" ********************************** """

z, s, t, p, d = densityWD()

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(bottom=0.35)

par1 = host.twiny()
par2 = host.twiny()
par3 = host.twiny()

offset = 60
new_fixed_axis1 = par1.get_grid_helper().new_fixed_axis
par1.axis["bottom"] = new_fixed_axis1(loc="bottom", axes=par1, offset=(0, -offset))
new_fixed_axis2 = par2.get_grid_helper().new_fixed_axis
par2.axis["bottom"] = new_fixed_axis2(loc="bottom", axes=par2, offset=(0, -2*offset))
new_fixed_axis3 = par3.get_grid_helper().new_fixed_axis
par3.axis["bottom"] = new_fixed_axis2(loc="bottom", axes=par3, offset=(0, -3*offset))
par1.axis["top"].toggle(all=False)
par2.axis["top"].toggle(all=False)
par3.axis["top"].toggle(all=False)

host.set_xlim(min(d)-0.5, max(d)+0.5) #density
host.set_xticks(np.linspace(min(d)-0.5, max(d)+0.5,10))
host.set_xticklabels(["%.2f" % _ for _ in np.linspace(min(d)-0.5, max(d)+0.5,10)])
host.set_ylim(min(z), max(z))         #depth
#host.set_yticks(range(int(min(z)), int(max(z))+1, 50), minor=True)

host.set_xlabel("Density [kg/m3]")
host.set_ylabel("Depth [m]")
par1.set_xlabel("Temperature [degC]")
par2.set_xlabel("Salinity [psu]")
par3.set_xlabel("Pressure [bar]")

p1, = host.plot(d, z, label="Density")
p2, = par1.plot(t, z, label="Temperature")
p3, = par2.plot(s, z, label="Salinity")
p4, = par3.plot(p, z, label="Pressure")

par1.set_xlim(min(t)-0.1, max(t)+0.1) #temperature
par1.set_xticks(np.linspace(min(t)-0.1, max(t)+0.1,10))
par1.set_xticklabels(["%.2f" % _ for _ in np.linspace(min(t)-0.1, max(t)+0.1,10)])
par2.set_xlim(min(s)-0.1, max(s)+0.1) #salinity
par2.set_xticks(np.linspace(min(s)-0.1, max(s)+0.1,10))
par2.set_xticklabels(["%.2f" % _ for _ in np.linspace(min(s)-0.1, max(s)+0.1,10)])
par3.set_xlim(min(p), max(p)+0.1) #pressure
par3.set_xticks(np.linspace(min(p), max(p)+0.1,10))
par3.set_xticklabels(["%.2f" % _ for _ in np.linspace(min(p), max(p)+0.1,10)])

host.legend(loc=6)

host.axis["bottom"].label.set_color(p1.get_color())
par1.axis["bottom"].label.set_color(p2.get_color())
par2.axis["bottom"].label.set_color(p3.get_color())
par3.axis["bottom"].label.set_color(p4.get_color())

plt.title("""Water Depth against Water Density, Temperature, Salinity and Pressure
          from Aasgard Metocean (2013) - Temperatures from October, Salinity from May""")

plt.grid()

plt.draw()
plt.show()
