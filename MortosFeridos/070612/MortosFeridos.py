import os
import sys

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
        os.system('dir /b '+ tmp + ' > ' +  tmpArquivoNome)
        tmpArquivo=open(tmpArquivoNome,'r')
        tmpLista=tmpArquivo.readlines()
        tmpArquivo.close()
        os.system('del ' + tmpArquivoNome)
        del tmp
        for tmp in tmpLista:
            ListaArquivosOUT.append(tmp[0:-1])
        return ListaArquivosOUT
    except:
        print "Erro ao criar lista de arquivos .OUT"
        return []



def CriaArquivoStatus(NomeArquivoStatus,NomeArquivoDAT):
# salva arquivo com status do programa
# retorna 1 caso sucesso, 0 caso erro
    try:
        try:
            pArquivoStatus=open(NomeArquivoStatus,'w')
            pArquivoDAT=open(NomeArquivoDAT,'r')
        except:
            print "Erro ao ler/abrir arquivo."
            raise
        pArquivoStatus.write("Echo of the control DAT file:\n")
        pArquivoStatus.write("=============================\n\n")
        pArquivoStatus.writelines(pArquivoDAT.readlines())
        pArquivoStatus.write("\nSummary of the corrected cases:\n")
        pArquivoStatus.write("===============================\n\n")
        pArquivoStatus.write("Case ID, Time-step, Tolerance, MinTorque\n")
        pArquivoDAT.close()
        pArquivoStatus.close()
        return 1
    except:
        print "Erro ao criar arquivo de status do programa."
        return 0

def AtualisaArquivoStatus(NomeArquivoStatus, ListaRodaram, TimeStep, Tol, MinTorque):
# atualisa o arquivo de status com os casos que rodaram
# retorna 1 caso sucesso e 0 caso erro
    try:
        try:
            pArquivoStatus=open(NomeArquivoStatus,'r+')
        except:
            print "Erro ao ler arquivo."
            raise
        pArquivoStatus.seek(0,2)
        for item in ListaRodaram:
            tmpString = item + '   ' + TimeStep + '   ' + Tol + '   ' + MinTorque + '\n'
            pArquivoStatus.write(tmpString)
        return 1
    except:
        print "Erro ao atualisar arquivo de status do programa."
        return 0

def FechaArquivoStatus(NomeArquivoStatus, ListaAindaMortos):
#imprime os arquivos que nao rodaram ao final do programa
#e fecha o arquivo de status
    try:
        try:
            pArquivoStatus=open(NomeArquivoStatus,'r+')
        except:
            print "Erro ao abrir o arquivo de status"
            raise
        pArquivoStatus.seek(0,2)
        pArquivoStatus.write("\n\nCases still dead:\n")
        pArquivoStatus.write(    "=================\n\n")
        for item in ListaAindaMortos:
            tmpString = item + '\n'
            pArquivoStatus.write(tmpString)
        return 1
    except:
        print "Erro ao atualizar arquivo de status."
        return 0

def LeArquivoControle(NomeArquivoDAT):
# le o arquivo com os parametros
# exemplo
# *AnalysisType
# S
# *Time-steps
# 0.1 0.05 0.01
# *Tolerances
# 0.03 0.04
# *MinTorque
# 10000    
    try:
        try:
            pArquivoDAT = open(NomeArquivoDAT,'r')
        except:
            print "Erro ao abrir arquivo %s" % NomeArquivoDAT
            raise
        Conteudo=pArquivoDAT.readlines()
        TipoAnalise=TimeSteps=Tolerances=MinTorques=[]
        for Linhas in Conteudo:
            #procura pelo tipo de analise
            tmp = Linhas.find('*AnalysisType')
            if tmp != -1:
                tmpstr=Linhas.split()
                tmpstr=tmpstr.pop()
                if tmpstr=='S' or tmpstr=='Q' or tmpstr=='D':
                    TipoAnalise = tmpstr
                else:
                    print "Tipo de analise invalida. *AnalisysType deve ser S, Q ou D."
                    raise
            #procura pelo time-steps
            tmp = Linhas.find('*Time-steps')
            if tmp != -1:
                tmpstr=Linhas.split()
                del tmpstr[0]
                try:
                    TimeSteps = [float(tmp) for tmp in tmpstr]
                    if min(TimeSteps)<= 0.0 :
                        print "Time-step negativo ou zero."
                        raise
                except:
                    print "Erro ao ler os time-steps. Verifique arquivo de controle"
                    raise
                continue
            #procura pelas tolerancias
            tmp = Linhas.find('*Tolerances')
            if tmp != -1:
                tmpstr=Linhas.split()
                del tmpstr[0]
                try:
                    Tolerances = [float(tmp) for tmp in tmpstr]
                    if min(Tolerances)<= 0.0 :
                        print "Tolerancia negativa ou zero."
                        raise
                except:
                    print "Erro ao ler as tolerancias. Verifique arquivo de controle"
                continue
            #procura pelo minimo torque
            tmp = Linhas.find('*MinTorque')
            if tmp != -1:
                tmpstr=Linhas.split()
                del tmpstr[0]
                try:
                    MinTorques = [float(tmp) for tmp in tmpstr]
                except:
                    print "Erro ao ler os valores minimos de torque. Verifique arquivo de controle"
                continue
        #verifica os dados do arquivo de controle
        if TipoAnalise==0:
            print "Tipo de analise nao consta em %s." % NomeArquivoDAT
            raise
        if TimeSteps==0 and Tolerances==0 and MinTorques==0:
            print "Pelo menos um parametro deve ser alterado em %s: time-step, tolerancia ou torque" % NomeArquivoDAT
            raise
        #retorna os valores de controle
        print "Arquivo de controle com os seguintes parametros:"
        print "Tipo de Analise: %s" % TipoAnalise
        print "Time-steps: ", TimeSteps
        print "Tolerances: ", Tolerances
        print "Minimum Torque Values: ", MinTorques
        return TipoAnalise, TimeSteps, Tolerances, MinTorques
    except:
        print "Erro no arquivo de controle."
        return [],[],[],[]
    
    
    




