'''
Module with some basic fraction operations
by Rafael Rossi, 05/04/2012

alternatively, python has a module 'fractions'

'''

class fraction:
    #defines a fraction of naturals in the form:
    # fraction = num/den
    def __init__(self, num, den):
        self.den=den
        self.num=num

def invFrac(f):
    #inverses a fraction
    return fraction(f.den, f.num)

def sumFrac(f1,f2):
    #sum 2 fractions
    #does not simplify the fraction
    return fraction(f1.den*f2.num+f2.den*f1.num, f1.den*f2.den)

def mdc(n1,n2):
    #encontra o maximo denominador comum entre 2 naturais
    #usado para simpliciar fracoes
    #this is equivalent to the function gdc from the
    #python module fractions
    i = min(n1,n2)
    while i>0:
    #for i in xrange(min(n1,n2),0,-1):
        if n1%i==0 and n2%i==0:
            break
        i-=1
    return i

def simplifyFrac(f1):
    #simplifies a fraction
    m=mdc(f1.den, f1.num)
    return fraction(f1.num/m, f1.den/m)

