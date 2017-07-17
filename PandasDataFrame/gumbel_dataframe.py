# -*- coding: utf-8 -*-
"""

Trying to improve the Gumbel module.

The idea is to apply functions staight from results.txt to get to results.

Created on Mon Jul 17 11:44:58 2017

@author: rarossi
"""
# %%
import pandas as pd
import numpy as np
from scipy import stats as ss


gamma = 0.5772  # Euler constant
need_more_seeds = 'need larger sample for this fractile'
use_sample = 'use sample'

pns = [0.9, 0.99]

# %%
# df = pd.read_table('results_mini.txt')
df = pd.read_table('results.txt')
keys = ['WaveHs', 'WaveTp', 'WaveDirection']
df = df.set_index(keys=keys)

# Split this in two dfs, one for max, one for min
df_max = df[df.columns[['max' in i.lower() for i in df.columns.values]]]
df_min = df[df.columns[['min' in i.lower() for i in df.columns.values]]]

# %%
# functions to be calculated for diagnosis


def betaME(x):
    return np.std(x)*(np.sqrt(6))/np.pi


def muME_min(x):
    return np.mean(x) + gamma*betaME(x)


def muME_max(x):
    return np.mean(x) - gamma*betaME(x)


def muMLE_min(x):
    return ss.gumbel_l.fit(x)[0]


def betaMLE_min(x):
    return ss.gumbel_l.fit(x)[1]


def muMLE_max(x):
    return ss.gumbel_r.fit(x)[0]


def betaMLE_max(x):
    return ss.gumbel_r.fit(x)[1]


def sample_min(x, pn=0.9):
    num_seeds = len(x)
    x = x.sort_values()
    i = int(num_seeds-pn*num_seeds)
    enoughSeeds = num_seeds >= round(1/(1-pn), 4)
    if not enoughSeeds:
        return need_more_seeds
    return x[i-1]


def gME_min(x, pn=0.9):
    if 0 in x.values:
        return use_sample
    return ss.gumbel_l.ppf(1-pn, *ss.gumbel_l._fitstart(x))


def gMLE_min(x, pn=0.9):
    if 0 in x.values:
        return use_sample
    return ss.gumbel_l.ppf(1-pn, *ss.gumbel_l.fit(x))


def sample_max(x, pn=0.9):
    num_seeds = len(x)
    x = x.sort_values()
    i = int(pn*num_seeds)
    enoughSeeds = num_seeds >= round(1/(1-pn), 4)
    if not enoughSeeds:
        return need_more_seeds
    return x[i-1]


def gME_max(x, pn=0.9):
    return ss.gumbel_r.ppf(pn, *ss.gumbel_r._fitstart(x))


def gMLE_max(x, pn=0.9):
    return ss.gumbel_r.ppf(pn, *ss.gumbel_r.fit(x))

agg_list_min = [np.std, np.mean, np.max, np.min, betaME, muME_min, betaMLE_min, muMLE_min]
agg_list_max = [np.std, np.mean, np.max, np.min, betaME, muME_max, betaMLE_max, muMLE_max]
for pn in pns:
    # All this thing with funcion names changes is because more than 1 lambda function
    # is not accepted by pandas in an aggregate list...
    label = '_{}'.format(pn).replace('.', '_')
    agg_list_min.extend([lambda x: gME_min(x, pn=pn),
                         lambda x: gMLE_min(x, pn=pn),
                         lambda x: sample_min(x, pn=pn)])
    agg_list_min[-3].__name__ = 'gME_min'+label
    agg_list_min[-2].__name__ = 'gMLE_min'+label
    agg_list_min[-1].__name__ = 'sample_min'+label
    agg_list_max.extend([lambda x: gME_max(x, pn=pn),
                         lambda x: gMLE_max(x, pn=pn),
                         lambda x: sample_max(x, pn=pn)])
    agg_list_max[-3].__name__ = 'gME_max'+label
    agg_list_max[-2].__name__ = 'gMLE_max'+label
    agg_list_max[-1].__name__ = 'sample_max'+label

# %%
# Do the magic - aggregate data frame from results.txt into the required output format

df_res = pd.concat([df_min.groupby(by=keys).agg(agg_list_min),
                    df_max.groupby(by=keys).agg(agg_list_max)], axis=1)

# Finally write results to excel.
# Note that sheet iterates through df.columns to keep original order of columns
xl_writer = pd.ExcelWriter('lixo.xlsx')
for sheet in df.columns:
    df_res[sheet].reset_index().to_excel(xl_writer, index=False, sheet_name=sheet)
xl_writer.save()


# %%
#                            .rename(columns={'amax': 'max', 'amin': 'min'})
# Old studd
#
#df_min.groupby(by=keys).describe(percentiles=[0.01, 0.1, 0.5, 0.9, 0.99]).head()
#
# Create a multiindex object for the results dataframe
## mindex = pd.MultiIndex.from_product(iterables=[['stdev', 'mean', 'max', 'min'], df.columns])

# Create a template for the results DataFrame. Keep same index, use the multi-index as columns
## df_res = pd.DataFrame(index=df[~df.index.duplicated(keep='first')].index, columns=mindex)
