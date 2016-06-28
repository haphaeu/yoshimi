from random import randint
import ConvertBase2
from Cross import Cross, Mutate

#test
#x=127
#retval=ConvertBase2.ConvertBase10to2(x)
#print retval
#retval2=ConvertBase2.ConvertBase2to10(retval)
#print retval2

print "This script uses the functions from"
print "ConvertBase2, which converts numbers"
print "from base 10 to base 2 and backwards,"
print "to test a 'cross' algorithm."
print "The cross is done by randomly"
print "changing a random number of bits between"
print "two integers."


x1=1234
x2=680
print "------------------------------"
print "Originaro Numbero"
print x1, x2
[x1_cros, x2_cros] = Cross(x1,x2)
x1_mut = Mutate(x1)
x2_mut = Mutate(x2)
print "Corossed Numbero"
print x1_cros, x2_cros
print "Mutatedo Numbero"
print x1_mut, x2_mut