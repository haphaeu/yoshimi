# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 16:03:29 2015

@author: rarossi
"""

import pandas as pd
import numpy as np
from scipy import stats as ss

#
# data = pd.read_table('data.txt')
data = pd.read_table('Results.txt')
#
# don't worry too much about this ugly generator,
# it just emulates the format of my data...
# total = 4500
# data = pd.DataFrame()
# data['Hs'] = np.random.randint(1,4,size=total)
# data['Tp'] = np.random.randint(5,15,size=total)
# data['wd'] = [[165, 180, 195][np.random.randint(0,3)] for _ in xrange(total)]
# data['seed'] = np.random.randint(1,51,size=total)
# data['Tmax'] = np.random.randint(100,250,size=total)
# data['Tmin'] = np.random.randint(10,25,size=total)

# %%
# and here it starts. would the creators of pandas pull their hair out if
# they see this?
# can this be made better?
cols = ['Hs', 'Tp']
cols.extend(data.columns[4:])
stdev = pd.DataFrame(columns=cols)
i = 0
for hs in set(data['Hs']):
    data_Hs = data[data['Hs'] == hs]
    for tp in set(data_Hs['Tp']):
        data_tp = data_Hs[data_Hs['Tp'] == tp]
        rw = [hs, tp]
        for c in cols[2:]:
            if c.lower().find('max') is not -1:  # max
                # # moment estimators
                # mx = max([np.mean(data_tp[data_tp['wd'] == wd][c]) +
                #           1.305*np.std(data_tp[data_tp['wd'] == wd][c])
                #           for wd in set(data_tp['wd'])])
                # MLE's
                mx = max([ss.gumbel_r(*ss.gumbel_r.fit(
                         data_tp[data_tp['wd'] == wd][c])).ppf(0.9)
                         for wd in set(data_tp['wd'])])
            else:
                # # moment estimators
                # mx = min([np.mean(data_tp[data_tp['wd'] == wd][c]) +
                #           1.305*np.std(data_tp[data_tp['wd'] == wd][c])
                #           for wd in set(data_tp['wd'])])
                # MLE's
                mx = min([ss.gumbel_l(*ss.gumbel_l.fit(
                         data_tp[data_tp['wd'] == wd][c])).ppf(0.1)
                         for wd in set(data_tp['wd'])])
            rw.extend([mx])
        stdev.loc[i] = rw
        i += 1

# adjust and sort index
stdev = stdev.sort_index(by=['Hs', 'Tp'])
stdev = stdev.reset_index()
del stdev['index']

# %%
# this works, but how to apply +/- depending on max/min
stdev3 = (1.305 * data.groupby(['Hs', 'Tp', 'wd'])[['Tmax', 'Tmin']].std() +
          data.groupby(['Hs', 'Tp', 'wd'])[['Tmax', 'Tmin']].mean()).max(
          level=[0, 1]).reset_index()


# %%
# this works for one variable only
# the .max(level=['Hs', 'Tp']) does the magic in getting the worst wave heading
stdev4 = data.groupby(['Hs', 'Tp', 'wd'])['Tmax'].apply(
                 lambda x: ss.gumbel_r(*ss.gumbel_r.fit(x)).ppf(0.9)).max(
                 level=['Hs', 'Tp']).reset_index()
# one possibility is to loop, once stdev4 is set, add Tmin with:
stdev4['Tmin'] = data.groupby(['Hs', 'Tp', 'wd'])['Tmin'].apply(
                 lambda x: ss.gumbel_l(*ss.gumbel_l.fit(x)).ppf(0.1)).min(
                 level=['Hs', 'Tp']).reset_index()['Tmin']


# %%
stdev['Tmax'].plot()
# stdev3['Tmax'].plot()
stdev4['Tmax'].plot(style='r--')

# %%
'''
# gumbel can be fit and frozen in one line by unpacking (*)
# the returned tuple from fit:
g = gumbel_l(*gumbel_l.fit(data))

# some tips to dataframe

stdev2 = data.groupby(['Hs', 'Tp', 'wd'])[['Tmax', 'Tmin']].std().max(
                                            level=[0, 1]).reset_index()


data.ix[0:4, ['Hs', 'Tp']]
data.ix[[0,10,22], ['Hs', 'Tp']]
data.get_value(0, 'Hs')

gb = data.groupby(['Hs', 'Tp', 'wd'])

def get_max_Tmax(group):
    return group.ix[group.Tmax.idxmax()]
data.groupby('Hs').apply(get_max_Tmax)
#apply can have arguments to func


res = data.groupby(['Hs','Tp'])['Tmax'].describe()



'''

# data=data.set_index(['Hs', 'Tp', 'wd'])
# gb = data.groupby(['Hs', 'Tp', 'wd'])
# res = gb.apply(max)
