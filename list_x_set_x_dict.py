from random import randint
from time import time

# ##### INPUTS ##### ########################################

#random list with 100k 6-digit integers integers 
L=[randint(100000,999999) for _ in range(100000)]

#create a set from L
S=set(L)

#create a dict from L
# (is there a better way to do this?)
D={}
for _ in L:
    D[_]=_

START=123456
END  =START+10000
# ##### RUN ##### ########################################
# now performs random searches and add elements in each 
# group to check for speed
print "List x Set x Dict"
print "Performing %d random searches" % (END-START)
print "Here we go..."
#SET
print "Set",
i=START
st=time()
while i<END:
    if i in S: pass
    else: S.add(i)
    i+=1
ts=time()-st
print "- took %.4fs" % ts
# DICT
print "Dict",
i=START
st=time()
while i<END:
    if i in D: pass
    else: D[i]=i
    i+=1
td=time()-st
print "- took %.4fs" % td
# LIST
print "List",
i=START
st=time()
while i<END:
    if i in L: pass
    else: L.append(i)
    i+=1
tl=time()-st
print "- took %.4fs" % tl

'''
OUTPUT

List x Set x Dict
Performing 10000 random searches
Here we go...
Set - took 0.0040s
Dict - took 0.0030s
List - took 19.7810s
'''
