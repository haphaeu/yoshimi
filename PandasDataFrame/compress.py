# -*- coding: utf-8 -*-
"""

Investigation on DataFrame siz eoptimisation for transfer.

Assumption that a CSV file is being written without memory efficiency concerns.

The CSV file is read as a DataFrame, which is memory optimised and gzip'ed into a file.


Created on Wed Oct 21 08:07:09 2020

@author: rarossi
"""

import numpy as np
import pandas as pd
import pickle as pk
import gzip as gz


def optimise(
        df: pd.DataFrame,
        verbose: bool = True
        ) -> pd.DataFrame:
    '''Optimise memory use of a DataFrame by setting column specific data types.
    '''
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2

    for col in df.columns:
        col_type = df[col].dtypes

        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                # This was too aggressive. float16 has only 4 significant digits
                # if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                #    df[col] = df[col].astype(np.float16)
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024**2

    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(
                end_mem, 100 * (start_mem - end_mem) / start_mem))

    return df


def zipit(obj, filename):
    '''Save a gzip compressed object into a file.'''
    with gz.GzipFile(filename, 'wb') as f:
        pk.dump(obj, f)


def unzip(filename):
    '''Load/Unzip a gzip compressed object from a file.'''
    with gz.GzipFile(filename, 'rb') as f:
        obj = pk.load(f)
    return obj


def test():

    # Create a large csv file, emulating a timetrace of a vessel MRU
    df0 = pd.DataFrame(
            data=np.array([365, 24, 10, 10, 10, 45, 45, 45, 9999, 9999, 360]) *
            np.random.random(size=(36000, 11)),
            columns=[
                'Date', 'Time', 'Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw',
                'GlobalX', 'GlobalY', 'Heading'
            ]
        )

    # Save dataframe to CSV file and to ZIP file
    df0.to_csv('data0.csv', index=False)
    zipit(df0, 'data0.zip')

    # Now, read that file, optimise df, and save again to CSV and ZIP
    df1 = optimise(pd.read_csv('data0.csv'))
    df1.to_csv('data1.csv', index=False)
    zipit(df1, 'data1.zip')

    # And finally, unzip the file
    df2 = unzip('data1.zip')

    # Compare memory usage
    df0.info(memory_usage='deep')
    df1.info(memory_usage='deep')
    df2.info(memory_usage='deep')

    # Compare precision
    assert np.allclose(df0, df1)
    assert np.allclose(df0, df2)
