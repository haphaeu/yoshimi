from math import log
# log(x [, base])

def ConvertBase10to2(x_10):
    #The returned number in base 2 is a list.
    #Note that the index of the list element
    #is the power of 2 of the number, i.e.,
    #the order of the bits is the **reverse**
    #order that one would write.
    if x_10==0:
        return 0
    else:
        x_2=[]
        bits=int(log(x_10,2))+1
        for i in range(bits): x_2.append(0)
        x_2[bits-1]=1
        rest=x_10-2**(bits-1)
        while rest>0:
            pot = int( log( rest, 2))
            x_2[pot]=1
            rest-=2**pot
        return x_2

def ConvertBase2to10(x_2):
    x_10=0
    if x_2>0:
        for pot in range(len(x_2)): x_10+=x_2[pot]*2**pot
    return x_10





