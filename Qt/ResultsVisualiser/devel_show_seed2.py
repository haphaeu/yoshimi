# -*- coding: utf-8 -*-
"""

Show seed number when mouse hover over data point.

Seed number is shown in status bar.

Adapted for multi line plots.

Created on Mon Jul 16 12:10:15 2018

@author: rarossi
"""
import scipy.stats as ss
import matplotlib.pyplot as plt


def on_move(event):
    ax.format_coord = format_coord
    for line, s in zip(lines, [s1, s2]):
        if line.contains(event)[0]:
            ind = line.contains(event)[1]["ind"][0]
            ax.format_coord = lambda x, y: 'x = %.3f   y = %.3f   Seed %d ' % (x, y, s[ind])


def format_coord(x, y):
    return 'x = %.3f   y = %.3f' % (x, y)


if __name__ == '__main__':
    x1 = ss.gumbel_r.rvs(size=50)
    x2 = ss.gumbel_r.rvs(size=50)
    y = list(range(len(x1)))
    s1 = sorted(range(len(x1)), key=x1.__getitem__)
    s2 = sorted(range(len(x2)), key=x2.__getitem__)
    x1.sort()
    x2.sort()

    fig, ax = plt.subplots()
    lines = [ax.scatter(x1, y, color='red', picker=True),
             ax.scatter(x2, y, color='blue', picker=True)]

    ax.format_coord = format_coord

    fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.show()
