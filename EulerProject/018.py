def CriaPath(n,size):
    if n>=2**size:
        print "Error in CriaPath. Number greater than size."
        return -1
    b=bin(n)[2:]
    s=len(b)
    zeros='0000000000000'
    return zeros[0:size-s]+b



p=open('018.txt','r')
tmp=p.read()
p.close()
tmp=[t.split(' ') for t in tmp.split('\n')]
triang=[]
for line in tmp:
    triang.append([int(i) for i in line])
del tmp

s=len(triang)

# o triangulo tem 15 linhas, a cada passo
# existem 2 possibilidades, ou seja,
# 2**(15-1) = 16384
# cada caminho pode ser representado
# por um numero binario de 14 digitos

maxsum=0
for c in range(2**(s-1)):
    path=CriaPath(c,s-1)
    soma=75
    bit=0
    for i in range(1,s):
        bit += int(path[i-1])
        soma += triang[i][bit]
    if soma>maxsum:
        maxsum=soma
        maxpath=path
        print "Step %d of %d - found maximum of %d" % (c, 2**(s-1), maxsum)

#show path
bit=0
print "Path with max sum: 75 ",
for i in range(1,s):
    bit += int(maxpath[i-1])
    print triang[i][bit],
print "\nThe max sum is %d" % maxsum
