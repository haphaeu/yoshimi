eps=1e-6
#fraction f = n1n2/d1d2
# ex. f=21/42 => n1=2, n2=1, d1=4, d2=2
for n1 in range(1,10):
	for n2 in range(1,10):
		for d1 in range(n1+1,10):
			for d2 in range(1,10):
				if not n1==n2:
					f1=(n1*10.0+n2)/(d1*10.0+d2)
					if n1==d2:
						f3=1.0*n2/d1
						if abs(f1-f3)<eps: print "%d%d/%d%d = %d/%d" % (n1,n2,d1,d2,n2,d1)
					if n2==d1:
						f2=1.0*n1/d2
						if abs(f1-f2)<eps: print "%d%d/%d%d = %d/%d" % (n1,n2,d1,d2,n1,d2)
					
#output is:
# 16/64 = 1/4
# 19/95 = 1/5
# 26/65 = 2/5
# 49/98 = 4/8

# doing by hand:	
# 1/4 * 1/5 * 2/5 * 4/8 = 1/100

#hence, answer is 100