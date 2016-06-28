i=2
ct=0
while i<=10000000:
    #print "\n==== %d ====" % i
    n=i
    while True:
        next=0
        for c in str(n): next+=int(c)**2
        #print next,
        if next==1: break
        if next==89:
            ct+=1
            break
        n=next
    i+=1
print("\n%d numbers arrived at 89." % ct)
