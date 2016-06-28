from ConvertBase2 import ConvertBase10to2, ConvertBase2to10
from random import randint

def Cross(x1, x2):
    x1_2=ConvertBase10to2(x1)
    x2_2=ConvertBase10to2(x2)
    minLen=min(len(x1_2),len(x2_2))
    NumBits2Change = randint(1,minLen)
    for i in range(NumBits2Change):
        Bit2Change=-1+randint(1,minLen)
        tmp=x1_2[Bit2Change]
        x1_2[Bit2Change]=x2_2[Bit2Change]
        x2_2[Bit2Change]=tmp
    x1_cros = ConvertBase2to10(x1_2)
    x2_cros = ConvertBase2to10(x2_2)
    return x1_cros, x2_cros

def Mutate(x):
    x_2=ConvertBase10to2(x)
    minLen=len(x_2)
    NumBits2Change = randint(1,minLen)
    for i in range(NumBits2Change):
        Bit2Change = -1+randint(1,minLen)
        if x_2[Bit2Change] == 1:
            x_2[Bit2Change]=0
        else:
            x_2[Bit2Change]=1
    x_mut = ConvertBase2to10(x_2)
    return x_mut