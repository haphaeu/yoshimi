from math import atan
import newton_raphson as nr

def myf(x):
    return (x - 5)**2 - 5

def myfp(x):
    return 2 * (x - 5)


def atanprime(x):
    return 1 / (x**2 + 1)

f = atan
fp = atanprime

root, has_converged, iters = nr._newton(
        f,
        fp,
        x0=1.2,
        verbose=True,
        )

nr.plot(f, iters)
