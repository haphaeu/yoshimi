import sys

def blue(total):
    delta=4+8*total*(total-1)
    sqdelta=int(delta**0.5)
    if delta==sqdelta*sqdelta:
        b=(2+sqdelta)/4
        if b==int(b):
            return int(b)
        else:
            return False
    return False


t=4
i=0
print("Total\tBlue")
while i<=10000:
    b=blue(t+i)
    if b:
        print("%d\t%d" % (t+i, b))
        t0=t+i
    i+=1
print("=-=")

'''output
Total	Blue
4	3
21	15
120	85
697	493
4060	2871
=-=

procurando os termos Total na OEIS:
http://oeis.org/A046090

o primeiro termo maior que 1E12:
1070379110497

blue(1070379110497)=756872327473'''