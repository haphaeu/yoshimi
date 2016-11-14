# -*- coding: utf-8 -*-
"""

Monitora um arquivo por mudancas.

Usando .readline() cada linha alterada sera detectada e mostrada na tela.
Usando .readlines() pode-se detectar uma mudanca e mostrar somente a ultima linha do arquivo.

Created on Mon Nov 14 20:25:01 2016

@author: raf
"""
import time


def todas():
    file = open('file.txt')
    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            print(line, end='')


def ultima():
    file = open('file.txt')
    while True:
        where = file.tell()
        line = file.readlines()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            print(line[-1], end='')
