from random import randint
print "Jogo mega-sena: ",
num=n=0
jogo=[]
for _ in range(6):
    num=randint(1,60)
    while num in jogo:    
        num=randint(1,60)
    jogo.append(num)
jogo.sort()
print jogo
    
