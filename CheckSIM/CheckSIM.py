from glob import glob
import os

def ListaSubfolders(TopPath):
    #retorna uma lista com todos as subpastas de um diretorio
    tmp = os.walk(TopPath)
    dirs=[]
    for tmp1, tmp2, tmp3 in tmp: dirs.append(tmp1)
    del tmp1, tmp2, tmp3, tmp
    return dirs
# 

def ListaArquivosNoExt(ext):
    #lista todos os arquivos de extensao ext
    #retorna uma lista sem as extensoes
    L=glob(ext)
    L = [ l.split('.')[0] for l in L ]
    return L
#

def ProcuraCasosComErro(Ldat, Lsim):
    #verifica quais SIM files nao estao na
    #lista de DAT files
    Lerror=[]
    for l in Ldat:
        try:
            Lsim.index(l)
        except:
            Lerror.append(l+'\n')
            print "Missing SIM file", l
    return Lerror
#

def SalvaArquivoResultados(Lerror):
    #salva um arquivo texto com
    #casos que nao rodaram
    pFile = open('CheckSIM.txt','w')
    if len(Lerror)==0:
        pFile.write('All cases have run.')
    else:
        pFile.write('Cases which did not run:\n')
        pFile.writelines(Lerror)
    pFile.close()
    return 0
#

# #################################
# Main program starts here
# #################################
CurrDir = os.getcwd()
print 'Listing all subfolders.'
SubDirs = ListaSubfolders(CurrDir)
for sdir in SubDirs:
    # DO NOT consider the base dir!!!
    if not sdir==CurrDir:
        os.chdir(sdir)
        print sdir
        #list with all DATs and SIMs files
        Ldat=ListaArquivosNoExt('*.dat')
        Lsim=ListaArquivosNoExt('*.sim')
        #list storing missing SIM files
        Lerror=ProcuraCasosComErro(Ldat, Lsim)
        #save results to file
        SalvaArquivoResultados(Lerror)

