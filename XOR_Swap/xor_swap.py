from time import clock
from random import randint
#test bitwise Tmp to swap variable values

def CreateArray(iArraySize):
    Numbers=[]
    for i in range(iArraySize):
        Numbers.append(randint(1,10))
    return Numbers

def SwapWithTmp(SwapedNumbersTmp):
    size=len(SwapedNumbersTmp)
    tmp=0
    for i in range(0,size-1,2):
        tmp                     = SwapedNumbersTmp[i]
        SwapedNumbersTmp[i]     = SwapedNumbersTmp[i+1]
        SwapedNumbersTmp[i+1]   = tmp
    del tmp
    return 0

def SwapWithXOR(SwapedNumbersXOR):
    size=len(SwapedNumbersXOR)
    for i in range(0,size-1,2):
        SwapedNumbersXOR[i]   = SwapedNumbersXOR[i] ^ SwapedNumbersXOR[i+1]
        SwapedNumbersXOR[i+1] = SwapedNumbersXOR[i] ^ SwapedNumbersXOR[i+1]
        SwapedNumbersXOR[i]   = SwapedNumbersXOR[i] ^ SwapedNumbersXOR[i+1]
    return 0


def SimpleTest():
    #begin main functions
    print
    a= 136
    b= 982
    print "Variables a and b: %i %i" % (a,b)
    a=a^b
    b=a^b
    a=a^b
    print "After 3 XORs - a and b: %i %i" % (a,b)
    del a, b
    return 0

def PerformanceTest(ArraySize):
    #test of performance...
    #create array and make 2 copies of it
    sec0=clock()
    MyNums = CreateArray(ArraySize)
    SwapedNumbersTmp=MyNums[:]
    SwapedNumbersXOR=MyNums[:]
    #print MyNums
    sec1=clock()
    SwapWithXOR(SwapedNumbersXOR)
    sec2=clock()
    SwapWithTmp(SwapedNumbersTmp)
    sec3=clock()
    sec_all=sec1-sec0
    sec_xor=sec2-sec1
    sec_tmp=sec3-sec2
    del sec0, sec1, sec2, sec3
    del MyNums[:], SwapedNumbersTmp[:], SwapedNumbersXOR[:]
    del MyNums, SwapedNumbersTmp, SwapedNumbersXOR
    return sec_all, sec_xor, sec_tmp

def BatchTests(numTimes, ArraySize):
    #calls PerformanceTest() numTimes times
    # using arrays of the size ArraySize
    AllocTime=0
    XORSwapTime=0
    TMPSwapTime=0
    for iter in range(numTimes):
        retval=PerformanceTest(ArraySize)
        AllocTime+=retval[0]
        XORSwapTime+=retval[1]
        TMPSwapTime+=retval[2]
    print "Size %i | NumTimes %i | Allocate %f | XOR %f | TMP %f" % (ArraySize, numTimes, AllocTime, XORSwapTime, TMPSwapTime)
    if XORSwapTime > TMPSwapTime:
        print "In this architecture, swap with temporary variable is %f times quicker than with XOR" % (XORSwapTime/TMPSwapTime)
    else:
        print "In this architecture, swap with XOR is %f times quicker than with temporary variable" % (TMPSwapTime/XORSwapTime)

 