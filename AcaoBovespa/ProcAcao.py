import urllib2
import sys

"""
ProcAcao.py
===========

   Script tosco pra buscar o preco e a oscilacao de acoes da BOVESPA.
   http://www.bmfbovespa.com.br/
   O script usa a busca "Cotacao Rapida" do site da BOVESPA, baixa
   a pagina e procura na pagina coringas que indicam onde esta o preco e a oscilacao.
   Tratamento de erro tosco e basico implementado para entradas de simbolos invalidos.

    Rafael Rossi - 25/08/2010

"""

if len(sys.argv)>1:
    for symbol in sys.argv[1:]:
        #busca pagina da Bovespa
        url="http://www.bmfbovespa.com.br/Cotacao-Rapida/ExecutaAcaoCotRapXSL.asp?gstrCA=&txtCodigo=%s&intIdiomaXsl=0" % symbol
        request=urllib2.Request(url)
        opener = urllib2.build_opener()
        #retval fica com o conteudo retornado pela bovespa
        retval = opener.open(request).read()
        #verifica se ativo existe e procura pelo preco - de forma tosca :)
        inicio= retval.find("R$")
        if inicio==-1:
            print "%s\tinexistente." %symbol
            continue
        inicio+=2
        final= retval.find("</td>",inicio)
        valor = retval[inicio:final].strip()
        #procura pela oscilacao - de forma mais tosca ainda
        inicio = retval.find("ValorPositivo")
        if inicio==-1:
            inicio = retval.find("ValorNegativo")
        inicio+=15
        final=retval.find("</span>",inicio)
        osc = retval[inicio:final].strip()
        #saida de resultados        
        print "%s\tR$ %s\t%s" % (symbol, valor, osc)
else:
    print "Uso: ProcAcao simbolo1 [simbolo2 simbolo3 ...]"