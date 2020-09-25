from typing import Callable, Optional, List, Tuple
import matplotlib.pyplot as plt
import numpy as np


def newton(*args, **kwargs) -> Optional[float]:
    '''Wrapper for _newton method, returning only the root.'''
    
    root, has_converged, iters = _newton(*args, **kwargs)
    
    if has_converged:
        return root
    return None


def _newton(
        f: Callable[[float], float],  # function to find the root to
        fprime: Callable[[float], float],  # derivative of f
        x0: float = 0.0,  # initial guess for the root
        max_iters: int = 20,  # max numbers of iteractions
        tolerance: float = 1e-7,  # tolerance to find the root
        epsilon: float = 1e-14,  # threshold for y to avoid overflow
        verbose: bool = False,  # print each iteraction
        ) -> Tuple[float, bool, List[Tuple[float, float]]]:

    if verbose:
        print('{:4s} {:>16s} {:>16s} {:>16s}'.format('Iter', 'x0', 'y', 'yprime'))

    iters = []
    has_converged = False
    x1 = x0  # just in case yprime<epsilon in 1st iteraction
    
    for i in range(max_iters):

        y = f(x0)
        yprime = fprime(x0)

        iters.append((x0, y))

        if verbose:
            print('{:4d} {:16.6g} {:16.4g} {:16.4g}'.format(i, x0, y, yprime))

        if abs(yprime) < epsilon:
            break

        x1 = x0 - y / yprime

        if abs(x1 - x0) < tolerance:
            has_converged = True
            break

        x0 = x1

    if verbose and not has_converged:
        print(f'Solution has not converged after {i} iteractions.')
        
    return x1, has_converged, iters
    
    
def plot(
        f: Callable[[float], float],
        iters: List[Tuple[float, float]],
        npoints: int = 100,
        ) -> None:
    '''Plot the iteractions of the Newton method'''
    
    # Adjusts the iteractions to show the path of the algorithm
    iters_plot = []
    for xi, yi in iters:
        iters_plot.append((xi, 0))
        iters_plot.append((xi, yi))
    xis, yis = zip(*iters_plot)  # transpose the list of lists
        
    # Also plots the function itself
    min_xis = min(xis)
    max_xis = max(xis)
    range_xis = max_xis - min_xis
    pad = 0.25 * range_xis
    xs = np.linspace(min_xis - pad, max_xis + pad, npoints)
    ys = list(map(f, xs))

    plt.plot(xs, ys, lw=3)
    plt.plot(xis, yis, 'k', lw=1)
    plt.grid()
    plt.show()
