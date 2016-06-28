import os
import sys

def CriaListaArquivos(strTopPath):
    #dado um diretorio, retorna uma lista com
    #os nomes de todos os arquivos em todos os
    # subdiretorios. a lista eh completa incluindo
    # o path.
    try:
        if not os.path.exists(strTopPath):
            raise
        ListaArquivos=[]
        strNomeArquivo = 'tmp_lixo_7395'
        os.chdir(strTopPath)
        os.system('dir /b /s > ' + strNomeArquivo )
        pArquivo = open(strNomeArquivo,'r')
        ListaArquivos=pArquivo.readlines()
        pArquivo.close()
        os.system('del ' + strNomeArquivo)
        return ListaArquivos
    except:
        return -1

def PegaNomesGrandes(ListaArquivos, iMaxLength):
    #dada uma lista de arquivos, retorna uma sublista
    #com os arquivos cujos nome+caminho sao maiores
    #que iMaxLength
    ListaArquivosGrandes=[]
    for strFile in ListaArquivos:
        if len(strFile)>iMaxLength: ListaArquivosGrandes.append(strFile)
    return ListaArquivosGrandes

def SalvaListaArquivosGrandes(ListaArquivos,strPath):
    #salva um arquivos com os nomes dos arquivos grandes
    try:
        if ListaArquivos==[]:
            ListaArquivos=[]
            ListaArquivos.append("No filename too big.")
        if not os.path.exists(strPath):
            raise
        strNomeArquivo="List_of_filenames_too_big.txt"
        os.chdir(strPath)
        pArquivo=open(strNomeArquivo,'w')
        pArquivo.writelines(ListaArquivos)
        pArquivo.close()
        return 0
    except:
        return -1

#strPath="Z:\\Proj\\4100 - S7 Petrobras Guara and Tupi NE DC FEED"
strPath = sys.argv[1]
print "Criando lista com todos os arquivos. Isso pode demorar."
Lista=CriaListaArquivos(strPath)
print "Verificando tamanho dos nomes dos arquivos."
iLimitingFilenameLength=256
ListaGrandes=PegaNomesGrandes(Lista,iLimitingFilenameLength)
print "Salvando resultados."
iRetVal = SalvaListaArquivosGrandes(ListaGrandes, strPath)

iMaxLen=0
for strFile in Lista:
    iLen = len(strFile)
    if iLen>iMaxLen: iMaxLen=iLen






