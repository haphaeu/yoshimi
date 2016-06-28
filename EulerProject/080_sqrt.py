#argument must be integer
def pair(num):
    pairs=[]
    while num>99:
        pairs.append(num%100)
        num/=100
    pairs.append(num)
    pairs.reverse()
    return pairs
# ##################################
# sum the first 100 digits
# of the square root of num
def sum100d(num):
    sqr=0
    pairs=pair(num)
    sz=len(pairs)
    n=pairs[0]
    sqr=int(n**0.5)
    resto=n
    tmp=sqr*sqr
    i=1; decpt=0
    sumOfDecimalDigits=sqr
    flag=False
    while True:
        if i>=sz:
            add=0
            decpt+=1
        else:
            add=pairs[i]    
        resto=(resto-tmp)*100+add
        if resto==0: break
        n=9
        while True: #next digit of sqrt
            tmp=(2*sqr*10+n)*n
            if tmp<resto: break
            n-=1
        sqr=sqr*10+n
        sumOfDecimalDigits+=n
        i+=1
        if i==100: break
    #print decpt, sqr
    return sumOfDecimalDigits
# ### MAIN ###
soma=0
for i in range(2,100):
    if not int(i**0.5)==i**0.5:
        soma+=sum100d(i)
print soma
        
    
    
    


