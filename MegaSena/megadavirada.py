#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       megadavirada.py - Script para conferir resultados da Mega Sena (Loteria Brasileira)
#
#       Copyright 2010 Thomas Jefferson Pereira Lopes <thomas@thlopes.com>
#
#       Uso: python megadavirada.py CONCURSO ARQUIVO
#         CONCURSO = número do concurso a conferir, por exemplo, 1245
#         ARQUIVO = nome do arquivo com os jogos, na seguinte sintaxe:
#           nomedojogador1
#           1,2,3,4,5,6
#           4,19,34,48,53
#           nomedojogador2
#           5,20,35,49,54
#           ...
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.

import sys
import urllib2
from BeautifulSoup import BeautifulSoup

def checa_jogo(sorteio, jogo):
    acertos = 0
    for numero in sorteio:
        if (numero in jogo):
            acertos += 1
    return acertos

def main():
    concurso = 1245
    nome_arquivo = 'jogos.txt'
    if (len(sys.argv) > 1):
        concurso = sys.argv[1]
    if (len(sys.argv) > 2):
        nome_arquivo = sys.argv[2]
    
    # checar arquivo
    try:
        arquivo_jogos = open(nome_arquivo, 'r')
    except:
        print "ERRO: Arquivo não encontrado!!!"
        sys.exit(1)
    
    print "Buscando resultado do Concurso %s" % (concurso)
    urlcaixa = "http://www1.caixa.gov.br/loterias/loterias/megasena/megasena_pesquisa_new.asp?submeteu=sim&opcao=concurso&txtConcurso=%s" % (concurso)
    html = urllib2.urlopen(urlcaixa).read()
    soup = BeautifulSoup(html)
    
    numeros_sorteados = soup.findAll('span','num_sorteio')
    
    if (len(numeros_sorteados) == 0):
        print "ERRO: Sorteio não localizado!!!"
        sys.exit(1)
    
    numeros_sorteados = numeros_sorteados[1].findAll('li')
    jogo_sorteado = [int(num.string) for num in numeros_sorteados]
    print "Números sorteados: %s" % (jogo_sorteado)

    # lendo jogos do arquivo
    linhas = arquivo_jogos.readlines()
    counter = 1
    print "Conferindo Jogos"
    
    total_premiados = 0
    
    for linha in linhas:
        if "," not in linha:
            print "================"
            print linha.strip().upper()
            counter = 1
        else:
            jogo = map(int,linha.split(','))
            resultado = checa_jogo(jogo_sorteado, jogo)
            if (resultado > 3):
                    print "\nAcertos: ***  %s *** - Jogo %s: %s\n" % (resultado,counter,jogo)
                    total_premiados += 1
            else:
                print "Acertos: %s - Jogo %s: %s" % (resultado,counter,jogo)
            counter += 1
    
    print "================"
    print "Total de Jogos premiados: %s" % (total_premiados)

if (__name__ == '__main__'):
    main()

