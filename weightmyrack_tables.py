# -*- coding: utf-8 -*-
"""
Scrapping of weightmyrack.com

Loads properties tables for all carabiners.

Saves a pickle with a dictionary
{name: {param1: value1, param2: value2, ...}, ...}
"""

from lxml import html
import pandas as pd
import requests
import pickle
import re
import os


def load_database(name='weightmyrack_biners.pickle'):
    if os.path.exists(name):
        print('Loading existing database')
        with open(name, 'rb') as handle:
            return pickle.load(handle)
    else:
        return dict()


def save_database(biners_table, name='weightmyrack_biners.pickle',):
    with open(name, 'wb') as handle:
        pickle.dump(biners_table, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_biners_names():
    print('Retrieving page contents')
    url = 'http://weighmyrack.com/Carabiner/index.html'
    page = requests.get(url)
    cont = page.content.decode('utf-8')
    
    print('Filtering available carabiners')
    e = re.compile(r'.*href="/[cC]arabiner/([^"]*)".*')
    return e.findall(cont)


def remove_units(biners):
    params = ['Weight (g)', 'Gate Opening']
    for b in biners.keys():
        for p in params:
            try:
                biners[b][p] = int(biners[b][p].split()[0])
            except:
                if isinstance(biners[b][p], str):
                    biners[b][p] = 999


def to_dataframe(biners_table, ):
    df = pd.DataFrame(data=biners_table)
    return df.transpose()


def get_biners_specs(biners, biners_table):
                    
    for i, biner in enumerate(biners):
        print('%d/%d %s' % (i+1, len(biners), biner))
        url = 'http://weighmyrack.com/Carabiner/' + biner
#        page = requests.get(url)
#        tree = html.fromstring(page.content)
#        params = tree.xpath('//td[@class="specs-property"]/text()')
#        values = [v.strip() for v in tree.xpath('//td[@class="specs-value"]/text()')]
#        specs = {p: v for p, v in zip(params, values)}
#        # adding the 3 strengths as a list of 3 values:
#        try:
#            specs[params[-1]] = values[-3:]
#            biners_table[biner] = specs
#            save_database(biners_table)
#        except:
#            print('   funny biner found... getting rid of it...')
        tbl = pd.read_html(url, index_col=0)[0]
        tbl.index = [i[:20] for i in tbl.index]
        specs = {p: v[0] for p, v in zip(tbl.index, tbl.values)}
        biners_table[biner] = specs


def main():
    print('Scrapping weightmyrack for biners')
    
    biners = set(get_biners_names())
    print('Found %d carabiners' % len(biners))
    
    biners_db = load_database()
    if biners_db:
        print('Database contains %d biners' % len(biners_db))
        biners -= biners_db.keys()
    
    print('Carabiners to be retrieved: %d' % len(biners))
    print('Retrieving specs for all carabiners')
    get_biners_specs(biners, biners_db)
    
    remove_units(biners_db)
    save_database(biners_db)
    
    df = to_dataframe(biners_db)
    # df.to_excel('weightmyrack_biners.xlsx')
    


if __name__ == '__main__':
    main()
