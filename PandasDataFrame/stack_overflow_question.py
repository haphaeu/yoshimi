'''
My data consists of 1000 samples, each sample containing 10 numbers (floats).
This data is stored in a pandas DataFrame using multi-indexing (2 levels columns, 3 levels rows).

For each os these 1000 samples, I need to describe it, fit it to Gumbel distributions using ME and MLE and save the ppf for a few fractiles.

I'm assuming that the more built-in numpy and pandas functions I use, and the more vectorisation is done, the more optimised the run would be.

But I'm not convinced that I can't get run time much below 10s... seems too much.

Question is: is this as fast as a complex DataFrame aggregation gets to be? Any hint on further run time optimisation here?

Here is a sample code:
'''
import pandas as pd
import numpy as np
from scipy import stats as ss
import pickle

class MemoizeMutable:
    """Memoize decorator for unhashable items, using pickle"""
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args, **kwds):
        str = pickle.dumps(args, 1)+pickle.dumps(kwds, 1)
        if str not in self.memo:
            self.memo[str] = self.fn(*args, **kwds)
        return self.memo[str]


# %%
# functions to be calculated for diagnosis
# using MemoizeMutable for the functions that need to be called more
# than once - assuming calling aggregate only once will give faster
# runs...


#@MemoizeMutable
def gME_min_fit(x):
    return ss.gumbel_l._fitstart(x)


#@MemoizeMutable
def gMLE_min_fit(x):
    return ss.gumbel_l.fit(x)


#@MemoizeMutable
def gME_max_fit(x):
    return ss.gumbel_r._fitstart(x)


#@MemoizeMutable
def gMLE_max_fit(x):
    return ss.gumbel_r.fit(x)


def muME_min(x):
    return gME_min_fit(x)[0]


def muME_max(x):
    return gME_max_fit(x)[0]


def betaME_min(x):
    return gME_min_fit(x)[1]


def betaME_max(x):
    return gME_max_fit(x)[1]


def muMLE_min(x):
    return gMLE_min_fit(x)[0]


def betaMLE_min(x):
    return gMLE_min_fit(x)[1]


def muMLE_max(x):
    return gMLE_max_fit(x)[0]


def betaMLE_max(x):
    return gMLE_max_fit(x)[1]


def sample_min(x, pn=0.9):
    num_seeds = len(x)
    x = x.sort_values()
    i = int(num_seeds-pn*num_seeds)
    enoughSeeds = num_seeds >= round(1/(1-pn), 4)
    if not enoughSeeds:  # sample too small
        return need_more_seeds
    return x[i-1]


def sample_max(x, pn=0.9):
    num_seeds = len(x)
    x = x.sort_values()
    i = int(pn*num_seeds)
    enoughSeeds = num_seeds >= round(1/(1-pn), 4)
    if not enoughSeeds:  # sample too small
        return need_more_seeds
    return x[i-1]


def gME_min(x, pn=0.9):
    if 0 in x.values:  # can't fit zero bounded samples
        return use_sample
    return ss.gumbel_l.ppf(1-pn, *gME_min_fit(x))


def gME_max(x, pn=0.9):
    return ss.gumbel_r.ppf(pn, *gME_max_fit(x))


def gMLE_min(x, pn=0.9):
    if 0 in x.values:  # can't fit zero bounded samples
        return use_sample
    return ss.gumbel_l.ppf(1-pn, *gMLE_min_fit(x))


def gMLE_max(x, pn=0.9):
    return ss.gumbel_r.ppf(pn, *gMLE_max_fit(x))


# ## Some set-up
gamma = 0.5772  # Euler constant
need_more_seeds = 'need larger sample for this fractile'
use_sample = 'use sample'

pns = [0.75, 0.9, 0.99]

# emulate my data format...
mindex = pd.MultiIndex.from_product([range(5), range(7), range(3), range(10)],
                                     names=['A', 'B', 'C', 'D'])
cols = ['Max A', 'Min A', 'Max B', 'Min B', 'Max C', 'Min C', 'Max D', 'Min D', 'Max E', 'Min E']
df = pd.DataFrame(data=np.random.random(size=(len(mindex), len(cols))), index=mindex, columns=cols)
df[df < 0.05] = 0  # add some zeros to the data, similarly to the original data...
#

# Split this in two dfs, one for max, one for min, due to different kind of fit.
df_max = df[df.columns[['max' in i.lower() for i in df.columns.values]]]
df_min = df[df.columns[['min' in i.lower() for i in df.columns.values]]]


# List of functions to be used for aggragation of the DataFrame
agg_list_min = [np.std, np.mean, np.max, np.min,
                betaME_min, muME_min, betaMLE_min, muMLE_min]
agg_list_max = [np.std, np.mean, np.max, np.min,
                betaME_max, muME_max, betaMLE_max, muMLE_max]

# And complement that list with user specific fractiles...
for pn in pns:
    # All this thing with function names changes is because
    # more than 1 lambda function is not accepted by pandas
    # in an aggregate list...
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
# Do the magic - aggregate data frame from results.txt into the
# required output format
# Note that some effort is put above to get this call simple. But it
# doesn't seem to be helping.
# This call alone takes most of the running time...

df_res = pd.concat([df_min.groupby(by=['A', 'B', 'C']).agg(agg_list_min),
                    df_max.groupby(by=['A', 'B', 'C']).agg(agg_list_max)], axis=1)

# after this is just saving df_res[col].to_excel(wrt, sheet_name=col) for all cols...
