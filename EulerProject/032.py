def isPandigital(strN):
    Ln = [c for c in strN]
    Ln.sort() 
    if Ln == ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    return False

listPans=[]
listMultiplier=[]
#dont know if these limits are ok
i=3
while i<2000:
    j=1
    while j<i:
        prod=i*j
        if isPandigital(str(i)+str(j)+str(prod)):
            listPans.append(prod)
            listMultiplier.append(i)
            print i, j, prod
        j+=1
    i+=1

numPans=len(listPans)
print "found %d pandigs" % numPans

#remove repeated pandigs
for p in listPans:
    if not listPans.index(p)==numPans-1-listPans[-1::-1].index(p):
        print "removing repeated entry %d" % p
        listPans.remove(p)
        numPans-=1
print "reduced to %d pandigs" % numPans
print listPans
print sum(listPans)
    
#output:    
#138 42 5796
#157 28 4396
#159 48 7632
#186 39 7254
#198 27 5346
#297 18 5346
#483 12 5796
#1738 4 6952
#1963 4 7852
#found 9 pandigs
#removing repeated entry 5796
#removing repeated entry 5346
#reduced to 7 pandigs
#[4396, 7632, 7254, 5346, 5796, 6952, 7852]
#45228
