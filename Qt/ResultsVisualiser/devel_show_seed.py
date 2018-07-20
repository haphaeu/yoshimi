# -*- coding: utf-8 -*-
"""

Show seed number when mouse hover over data point.

Seed number is shown in annotation box and in status bar.

Too cumbersome. See version 2.


Created on Mon Jul 16 12:10:15 2018

@author: rarossi
"""
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np

def on_move(event):
    for annot, line in zip(img_annotations, lines):
        try:
            on_move.ab.set_visible(False)
        except AttributeError:
            pass
        ax.format_coord = format_coord
        if line.contains(event)[0]:
            ind = line.contains(event)[1]["ind"]
            print(ind)
            on_move.ab = annot[ind[0]]
            on_move.ab.set_visible(True)
            ax.format_coord = lambda x, y: 'x = %.3f   y = %.3f   %s ' % (
                    x, y, on_move.ab.get_text())
    fig.canvas.draw_idle()
on_move.ab = None


def format_coord(x, y):
    return 'x = %.3f   y = %.3f' % (x, y)


if __name__ == '__main__':
    x = ss.gumbel_r.rvs(size=50)
    y = list(range(len(x)))
    s = sorted(range(len(x)), key=x.__getitem__)
    x.sort()

    fig, ax = plt.subplots()
    lines = [ax.scatter(x, y, c="red", picker=True, marker='*')]

    ax.format_coord = format_coord
    ia = lambda i: plt.annotate("Seed {}".format(s[i]+1), (x[i], y[i]), visible=False)
    img_annotations = [[ia(i) for i in range(len(x))]]

    fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.show()