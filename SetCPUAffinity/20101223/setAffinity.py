import os
from time import sleep

#
# setAffinity.py
# ==============
#
# Version    Author  Date         Description
# 1.0.0      RR      20/12/2010   First issue
#
# set processor affinity for a selected service.
# this is done using a batch file and the program
# Process.exe:
#Command Line Process Viewer/Killer/Suspender for Windows NT/2000/XP V2.03
#Copyright(C) 2002-2003 Craig.Peacock@beyondlogic.org
#
# Use:
# run the python script
# a batch file should be created in the same folder
# just run this batch and keep it running
# the python script will update the batch file
# on the run and set processor priority for the processes


def WriteID2file(processName, fileIDs):
# roda process.exe e busca o ID 
# de processos
    try:
        LinhaComando = 'process | find ' + processName + ' > '+ fileIDs
        os.system(LinhaComando)
        return 1
    except:
        print "Error in function GetIDs"
        return 0

def ReadIDfile(fileIDs):
# le arquivo criado pela fincao WriteID2file
# no seguinte formato:
#      processname1   processID1    etc...
#      processname2   processID2    etc...
#      etc...
# 
# e retorna uma lista com os IDs
#
    try:
        try:
            pArquivo = open(fileIDs,'r')
        except:
            print "Erro ao abrir arquivo %s" % fileIDs
            raise
        Conteudo=pArquivo.readlines()
        pArquivo.close()
        listID=[]
        for linha in Conteudo:
            tmp=linha.split()
            listID.append(tmp[1])
        return listID
    except:
        print "Error in function ReadIDfile"
        return []


def CreateBAT(listIDs,nomeBAT):
# create a batch file to run process -a
#
# !!! -> adjust number of IDs to exactly 8
# if more processes are running, the
# latest are disconsidered.
#
    try:
        try:
            pArquivoBAT=open(nomeBAT,'w')
        except:
            print "Erro ao ler/abrir arquivo."
            raise
        pArquivoBAT.write(":START\n")
        #this fills exactly the number of processes
        #but as this is applied to a running batch,
        #might give an error
        #for id in listIDs:
        #    linha='   @process -a ' + id + ' ' + CPUmask + '\n'
        #    pArquivoBAT.write(linha)
        #hence, exactly 8 processes are handled:
        for i in range(0,8):
            try:
                linha='   @process -a ' + listIDs[i] + ' ' + str(int(10**(7-i))) + ' > p\n'
            except:
                linha='   @REM dummy line ignore it\n'
            pArquivoBAT.write(linha)
        #done
        pArquivoBAT.write("@GOTO START")
        pArquivoBAT.close()
        return 1
    except:
        print "Error in function CreateBAT."
        return 0

def SetAffinity(listIDs, CPUmask):
# set up CPU affinity 
# for processes with IDs in listIDs
#!!!!
#not actually being used
#the number of windows raised is too much
#and costs too muhc processor
#!!!!
    try:
        for id in listIDs:
            LinhaComando = 'process -a ' + id + ' ' + CPUmask
            os.system(LinhaComando)
        return 1
    except:
        print "Error in function SetAffinity"
        return 0

#for debbuging...
path='C:\\Users\\public.2HBRRIO1\\Desktop\\SetAffinity\\Tabajara'
os.chdir(path)
processo='"flex3.exe"'
fileIDs='processIDs.txt'
WriteID2file(processo,fileIDs)
IDs=ReadIDfile(fileIDs)
CreateBAT(IDs, 'setAf.bat')

j=0
while j<1000:
    j+=1
    WriteID2file(processo,fileIDs)
    IDs=ReadIDfile(fileIDs)
    CreateBAT(IDs, 'setAf.bat')
    sleep(10)

