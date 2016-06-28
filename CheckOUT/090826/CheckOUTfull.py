import os
import sys

class Fim():
# Classe definida para terminar o programa
# caso todos os casos todem
    pass

def ProcuraMortosFeridos(ListaArquivosOUT):
# Procura pelos arquivos que nao rodaram
# ListaArquivos: lista de arquivos .out
#
# para arquivo em ListaArquivos, procura por uma
# string para ver se a analyse nao rodou
    try:
        Indice_Lista = 0
        tmp=0
        Indice_MortosFeridos = []
        ListaMortosFeridos=[]
        for ArquivoOUT in ListaArquivosOUT:
            try:
                pFile = open(ArquivoOUT,'r')
            except:
                print "Erro ao ler arquivo %s" % ArquivoOUT
                raise
            Conteudo = pFile.readlines()
            pFile.close()
            Rodou=False
            for Linhas in Conteudo:
                tmp = Linhas.find("SUCCESSFUL FLEXCOM ANALYSIS")
                if tmp != -1:
                    Rodou=True
                    break
            # fim do loop nas linhas do arquivo
            if not Rodou:
                Indice_MortosFeridos.append(Indice_Lista)
            Indice_Lista+=1
        #fim do loop na lista de arquivos
        del tmp
        Indice_MortosFeridos.reverse()
        for tmp in Indice_MortosFeridos:
            ListaMortosFeridos.append(ListaArquivosOUT.pop(tmp))
        ListaMortosFeridos.reverse()
        return ListaMortosFeridos
    except:
        print "Erro ao tentar criar a lista dos casos que nao rodaram."
        return 0



def CriaListaArquivosOUT(TipoAnalise):
# procura no diretorio por todos os arquivos .out
# de acordo com TipoAnalyise
# TipoAnalyse pode ser "S", "Q" ou "D"
#
# assume o arquivo temporario tmpArquivoNome
    try:
        ListaArquivosOUT = []
        tmpArquivoNome = 'tmp_lixo_0106'
        tmp = '*' + TipoAnalise + '.out'
        os.system('if exist ' + tmp + ' dir /b '+ tmp + ' > ' +  tmpArquivoNome)
        tmpArquivo=open(tmpArquivoNome,'r')
        tmpLista=tmpArquivo.readlines()
        tmpArquivo.close()
        os.system('del ' + tmpArquivoNome)
        del tmp
        for tmp in tmpLista:
            ListaArquivosOUT.append(tmp[0:-1])
        return ListaArquivosOUT
    except:
##        print "Erro ao criar lista de arquivos .OUT"
        return []




##def AtualizaArquivoStatus(NomeArquivoStatus, Linhas):
###imprime as 'linhas' no 'ArquivoStatus'
##    try:
##        try:
##            pArquivoStatus=open(NomeArquivoStatus,'r+')
##        except:
##            print "Erro ao abrir o arquivo de status"
##            raise
##        #vai ate o final do arquivo
##        pArquivoStatus.seek(0,2)
##        #verifica o tipo de argumento passado e escreve as linhas
##        tmp='temp string'
##        if type(Linhas) == type(tmp):
##            pArquivoStatus.write(Linhas)
##            pArquivoStatus.write('\n')
##        else:
##            for lin in Linhas:
##                pArquivoStatus.write(lin[:-4])
##                pArquivoStatus.write('\n')
####            pArquivoStatus.write('\n')
##        pArquivoStatus.close()
##        return 1
##    except:
##        print "Erro ao atualizar arquivo de status."
##        return 0



##def CriaArquivoStatus(NomeArquivoStatus):
###cria o arquivo para imprimir status
##    try:
##        pArquivoStatus=open(NomeArquivoStatus,'w')
##        return 1
##    except:
##            print "Erro ao abrir o arquivo de status"
##            return 0
        



def ListaSubfolders(TopPath):
    #retorna uma lista com todos as subpastas de um diretorio
    tmp = os.walk(TopPath)
    dirs=[]
    for tmp1, tmp2, tmp3 in tmp: dirs.append(tmp1)
    del tmp1, tmp2, tmp3, tmp
    return dirs

ArqStatus = 'CheckOUTsimple.txt'
try:
    CurrDir = os.getcwd()
    SubDirs = ListaSubfolders(CurrDir)
    for sdir in SubDirs:
        os.chdir(sdir)
        print sdir
        # define tipos de analises
        TiposAnalises=["T","S","Q","D"]
##      CriaArquivoStatus(ArqStatus)
        for TipoAnalise in TiposAnalises:
            #cria a lista com os arquivos .OUT e testa
            ListaArquivosOUT = CriaListaArquivosOUT(TipoAnalise)
            if ListaArquivosOUT == []:
                #tstr = 'Nenhum arquivo ' + TipoAnalise + '.OUT encontrado.'
                #print(tstr)
                #AtualizaArquivoStatus(ArqStatus, tstr)
                continue
            # procura pelos casos que nao rodaram e retona lista
            ListaMortos = ProcuraMortosFeridos(ListaArquivosOUT)
            if ListaMortos==[]:
                #tstr = 'Todos os arquivos do tipo ' + TipoAnalise + ' rodaram com sucesso.\n'
                #print (tstr); print
                #AtualizaArquivoStatus(ArqStatus, tstr)
                pass
            else:
##             n = len(ListaMortos)
##             if n==1:
##                 tstr = str(n) + ' arquivo do tipo ' + TipoAnalise + ' apresenta erro:'
##                 print (tstr)
##                 AtualizaArquivoStatus(ArqStatus, tstr)
##             else:
##                 tstr = str(n) + ' arquivos do tipo ' + TipoAnalise + ' apresentam erro:'
##                 print (tstr)
##                 AtualizaArquivoStatus(ArqStatus, tstr)
                #escreve a lista de casos com erro em arquivo de status
                for list in ListaMortos: print list[:-4]
##                AtualizaArquivoStatus(ArqStatus, ListaMortos)
except:
    print "Erro."
## finally:
##    print "Resultados salvos em %s" % ArqStatus
