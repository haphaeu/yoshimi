#divs=[5,6,7,8,9,10]
divs=[11,12,13,14,15,16,17,18,19,20]

#this is my brute force code, takes a few minutes to run
#
##n=100
##while True:
##    flag=True
##    for i in divs:
##        if not n%i==0:
##            flag=False
##            break
##    if flag: break
##    n += 2
##print n


# this is a very clever algorithm I found, VERY QUICK
def numEvenDivBy(list):
	def isDiv(a,list):
		'''Checks if current number is divisable by numbers in list'''
		for i in list:
			if a%i != 0:
				return False
		return True


	def tester(list, iter):
		'''a basic and very ugly brute force algorithim'''
		a=iter
		while True:
			if isDiv(a,list):
				return a
				#print(a) #to see the magic, uncomment this print statement
			a+=iter  #part of magic


	c=1
	i=1
	for a in list:	#heart and soul of this method is this for loop
		i=tester(list[0:c],i)
		c+=1
	print(i)

numEvenDivBy(divs)
