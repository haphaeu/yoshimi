#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:49:39 2018

@author: raf
"""
import re
import pandas
import requests
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


base_url = 'https://www.finn.no/car/used/'

# This is the entry page for car search in finn
search_url = base_url + 'search.html'

# This is the url for ads, finn_kode to be filled in
ad_url =     base_url + 'ad.html?finnkode={}'

# Codes for fuel types
fuel_types = {'Bensin': 'engine_fuel=0%2F1',
              'Diesel': 'engine_fuel=0%2F2',
              'Hybrid': 'engine_fuel=0%2F11111',
              'Electric': 'engine_fuel=0%2F4'
             }

# Codes for karosseri type
karosseri_types = {'Stasjonsvogn': 'body_type=4',
                   'SUV': 'body_type=9'
                   # only these 2 for now...
                  }

# All cars maker, model and codes
makers_and_models = dict()


def fetch_makers_and_models():
    '''initialised global variable makers_and_models with all cars makers and models in finn.
    '''
    global makers_and_models
    
    page = requests.get(search_url)
    cont = page.content.decode()
    parsed = BeautifulSoup(cont, 'lxml')
    
    # regex to match name and count from 'name (count)'
    # name might have parenthesis, and finn might put lots of crap like \xa0085 on the side 
    # of the numbers in count...
    expr = re.compile('(.+)\((\d+).*\)')  
    
    for hit in parsed.body.find_all('div', attrs={'class': 'fancyinput'}):
        hit_maker = hit.find('input', attrs={'name': 'make'})
        hit_model = hit.find('input', attrs={'name': 'model'})
        if hit_maker:
            maker_value = hit_maker.attrs['value']
            maker, count = expr.findall(hit.find('span').text.replace('\xa0', ''))[0]
            maker = maker.strip()
            count = int(count)
            makers_and_models[maker] = {'value': maker_value, 'count': count, 'models': {}}
        elif hit_model:
            model_value = hit_model.attrs['value']
            model, count = expr.findall(hit.find('span').text.replace('\xa0', ''))[0]
            model = model.strip()
            count = int(count)
            makers_and_models[maker]['models'][model] = {'value': model_value, 'count': count}
    
    
def build_url(makers_and_models, maker, model, fuel=None, karosseri=None):
    '''Returns a valid search URL to be used in finn.no
    '''
    try:
        url = search_url + '?model=' + makers_and_models[maker]['models'][model]['value']
        if fuel:
            url += '&' + fuel_types[fuel]
        if karosseri:
            url += '&' + karosseri_types[karosseri]
        return url
    except KeyError:
        print('Invalid maker, model, fuel or karosseri name.')


# this method was stupid... see below new function
#def getdata(url):
#    '''Get car year, km and price from one page in finn.no.
#    '''
#    page = requests.get(url)
#    cont = page.content.decode()
#    parsed = BeautifulSoup(cont, 'lxml')
#    data = list()
#    search = ['year', 'km', 'kr']
#    now = 0
#    for i, hit in enumerate(parsed.body.find_all(
#                            'span', attrs={'data-automation-id': 'bodyRow'})):
#        if search[now] == 'year':
#            if 1990 < int(hit.text) < 2020:
#                year = int(hit.text)
#                now = 1
#            else:
#                continue
#        elif search[now] == 'km':
#            if 'km' in hit.text:
#                km = int(hit.text[:-2].replace(u'\xa0', ''))
#                now = 2
#            else:
#                now = 0
#                continue
#        elif search[now] == 'kr':
#            if ',-' in hit.text:
#                kr = int(hit.text[:-2].replace(u'\xa0', ''))
#                now = 0
#                data.append((year, km, kr))
#            else:
#                now = 0
#                continue
#    return pandas.DataFrame(data, columns=search)

def getdata(url):
    '''Get car year, km and price from one page in finn.no.
    '''
    page = requests.get(url)
    cont = page.content.decode()
    parsed = BeautifulSoup(cont, 'lxml')
    data = list()

    for i, hit in enumerate(parsed.body.find_all('div', 
                                                 attrs={'class':
                                                 'unit flex align-items-stretch result-item'})):

        finn_kode = hit.find('a')['data-finnkode']
        
        hit_year = hit.find('span', attrs={'class': 'prm inlineblockify'})
        year = int(hit_year.text)
        
        hit_km = hit_year.find_next('span', attrs={'class': 'prm inlineblockify'})
        km = int(hit_km.text[:-2].replace(u'\xa0', ''))
    
        hit_kr = hit_km.find_next('span', attrs={'class': 'prm inlineblockify'})
        try:
            kr = int(hit_kr.text[:-2].replace(u'\xa0', ''))
        except ValueError:  # Sold cars have a string instead of price
            kr = hit_kr.text
            #continue
          
        data.append((year, km, kr, finn_kode))

    return pandas.DataFrame(data, columns=['year', 'km', 'kr', 'kode'])


def getalldata(search_url):
    '''Call getdata() for all pages available in finn.no.
    '''
    # Make sure to tick only Brukt bil til salgs
    brukt_bil_str = '&sales_form=1'
    if brukt_bil_str not in search_url:
        search_url += brukt_bil_str

    print('Fetching page 1')
    dataf = getdata(search_url)
    for page in range(2, 999):
        print('Fetching page', page)
        url_next = search_url + '&page=%d' % page
        tmp_df = getdata(url_next)
        if len(tmp_df) < 2:  # stop when page has 1 or 0 cars
            break
        dataf = dataf.append(tmp_df)
    # fix index
    dataf = dataf.reset_index()
    del dataf['index']

    return dataf


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Experimental functions - get detailed data for each car

def get_detailed_car_data(finn_kode):
    '''Get more detailed data for one car.
    
    Test - just getting number of car owners for now.
    '''
    page = requests.get(ad_url.format(finn_kode))
    cont = page.content.decode()
    parsed = BeautifulSoup(cont, 'lxml')
    
    for hit in parsed.body.find_all('dt', attrs={'data-automation-id': 'key'}):
        if hit.text.lower().strip() == 'antall eiere':
            value = hit.find_next('dd').text
            break
    else:
        value = 'na'
    
    return value

def get_all_detailed(data):
    '''Call get_detailed_car_data for all cars in the database.
    
    SKETCH - just printing out to screen for now.
    '''
    I = len(data)
    for i, car in enumerate(data):
        print(i, I, car)
        J = len(data[car].kode)
        for j, kode in enumerate(data[car].kode):
            print('  ', j, J, kode, get_detailed_car_data(kode))

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

    
def getstats(dataf):
    '''Calculate statistics for the data fetched.
    '''
    # dataf = dataf[dataf.kr != 'Solgt']  # get rid of sold cars for stats
    dataf = dataf[dataf.kr.apply(np.isreal)]
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
    years = list(stats.keys())
    years.sort()
    print('year \t  # \t km ave \t km std \t kr ave \t kr std ')
    for year in years:
        print('%d \t %2d \t %6d \t %6d \t %6d \t %6d ' % (
                year, stats[year]['count'], stats[year]['km mean'], stats[year]['km std'],
              stats[year]['kr mean'], stats[year]['kr std']))


def plot_all_stats(stats, norm=False, err_bars=False, min_year_user=0):

    plt.figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')

    max_price = 0
    min_year = 2020
    for car in stats:
        years = [year for year in stats[car]]
        years.sort()
        price = [stats[car][year]['kr mean']/1000 for year in years]
        p_err = [stats[car][year]['kr std']/1000 for year in years]

        if norm:
            p_err = [yi/max(price) for yi in p_err]
            price = [yi/max(price) for yi in price]

        if err_bars:
            plt.errorbar(years, price, yerr=p_err, label=car, lw=2, elinewidth=1)
        else:
            plt.plot(years, price, label=car, lw=2)

        min_year = min(min_year, years[0])
        max_price = max(max_price, max(price))

    plt.title(('Normalised ' if norm else '') + 'Car Price Depreciation - source: finn.no',
              fontsize=20)
    plt.xlabel('Car Year')
    plt.ylabel('Average Price in 1000 NOK')
    plt.legend(loc='best', fontsize=14)
    plt.grid()
    min_year = max(min_year, min_year_user)
    plt.xlim(min_year, years[-1])
    plt.xticks(range(min_year, years[-1]+1, 1))
    if norm:
        plt.ylim(0, 1)
        plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    else:
        plt.ylim(0, max_price)
        plt.yticks(range(0, int(max_price)+1, 50))
    plt.show()


class Car():
    '''Simple class to handle input of cars
    '''
    def __init__(self, maker, model, fuel=None, karosseri=None):
        self.maker = maker
        self.model = model
        self.fuel = fuel
        self.karosseri = karosseri
        
        self.id = ' '.join([maker, model])
        if fuel:
            self.id += ' ' + fuel
        if karosseri:
            self.id += ' ' + karosseri
            
        self.url = build_url(makers_and_models, maker, model, fuel, karosseri)


if __name__ == '__main__':

    print('Fetching makers and models from finn.no. ', end='')
    fetch_makers_and_models()
    print('Done')
    
    # Cars to be searched for
    #            maker, model, fuel=None, karosseri=None)
    cars = [Car('Toyota', 'Avensis', 'Diesel'),
            Car('Renault', 'Megane'),
            # Car('Volvo', 'XC 90'),
            #Car('Nissan', 'Leaf'),
            #Car('Volvo', 'V60'),
            #Car('Toyota', 'Auris'),
           ]

    try:
        data
    except NameError:
        data = dict()
        
    stats = dict()
        
    for car in cars:
        
        print('\n', '='*len(car.id), '\n', car.id, '\n', '='*len(car.id), '\n')
        if car.id not in data:
            data[car.id] = getalldata(car.url)
        else:
            print(car.id, 'already in the database.')
        
        print('Found', len(data[car.id]), 'entries.')
        stats[car.id] = getstats(data[car.id])
        print_stats(stats[car.id])
        print()

    plot_all_stats(stats)
