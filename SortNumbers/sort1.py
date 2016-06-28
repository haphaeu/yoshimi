from random import randint

def CreateArray(iArraySize):
    Numbers=[]
    for i in range(iArraySize):
        Numbers.append(randint(1,10))
    return Numbers

def SortArray(Numbers):
    SortedNumbers=Numbers
    size=len(Numbers)
    Trocou = 1
    ct=0
    while Trocou==1:
        Trocou=0
        ct+=1
        for i in range(size-1):
            if SortedNumbers[i]>SortedNumbers[i+1]:
                tmp = SortedNumbers[i]
                SortedNumbers[i]=SortedNumbers[i+1]
                SortedNumbers[i+1]=tmp
                Trocou=1
    print ct
    return SortedNumbers

print "Starting..."
MyArray = CreateArray(1000)
MySortedArray = SortArray(MyArray)

#print MyArray
#print MySortedArray
print "Done."