def isPandigital(strN):
    Ln = [c for c in strN]
    Ln.sort() 
    if Ln == ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    return False

listPans=[]
listMultiplier=[]
#dont know if these limits are ok
i=9
while i<9999:
    n=2
    while n<999:
        j=1
        strProd=''
        while j<n:
            prod=j*i
            strProd += str(prod)
            j+=1
        if len(strProd)>9:
            break
        #print i,  n,  strProd
        if isPandigital(strProd):
            listPans.append(prod)
            listMultiplier.append(i)
            print "Pandigital", i, j, strProd
        n+=1
    i+=1

#output:
#Pandigital 9 6 918273645
#Pandigital 192 4 192384576
#Pandigital 219 4 219438657
#Pandigital 273 4 273546819
#Pandigital 327 4 327654981
#Pandigital 6729 3 672913458
#Pandigital 6792 3 679213584
#Pandigital 6927 3 692713854
#Pandigital 7269 3 726914538
#Pandigital 7293 3 729314586
#Pandigital 7329 3 732914658
#Pandigital 7692 3 769215384
#Pandigital 7923 3 792315846
#Pandigital 7932 3 793215864
#Pandigital 9267 3 926718534
#Pandigital 9273 3 927318546
#Pandigital 9327 3 932718654
