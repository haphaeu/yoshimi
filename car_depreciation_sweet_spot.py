# -*- coding: utf-8 -*-
"""

Attempt to model the yearly car cost to find the sweet spot to sell/buy.

The code models selling an s-years old car, and buying a b-years old car. Assuming the car to be
bought is newer than the car being sold (b < s). Also assumes that we're going to stick to the
newly bought car for at lest 4 years (s-b > 4), when the same processes repeats.

The net cost of car change, plus the maintenance paid in the years of owning the car are
calculated and divided by the number of years, so it is an yearly cost.

The comfort and safety of a new car is not taken into account.

===
Need more work to get meaninfull data for the car_price and car_maintenance functions.
===


Created on Thu Oct 25 12:00:22 2018
@author: rarossi
"""
import matplotlib.pyplot as plt
import pandas as pd


def car_price(n):
    '''value of a n years old car'''
    #         0    1    2    3    4   5   6   7   8   9   10
    return [300, 220, 175, 140, 100, 80, 50, 40, 20, 15,  10][n]


def car_maintenance(n):
    '''yearly maintenance costs of a n years old car
    '''
    # constant costs: fees, fuel, toll
    cte = 10
    # variable costs: insurance, garage, parts,
    #      0  1  2  3  4  5  6  7  8  9  10
    var = [3, 3, 3, 3, 3, 3, 7, 5, 6, 7, 10][n]
    return cte + var


y = list(range(10))
p = [car_price(i) for i in y]
plt.plot(y, p)
plt.show()

data = []
for buy in range(6):
    for sell in range(buy+4, 11):
        cost = int((car_price(sell) - car_price(buy) -
                    sum([car_maintenance(i) for i in range(buy, sell)])) / (sell-buy))
        data.append([sell, buy, cost])

dataf = pd.DataFrame(data=data, columns=['sell', 'buy', 'cost'])

# normalise cost based on the minimum loss and show as integer percent points
dataf.cost /= max(dataf.cost)/100
dataf.cost -= 100
dataf.cost = dataf.cost.apply(int)

table = dataf.pivot_table(values='cost', columns='sell', index='buy', fill_value='')
print('Increase in costs from cheapest option - in percent points')
print(table)
