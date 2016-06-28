import os
from tempfile import TemporaryFile


# Procura pelos arquivos que nao rodaram
# caminho: diretorio da analise
# ListaArquivos: lista de arquivos .out
#
# para arquivo em ListaArquivos, procura por uma
# string para ver se a analyse nao rodou
def ProcuraMortosFeridos(caminho, ListaArquivosOUT):
    Indice_Lista = 0
    tmp=0
    Indice_MortosFeridos = []
    ListaMortosFeridos=[]
    for ArquivoOUT in ListaArquivosOUT:
        pFile = open(ArquivoOUT,'r')
        Conteudo = pFile.readlines()
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
    for tmp in Indice_MortosFeridos:
        ListaMortosFeridos.append(ListaArquivosOUT.pop(tmp))
    return ListaMortosFeridos


# assume o arquivo temporario tmpArquivoNome
def CriaListaArquivosOUT(caminho, TipoAnalise):
    ListaArquivosOUT = []
    tmpArquivoNome = 'tmp_lixo_0106'
    tmp = caminho + '\*' + TipoAnalise + '.out'
    os.system('dir /b '+ tmp + ' > ' +  tmpArquivoNome)
    tmpArquivo=open(tmpArquivoNome,'r')
    tmpLista=tmpArquivo.readlines()
    tmpArquivo.close()
    os.system('del ' + tmpArquivoNome)
    del tmp
    for tmp in tmpLista:
        ListaArquivosOUT.append(tmp[0:-1])

    return ListaArquivosOUT



# chama CriaListaArquivosOUT
# chama ProcuraMortosFeridos
# le DAT e salva time-step, tolerancia, torque
# loop no torque
#     loop na tolerancia
#        faz loop nos time-steps
#            faz loop nos arquivos mortos
#                abre e altera KEY
#            manda rodar todos os mortos
#            chama ProcuraMortosFeridos(..., Mortos)
#            compara lista atual com anterior
#            salva historico dos que funcionaram
# atualisa historico com os que nao rodaram



caminho='c:\\temp'
TipoAnalise='S'
Lista=CriaListaArquivosOUT(caminho, TipoAnalise)
Mortos=ProcuraMortosFeridos(caminho,Lista)
print Mortos
