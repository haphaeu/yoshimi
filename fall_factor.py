# -*- coding: utf-8 -*-
"""
Fall Factor

Impact loads on rock climbing gear.

  Force = sqrt(2 * m * g * EA * h/Lo)

where:
    m: mass of the falling object
    g: gravity
    EA: stiffness of the rope/sling
    h: height of the fall
    Lo: length of rope/sling absorbing the impact load

Note that a fall factor can be defined as FF = h/Lo.

by Rafael Rossi, 21.08.2017

"""

import pandas
from matplotlib import pyplot as plt


def dmm_tests():
    """Calibrate slings stiffness based on a batch of tests performed by DMM [1]
    [1] http://dmmclimbing.com/knowledge/how-to-break-nylon-dyneema-slings/
    """
    tests = [(1, 'Nylon 16mm', '120cm', 12.8),
             (2, 'Nylon 16mm', '120cm', 17.6),
             (1, 'Dyneema 8mm', '60cm', 17.8),
             (1, 'Dyneema 11mm', '60cm', 16.7),
             (1, 'Nylon 16mm', '60cm', 11.6),
             (1, 'Nylon 26mm', '60cm', 11.8),
             (1, 'Static rope 11mm', '60cm', 7.3),
             (1, 'Dynamic rope 10mm', '60cm', 5.7),
             (2, 'Nylon 16mm', '60cm', 15.4),
             (2, 'Nylon 26mm', '60cm', 16.3),
             (2, 'Static rope 11mm', '60cm', 10.3),
             (2, 'Dynamic rope 10mm', '60cm', 7.4),
             (1, 'Dyneema 8mm', '30cm', 14.8),
             (1, 'Dyneema 11mm', '30cm', 16.4),
             (1, 'Nylon 16mm', '30cm', 10.6),
             (1, 'Nylon 26mm', '30cm', 11.0),
             (2, 'Dyneema 8mm', '30cm', 22.6),
             (2, 'Dyneema 11mm', '30cm', 18.7),
             (2, 'Nylon 16mm', '30cm', 14.0)]
    df = pandas.DataFrame(data=tests, columns=['FF', 'Type', 'Length', 'Load'])
    print('Impact Loads from DMM tests [kN]')
    print(df.pivot_table(values='Load', columns='FF', index=('Type', 'Length'),
                         fill_value='-'))

    # Calculate and add EA values
    test_weight = 80 * 9.806
    df['EA'] = df.Load**2 / (2*test_weight*df.FF) * 1000

    print('Calculated stiffness [kN]')
    print(df.pivot_table(values='EA', columns='FF', index=('Type', 'Length'),
                         fill_value='-'))


def solve_fall(sling_length=1.2,
               fall_factor=1,
               sling_stiffness=105000,
               mass=80):
    """Solve the motion of an impact load. No damping effects.
    sling_length in meters
    fall_factor
    sling_stiffness in N
    mass in kg
    force in kN
    """

    # Echo input
    print('Sling length %.2f m' % sling_length)
    print('Fall factor %.1f' % fall_factor)
    print('Sling stiffness %.1f N' % sling_stiffness)
    print('Mass %.1f kg\n' % mass)

    # Simplified- Force only
    force = (2 * mass * 9.806 * sling_stiffness * fall_factor)**0.5 / 1000

    # Motion solver
    vo = (2*9.806*sling_length*fall_factor)**0.5
    c = sling_stiffness/sling_length/mass
    dt = 1e-5
    t, x, v, a, F = [0], [0], [vo], [0], [0]
    while v[-1] > 0:
        xp = x[-1]
        t.append(t[-1]+dt)
        a.append(- c * xp)
        v.append(v[-1] + a[-1] * dt)
        x.append(x[-1] + v[-1] * dt)
        F.append(sling_stiffness/sling_length * x[-1] / 1000)
    return force, t, x, v, a, F


def plot_fall(*args, **kwargs):
    """Plots the time traces of the fall with impact load.
    Same input arguments as solve_fall.
    """
    force, t, x, v, a, F = solve_fall(*args, **kwargs)
    print('Impact force %.1f kN' % force)
    plt.subplot(221)
    plt.plot(t, F)
    plt.title('Fall Impact Force [kN]')
    plt.xticks(())
    plt.subplot(222)
    plt.plot(t, x)
    plt.title('Fall Distance [m]')
    plt.xticks(())
    plt.subplot(223)
    plt.plot(t, v)
    plt.title('Fall Speed [m/s]')
    plt.subplot(224)
    plt.plot(t, a)
    plt.title('Fall Acceleration [m/s2]')
    plt.xlabel('Time [s]')
    plt.show()
    print('Solved only up to maximum force.')


def main():
    plot_fall()


if __name__ == '__main__':
    import time
    t0 = time.time()
    main()
    print('\nruntime %f s' % (time.time()-t0))
