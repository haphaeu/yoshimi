# -*- coding: utf-8 -*-
"""
Scrapping of weightmyrack.com

Loads properties tables for types of gear.


@author: haphaeu
@date: 2017-08-29
"""

import pandas as pd
import requests
import pickle
import re
import os


def pickle_name(item_type):
    return 'weightmyrack_%s.pickle' % item_type


def load_database(item_type='Carabiner'):
    name = pickle_name(item_type)
    if os.path.exists(name):
        print('Loading existing database')
        with open(name, 'rb') as handle:
            return pickle.load(handle)
    else:
        return dict()


def save_database(table, item_type='Carabiner'):
    name = pickle_name(item_type)
    with open(name, 'wb') as handle:
        pickle.dump(table, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_names(item_type='Carabiner'):
    """Gets the name of all available items in the site.
    item_type must match the names used in the site:
        Carabiner
        Cams
        etc...
    """
    url = 'http://weighmyrack.com/%s/index.html' % item_type
    page = requests.get(url)
    cont = page.content.decode('utf-8')

    print('Filtering available items')
    e = re.compile(r'.*href="/%s/([^"]*)".*' % item_type, )
    return e.findall(cont, re.IGNORECASE)


def remove_units(biners):
    """obsolete. not used..."""
    params = ['Weight (g)', 'Gate Opening']
    for b in biners.keys():
        for p in params:
            try:
                biners[b][p] = int(biners[b][p].split()[0])
            except:
                if isinstance(biners[b][p], str):
                    biners[b][p] = 999


def to_dataframe(table):
    df = pd.DataFrame(data=table)
    return df.transpose()


def get_specs(table, item_names, item_type='Carabiner'):
    """Retrieves the specs-table of an item and saves it to a dictionary.
    A pickle is saved after every item so that a broken loading can be resumed.
    """
    for i, name in enumerate(item_names):
        print('%d/%d %s' % (i+1, len(item_names), name))
        url = 'http://weighmyrack.com/%s/' % item_type + name
        try:
            tbl = pd.read_html(url, index_col=0, attrs={'class': 'technical-specs table'})[0]
        except ValueError:
            print('    funny things happening... skipping this one...')
            continue
        tbl.index = [i[:20] for i in tbl.index]
        specs = {p: v[0] for p, v in zip(tbl.index, tbl.values)}
        table[name] = specs
        save_database(table, item_type)


def main():

    item_types = ['Carabiner', 'Cam']
    dataframes = dict()

    for item_type in item_types:
        print('Scrapping weightmyrack for %s' % item_type)

        print('Retrieving page contents')
        item_names = set(get_names(item_type))
        print('Found %d items of type %s' % (len(item_names), item_type))

        table = load_database(item_type)
        if table:
            print('Database contains %d items' % len(table))
            item_names -= table.keys()

        print('Items to be retrieved: %d' % len(item_names))
        print('Retrieving specs for all items')
        get_specs(table, item_names, item_type)

        save_database(table, item_type)

        dataframes[item_type] = to_dataframe(table)

    writer = pd.ExcelWriter('weightmyrack.xlsx')
    for key in dataframes.keys():
        dataframes[key].to_excel(writer, sheet_name=key)
    writer.save()


if __name__ == '__main__':
    main()
