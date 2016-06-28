def main():
    primes = [2,3,5,7,11,13,17,19,23,29]
    targetn = 15499
    targetd = 94744
    val = 1
    bar = 1
    for p in primes:
        nval = val * p
        nbar = bar * (p-1)
        if (targetn * (nval-1) > nbar*targetd):
            d = targetn*val - targetd*bar
            n = (targetn+d-1)/d
            print (n * val)
            return
        val = nval
        bar = nbar
    print "Need more primes"

from time import time
st=time()
main()
print (time()-st)
