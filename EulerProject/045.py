nterms=60000
#set of triangle number
triang={n*(n+1)>>1 for n in xrange(1, nterms)}
#set of pentagonal numbers
pentag={n*(3*n-1)>>1 for n in xrange(1, nterms)}
#set of hexagonal numbers
hexag={n*(2*n-1) for n in xrange(1, nterms)}
#find common values in the 3 sets above
print triang.intersection(pentag.intersection(hexag))
#output
#set([1, 40755, 1533776805])
