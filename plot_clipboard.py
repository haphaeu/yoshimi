# -*- coding: utf-8 -*-
"""

Plot data from clipboard.

Use:
    1. Select the data as text or spreadsheet and copy them into the clipboard
    3. Run the lines below "pd.read_clipboard()" for each variable you want.
       This will import the data into a Pandas DataFrame. If the header row
       is also copied into clipboard, it will be the name of the dataframe column
       with the data.
    4. Plot them using pyplot by selecting the columns you want plotted.

To import data from Orcaflex, just extract data as values and copy it.

This script is not supposed to be run. Import from clipboard should be executed
line by line.

Created on Fri Nov  3 08:13:17 2017
@author: rarossi
"""
# %%
import pandas as pd
from matplotlib import pyplot as plt

# %%
input('Copy data to clipboard and press any key\n')
correct = pd.read_clipboard()

input('Copy data to clipboard and press any key\n')
wrong = pd.read_clipboard()

# %%
plt.plot(correct.Time, correct.Tension, label='correct')
plt.plot(wrong.Time, wrong.Tension, label='wrong')

plt.grid()
plt.legend(loc='best')
