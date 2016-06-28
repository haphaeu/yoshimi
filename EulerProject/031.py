from time import time
st=time()

# Equation
# 1.c0 + 2.c1 + 5.c2 + 10.c3 + 20.c4 + 50.c5 + 100.c6 = 200
# constrants:
#	c0 <= 200
#	c1 <= 100
#	c2 <=  40
#	c3 <=  20
#	c4 <=  10
#	c5 <=	4
#	c6 <=   2

tot=1 # don't forget the 2L coin ;D
for c6 in range(3):
 C6=c6*100
 for c5 in range(5):
  C5=c5*50+C6
  if C5>200: break
  for c4 in range(11):
   C4=c4*20+C5
   if C4>200: break
   for c3 in range(21):
    C3=c3*10+C4
    if C3>200: break
    for c2 in range(41):
     C2=c2*5+C3
     if C2>200: break
     for c1 in range(101):
      C1=c1*2+C2
      if C1>200: break
      for c0 in range(201):
       C0=c0*1+C1
       if C0==200:
        tot+=1
        break
print "Found %d combinations (took %.2fms)" % (tot, 1000*(time()-st))
#output
#Found 73682 combinations (took 936.00ms)