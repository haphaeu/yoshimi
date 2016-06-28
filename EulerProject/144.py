from math import atan, tan, sqrt
def f(x):
#elipse 4x^2+y^2=100
  return sqrt(100-4*x**2)
def elipse_slope(p):
#slope of the tangent line of the elipse
#p is a tuple (x,y)
  return -4.*p[0]/p[1]
def beam_slope(p1,p2):
  return (p2[1]-p1[1])/(p2[0]-p1[0])

# MAIN
VERBOSE=False
#define tolerance for equalities
eps=1.e-6
#initial points
p1=(0.0, 10.1)
p2=(1.4, -9.6)
if VERBOSE: print "enter, %.16f, %.16f" % (p1[0], p1[1])
#start loop
ct=1
while True:
  #calc next point laser beam will hit ellipse
  mb=beam_slope(p1,p2)        #slope of the incident beam
  mt=elipse_slope(p2)         #slope of the elipse tangent @ p2
  mn=-1./mt                    #slope of the normal to the elipse @ p2
  mr=tan(2*atan(mn)-atan(mb)) #slope of the reflected beam
  #calc where reflected beam crosses the ellipse
  a=mr
  b=p2[1]-mr*p2[0]
  #Bhaskara
  delta=400*a**2-16*b**2+1600
  x1= ( -2*a*b + sqrt(delta) ) / (8+2*a**2)
  x2= ( -2*a*b - sqrt(delta) ) / (8+2*a**2)
  #as one of the roots is p2 itself, take the other
  if x1-p2[0] < eps: xr=x2
  else: xr=x1
  #yr=f(xr)  #can't use ellipse equation as signal will be lost
  yr= a*xr+b #need to use straight line equation instead
  #check if beam exits white cell
  if yr>0 and abs(xr)<=0.01:
    if VERBOSE: print "exits, %.16f, %.16f" % (xr,yr)
    break
  #print status
  if VERBOSE: print "%d, %.16f, %.16f, %.16f, %.16f, %.16f, %.16f" % (ct, mb, mt, mn, mr, p2[0], p2[1])
  #move p2 to p1 and update p2
  p1=p2
  p2=(xr,yr)
  ct+=1 
print ct
#output:
#354


"""
Desenvolvimento da solucao de Bhaskara:
reta do raio refletido em p2
y=ax+b
a=mr
b=y-ax=p2[1]-mr*p2[0]


y=ax+b e 4x^2+y^2=100
=> 4x^2+[ax+b]^2=100

4x^2 + a^2 x^2 + 2abx + b^2 = 100
(4+a^2)x^2 + 2abx + (b^2-100) = 0
delta=(2.a.b)^2 - 4.(4+a^2).(b^2-100)
delta=4a^2 b^2-4(4b^2-400+a^2 b^2 -100a^2)
delta=4a^2b^2 - 16b^2 + 1600 - 4a^2b^2 + 400a^2
delta=400a^2-16b^2+1600
x= [ -2ab +/- sqrt(delta) ] / 2(4+a^2)
"""