'''
Module with some basic fraction operations
by Rafael Rossi, 05/04/2012

alternatively, python has a module 'fractions'

'''

class fraction:
    #defines a fraction of naturals in the form:
    # fraction = num/den
    def __init__(self, num, den):
        if den==0:
            print "WARNING - denominator zero"
        self.den=den
        self.num=num

def invFrac(f):
    #inverses a fraction
    return fraction(f.den, f.num)

def sumFrac(f1,f2):
    #sum 2 fractions
    #does not simplify the fraction
    if f1.num==0: return f2
    if f2.num==0: return f1
    return fraction(f1.den*f2.num+f2.den*f1.num, f1.den*f2.den)

def mdc(n1,n2):
    #encontra o maximo denominador comum entre 2 naturais
    #usado para simpliciar fracoes
    #this is equivalent to the function gdc from the
    #python module fractions
    #http://en.wikipedia.org/wiki/Greatest_common_divisor#Using_Euclid.27s_algorithm
    if n1>n2: a=n1; b=n2
    else: a=n2; b=n1
    r=a%b
    while r:
        a=b
        b=r
        r=a%b
    return b

def simplifyFrac(f1):
    #simplifies a fraction
    m=mdc(f1.den, f1.num)
    return fraction(f1.num/m, f1.den/m)

