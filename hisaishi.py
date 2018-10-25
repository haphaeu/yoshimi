#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Scrap a website to download Joe Hisaishi music.

Video Game Music
https://downloads.khinsider.com/


Created on Sun Sep  9 12:24:15 2018
@author: raf
"""

import urllib.request
import requests
import re
import os.path as osp
import os
import multiprocessing
import time

_path_data = '/home/raf/Music/'


def worker(arg):
    url, dst = arg
    fetch(url, dst)


def fetch(url, dst):
    """Downloads one file into dst directory.
    Skips if the destination file already exists.
    """
    fname = osp.join(dst, osp.basename(url.replace('%20', '_')))
    print(' ', fname)
    if not osp.exists(fname):
        try:
            urllib.request.urlretrieve(url, fname)
        except urllib.error.HTTPError:
            print('Skipping file not found on server:', url)
            pass
    return fname


def get_links(url):
    
    page = requests.get(url)
    cont = page.content.decode('utf-8')
    e = re.compile(r'.*href="([^"]*.mp3)".*', )
    hits = set(e.findall(cont, re.IGNORECASE))

    links = []
    for url in hits:
        url = 'https://downloads.khinsider.com' + url
        page = requests.get(url)
        cont = page.content.decode('utf-8')
        e = re.compile(r'.*href="([^"]*.mp3)".*', )
        file = e.findall(cont, re.IGNORECASE)
        if len(file) > 1:
            print('ooops... more than 1 song. Using first hit')
        links.append(file[0])
    return links

if __name__ == '__main__':
    urls = ['https://downloads.khinsider.com/game-soundtracks/album/joe-hisaishi-piano-stories-i',
            'https://downloads.khinsider.com/game-soundtracks/album/joe-hisaishi-piano-stories-ii',
            'https://downloads.khinsider.com/game-soundtracks/album/joe-hisaishi-piano-stories-iii',
            'https://downloads.khinsider.com/game-soundtracks/album/joe-hisaishi-symphonic-best-selection',
            'https://downloads.khinsider.com/game-soundtracks/album/joe-hisaishi-works-i',
            'https://downloads.khinsider.com/game-soundtracks/album/joe-hisaishi-works-ii',]

    pool = multiprocessing.Pool(processes=10)
    
    for url in urls:    

        album = osp.basename(url)
        print('Album: %s' % album)
        album_path = osp.join(_path_data, album)

        if not osp.exists(album_path):
            os.mkdir(album_path)
        
        songs_links = get_links(url)
        print(' Found %d songs' % len(songs_links))
        print(' Downloading...')
        time.sleep(0.1)
        
        res = pool.map(worker, zip(songs_links, [album_path]*len(songs_links)))
        
    
