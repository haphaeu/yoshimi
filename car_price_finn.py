#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:49:39 2018

@author: raf
"""
import pandas
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def getdata(url):
    '''Get car year, km and price from one page in finn.no.
    '''
    page = requests.get(url)
    cont = page.content.decode()
    parsed = BeautifulSoup(cont, 'lxml')
    data = list()
    search = ['year', 'km', 'kr']
    now = 0
    for i, hit in enumerate(parsed.body.find_all(
                            'span', attrs={'data-automation-id': 'bodyRow'})):
        if search[now] == 'year':
            if 1990 < int(hit.text) < 2020:
                year = int(hit.text)
                now = 1
            else:
                continue
        elif search[now] == 'km':
            if 'km' in hit.text:
                km = int(hit.text[:-2].replace(u'\xa0', ''))
                now = 2
            else:
                now = 0
                continue
        elif search[now] == 'kr':
            if ',-' in hit.text:
                kr = int(hit.text[:-2].replace(u'\xa0', ''))
                now = 0
                data.append((year, km, kr))
            else:
                now = 0
                continue
    return pandas.DataFrame(data, columns=search)


def getalldata(base_url):
    '''Call getdata() for all pages available in finn.no.
    '''
    print('Fetching page 1')
    dataf = getdata(base_url)
    for page in range(2, 999):
        print('Fetching page', page)
        url_next = base_url + '&page=%d' % page
        tmp_df = getdata(url_next)
        if len(tmp_df) < 2:  # stop when page has 1 or 0 cars
            break
        dataf = dataf.append(tmp_df)
    # fix index
    dataf = dataf.reset_index()
    del dataf['index']
    
    return dataf


def getstats(dataf):
    '''Calculate statistics for the data fetched.
    '''
    years = list(set(dataf.year))
    years.sort()
    stats = dict()
    for year in years:
        tmp = dataf[dataf.year == year]
        stats[year] = {'count': len(tmp), 
                       'km mean': int(tmp.km.mean()), 'km std': int(tmp.km.std(ddof=0)),
                       'kr mean': int(tmp.kr.mean()), 'kr std': int(tmp.kr.std(ddof=0))}
    return stats


def print_stats(stats):
    '''Print statistics from getstats().
    '''
    print('year \t  # \t km ave \t km std \t kr ave \t kr std ')
    for key in stats:
        print('%d \t %2d \t %6d \t %6d \t %6d \t %6d ' % (
                key, stats[key]['count'], stats[key]['km mean'], stats[key]['km std'], 
              stats[key]['kr mean'], stats[key]['kr std']))


def plot_all_stats(stats, norm=False):
    
    plt.figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    
    for car in stats:
        x = [year for year in stats[car]]
        y = [stats[car][year]['kr mean'] for year in stats[car]]
        if norm:
            ymx = max(y)
            y = [yi/ymx for yi in y]
        plt.plot(x, y, label=car)
        
    plt.title(('Normalised ' if norm else '') + 'Car Price Depreciation Curve',
              fontsize=16)
    plt.legend()
    plt.grid()
    plt.xlim((2000, 2020))
    plt.xticks(range(2000, 2021, 1))
    if norm:
        plt.ylim(0, 1)
        plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    else:
        plt.ylim(ymin=0)
        plt.yticks(range(0, 1000001,50000))
    plt.show()
        

if __name__ == '__main__':
    
    # Remember to tick Brukt bil til salgs, to remove leasing shit
    # append '&sales_form=1' to the url.
    cars = {'Toyota Avensis Stasjonvogn Diesel':
                'https://www.finn.no/car/used/search.html?body_type=4&engine_fuel=0%2F2&make=0.813&model=1.813.3252&sales_form=1',
            'Renault Megane Stasjonvogn Diesel':
                'https://www.finn.no/car/used/search.html?body_type=4&engine_fuel=0%2F2&make=0.804&model=1.804.1331&sales_form=1',
            'Volvo XC 90':
                'https://www.finn.no/car/used/search.html?make=0.818&model=1.818.7651&sales_form=1',
            'Audi A6 Diesel':
                'https://www.finn.no/car/used/search.html?engine_fuel=0%2F2&make=0.744&model=1.744.840&sales_form=1',
            'Audi A4 Diesel Stasjonsvogn':
                'https://www.finn.no/car/used/search.html?body_type=4&engine_fuel=0%2F2&make=0.744&model=1.744.839&sales_form=1',
            'Audi A4 Bensin Stasjonsvogn':
                'https://www.finn.no/car/used/search.html?body_type=4&engine_fuel=0%2F1&make=0.744&model=1.744.839&sales_form=1',
            'VW Touran':
                'https://www.finn.no/car/used/search.html?make=0.817&model=1.817.7593&sales_form=1',
            'Tesla S':
                'https://www.finn.no/car/used/search.html?make=0.8078&model=1.8078.2000138&sales_form=1',
            'Nissan Leaf':
                'https://www.finn.no/car/used/search.html?engine_fuel=0%2F4&make=0.792&model=1.792.2000183&sales_form=1',
                
            }
    
    data = dict()
    stats = dict()
    for car in cars:
        print('\n', '='*len(car), '\n', car, '\n', '='*len(car), '\n')
        data[car] = getalldata(cars[car])
        print('Found', len(data[car]), 'entries.')
        stats[car]=getstats(data[car])
        print_stats(stats[car])
        print()
        
    plot_all_stats(stats, False)
    
