units=['','one','two','three','four','five','six','seven','eight','nine']
tenths=['','ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
ten=['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
hundred='hundred'
e='and'

verb=True

soma=0
for i in range(1,1000):
    h=i/100
    d=(i-100*h)/10
    u=i-100*h-10*d
    if i<10:
        if verb: print i, units[u]
        soma += len(units[u])
    elif i<20:
        if verb: print i, ten[u]
        soma += len(ten[u])
    elif i<100:
        if verb: print i, tenths[d], units[u]
        soma += len(tenths[d]) + len(units[u])
    else:
        if d==0 and u==0:
            if verb: print i, units[h], hundred
            soma += len(units[h])+len(hundred)
        elif d==0:
            if verb: print i, units[h], hundred, e, units[u]
            soma += len(units[h])+len(hundred)+len(e)+len(units[u])
        elif d==1:
            if verb: print i, units[h], hundred, e, ten[u]
            soma += len(units[h])+len(hundred)+len(e)+len(ten[u])
        else:
            if verb: print i, units[h], hundred, e, tenths[d], units[u]
            soma += len(units[h])+len(hundred)+len(e)+len(tenths[d])+len(units[u])


soma += len('onethousand')
print soma