def AlteraKEY(NomeArquivoKEY, FlagParametro, ValorParametro):
# abre o arquivo KEY e faz as alteracoes com o novo parametro
# FlagParametro
#    1 - TimeStep
#    2 - Tolerances
#    3 - MinTorque
# ValorParametro - valor a ser atribuido
# a funcao retorn 1 se for executada com sucesso
# e 0 se algum erro occoreu
    try:
        #abre o arquivo KEY para leitura e escrita
        try:
            pArquivoKEY = open(NomeArquivoKEY,'r+')
        except:
            print "Erro ao tentar abrir arquivo %s" % NomeArquivoKEY
            raise
        #define a string a procurar de acordo com FlagParametro
        if FlagParametro==1: ProcuraPor='*TIME'
        elif FlagParametro==2: ProcuraPor='*TOLERANCE'
        elif FlagParametro==3: ProcuraPor='*TOLERANCE'
        else:
            print "Erro na funcao AlteraKEY, FlagParametro invalido."
            raise
        #le o arquivo KEY, procura pelo comando desejado e fecha o arquivo
        Conteudo = pArquivoKEY.readlines()
        pArquivoKEY.close()
        NumLinha = 0
        NumLinhaMax=len(Conteudo)
        for Linhas in Conteudo:
            tmpout = Linhas.find(ProcuraPor)
            if tmpout != -1:
                if FlagParametro==1:
                    tmpout2=Conteudo[NumLinha+1].find('FIXED')
                    if tmpout2 == -1:
                        print "Time-step variavel nao suportado. Aguarde a nova versao ;)"
                        raise
                    ValoresTimeStep = Conteudo[NumLinha+2]
                    ValoresTimeStep = ValoresTimeStep.split()
                    ValoresTimeStepNum = [float(f) for f in ValoresTimeStep]
                    ValoresTimeStep = ' ' + ValoresTimeStep[0] + ' ' + ValoresTimeStep[1] + ' ' + str(ValorParametro) + '\n'
                    del Conteudo[NumLinha+2]
                    Conteudo.insert(NumLinha+2, ValoresTimeStep)
                elif FlagParametro==2:
                    ValoresTolerance = Conteudo[NumLinha+1]
                    ValoresTolerance = ValoresTolerance.split()
                    ValoresToleranceNum = [float(f) for f in ValoresTolerance]
                    ValoresTolerance = ' ' + str(ValorParametro) + ' ' + ValoresTolerance[1] + ' ' + ValoresTolerance[2] + '\n'
                    del Conteudo[NumLinha+1]
                    Conteudo.insert(NumLinha+1, ValoresTolerance)
                elif FlagParametro==3:
                    ValoresTolerance = Conteudo[NumLinha+1]
                    ValoresTolerance = ValoresTolerance.split()
                    ValoresToleranceNum = [float(f) for f in ValoresTolerance]
                    ValoresTolerance = ' ' + ValoresTolerance[0] + ' ' + ValoresTolerance[1] + ' ' + str(ValorParametro) + '\n'
                    del Conteudo[NumLinha+1]
                    Conteudo.insert(NumLinha+1, ValoresTolerance)
                else:
                    print "Erro na funcao AlteraKEY: FlagParametro incorreto."
                    raise
                break
            else: NumLinha+=1
        if NumLinha==NumLinhaMax:
            print "Parametro a ser alterado nao encontrado. Verifique arquivo KEY"
            raise
        #salva arquivo KEY com o novo parametro
        try:
            pArquivoKEY = open(NomeArquivoKEY,'w')
            for Linhas in Conteudo: pArquivoKEY.write(Linhas)
        except:
            print "Erro ao tentar abrir arquivo %s para escrita" % NomeArquivoKEY
            raise
        return 1
    except:
        print "Erro na funcao AlteraKEY"
        print sys.exc_info()
        return 0
    

    


def RodaFLEXCOM(ListaMortos):
# funcao que roda o FLEXCOM para os arquivos alterados
# retorna 1 caso sucesso e 0 caso erro
    try:
        for Morto in ListaMortos:
                LinhaComando = 'CALL RUNFLEX ' + Morto[0:-2]
                os.system(LinhaComando)
        return 1
    except:
        print "Erro ao tentar rodar o FLEXCOM"
        return 0
    





def ComparaListas(ListaMortosVelha, ListaMortosNova):
# compara a lista dos casos mortos do loop anterior
# com a do loop atual. retorna uma lista com os
# casos que rodaram no loop atual
#
    ListaRodaram=[]
    for item in ListaMortosVelha:
        if not item in ListaMortosNova:
            ListaRodaram.append(item)
    return ListaRodaram





