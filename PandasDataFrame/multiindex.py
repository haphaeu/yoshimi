# -*- coding: utf-8 -*-
"""

Playing with MultiIndex'ed DataFrames.

This is to replace Panels, since they are deprecated.

Created on Mon Jul 17 11:12:19 2017

@author: rarossi
"""

import pandas as pd
import numpy as np
import itertools

loads = ['Crane Max Tension', 'Crane Min Tension', 'Sling1 Max Tension', 'Sling1 Min Tension',
         'Sling2 Max Tension', 'Sling2 Min Tension']

# Not sure about this one - maybe index could be a tuple (Hs, Tp, wd)
params = ['StDev', 'Mean', 'Max', 'Min', 'beta ME',
          'mu ME', 'beta MLE', 'mu MLE', 'g ME (0.9)', 'g ME (0.99)',
          'g MLE(0.9)', 'g MLE(0.99)', 'sample (0.9)', 'sample (0.99)']

Hss, Tps, WDs = [1.5, 2, 2.5], [8, 9, 10], [150, 180, 210]

index = list(itertools.product(Hss, Tps, WDs))

mindex = pd.MultiIndex.from_product([loads, params], names=['loads', 'params'])



df = pd.DataFrame(np.random.randn(len(index), len(loads)*len(params)), index=index, columns=mindex)

# From here, one can do:
df['Sling1 Max Tension']['g ME (0.99)']
# or - note that the tuple index must be wrapped in a list in order for this to work
df.loc[[(1.5, 8, 150)]]['Crane Max Tension']['sample (0.9)'].values
