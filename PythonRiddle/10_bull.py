#http://www.pythonchallenge.com/pc/return/sequence.txt
# a = [1, 11, 21, 1211, 111221,
a = [1, 11, 21, 1211, 111221]

def CalcNext(term):
    sterm=str(term)
    n=len(sterm)
    nextterm=''
    s=1
    c=sterm[0]
    for i in range(1,n):
        if sterm[i]==c:
            s+=1
        else:
            nextterm+=str(s)+c
            c=sterm[i]
            s=1
    nextterm+=str(s)+c
    return int(nextterm)

i=0
a=1
while i<=30:
   print "i=",i,", len=", len(str(a)) #, ", a=",a
   a=CalcNext(a)
   i+=1
# len a[30]=5808
