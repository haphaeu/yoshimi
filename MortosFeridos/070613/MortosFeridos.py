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
        pArquivoStatus.write("\n\nSummary of the corrected cases:\n")
        pArquivoStatus.write("===============================\n\n")
        pArquivoStatus.write("Case ID, Time-step, Tolerance, MinTorque\n\n")
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
        if TimeStep==0:
            TimeStep='NA'
        else:
            TimeStep=str(TimeStep)
        if Tol==0:
            Tol='NA'
        else:
            Tol=str(Tol)
        if MinTorque==0:
            MinTorque='NA'
        else:
            MinTorque=str(MinTorque)
        try:
            pArquivoStatus=open(NomeArquivoStatus,'r+')
        except:
            print "Erro ao ler arquivo."
            raise
        pArquivoStatus.seek(0,2)
        for item in ListaRodaram:
            tmpString = item[0:-4] + '   ' + TimeStep + '   ' + Tol + '   ' + MinTorque + '\n'
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
            tmpString = item[0:-4] + '\n'
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
        TipoAnalise=TimeSteps=Tolerances=MinTorques=UserName=[]
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
                    #strTimeSteps = [str(tmp) for tmp in tmpstr]
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
                    #strTolerances = [str(tmp) for tmp in tmpstr]
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
                    #strMinTorques = [str(tmp) for tmp in tmpstr]
                except:
                    print "Erro ao ler os valores minimos de torque. Verifique arquivo de controle"
                continue
            #procura pelo nome do usuario
            tmp = Linhas.find('*UserName')
            if tmp != -1:
                tmpstr=Linhas.split()
                tmpstr=tmpstr.pop()
                UserName = tmpstr
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
        print "User Name: ", UserName
        return TipoAnalise, TimeSteps, Tolerances, MinTorques, UserName
    except:
        print "Erro no arquivo de controle."
        return [],[],[],[],[]
    
    
    




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
    

    


def AlteraMortos(ListaMortos,FlagParametro, valorParametro):
#altera o arquivo .KEY de uma lista de casos, dado o paramentro:
# 1 - timestep
# 2 - tolerance
# 3 - torque
# retorn 1 caso sucesso, 0 caso erro
    try:
        for morto in ListaMortos:
            NomeKEY = morto[0:-3] + 'key'
            tmp = AlteraKEY(NomeKEY, FlagParametro, valorParametro)
            if tmp==0:
                print "Erro na alteracao do arquivo KEY"
                raise
        return 1
    except:
        print "Erro ao alterar arquivos .KEY"
        return 0

def RodaFLEXCOM(ListaMortos):
# funcao que roda o FLEXCOM para os arquivos alterados
# retorna 1 caso sucesso e 0 caso erro
    try:
        for Morto in ListaMortos:
                LinhaComando = 'CALL RUNFLEX ' + Morto[0:-4]
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

def FazTudo(ListaMortos, FlagParametro, ts, tol, torque, NomeArquivoStatus):
    try:
        if FlagParametro==1:
            Parametro = 'time-step'
            ValorParametro=ts
        elif FlagParametro==2:
            Parametro = 'tolerancia'
            ValorParametro=tol
        elif FlagParametro==3:
            Parametro = 'min. torque'
            ValorParametro=torque
        tmp = AlteraMortos(ListaMortos,FlagParametro,ValorParametro)
        if tmp==0:
            print "Erro ao alterar " +  Parametro + " nos arquivos KEY"
            raise
        #re-roda os casos alterados
        tmp = RodaFLEXCOM(ListaMortos)
        if tmp ==0:
            print "Erro ao tentar rodar FLEXCOM"
            raise
        #procura nos casos re-rodados os que ainda nao rodaram
        ListaMortos2 = ProcuraMortosFeridos(ListaMortos)
        #atualisa as listas dos arquivos que rodaram e dos mortos
        #note que a funcao ProcuraMortosFeridos altera o argumento de entrada
        ListaRodaram = ListaMortos
        ListaMortos = ListaMortos2
        del ListaMortos2
        #testa a lista de saida
        if ListaMortos==0:
            raise
        elif ListaMortos==[]:
            print "Todos os arquivos rodaram"
            tmp = AtualisaArquivoStatus(NomeArquivoStatus, ListaRodaram, ts, tol, torque)
            if tmp==0:
                print "Erro ao fechar arquivo de status"
                raise
            raise Fim
        tmp = AtualisaArquivoStatus(NomeArquivoStatus, ListaRodaram, ts, tol, torque)
        if tmp==0:
            print "Erro ao atualisar o arquivo de status"
            raise
        return ListaMortos
    except Fim:
        return 1
    except:
        return 0




def AvisaAcabou(ListaAindaMortos, UserName):
#Manda um aviso para o usuario dizendo que as rodadas ja acabaram
#Diz se todos os aruivos rodaram com sucesso os quantos ainda continuam sem rodar
# retorna 1 caso sucesso e 0 caso erro
    try:
        QuantosNaoRodaram=len(ListaAindaMortos)
        if QuantosNaoRodaram==0:
            LinhaComando = 'NET SEND ' + UserName + ' Todos os casos rodaram com sucesso '
        else:
            LinhaComando = 'NET SEND ' + UserName + ' Nao foi possivel rodar ' + str(QuantosNaoRodaram) + ' casos com os parametros escolhidos'
        os.system(LinhaComando)
        return 1
    except:
        print "Erro ao tentar avisar ao usuario que o programa terminou"
        return 0


ArqControle = 'controla.dat'
ArqStatus   = 'MortosFeridosLog.txt'

try:
    # le arquivo de controle e testa parametros
    TipoAnalise, TimeSteps, Tolerances, MinTorques, UserName = LeArquivoControle(ArqControle)
    if TipoAnalise==[] or (TimeSteps==[] and Tolerances==[] and MinTorques==[]):
        print "Erro nos parametros de entrada. Verifique arquivo de controle"
        raise
    #cria a lista com os arquivos .OUT e testa
    ListaArquivosOUT = CriaListaArquivosOUT(TipoAnalise)
    if ListaArquivosOUT == []:
        print "Nenhum arquivo %s.OUT encontrado." % TipoAnalise
        raise
    # procura pelos casos que nao rodaram e retona lista
    ListaMortos = ProcuraMortosFeridos(ListaArquivosOUT)
    if ListaMortos==[]:
        print "Todos os arquivos do tipo %s rodaram com sucesso." % TipoAnalise
        raise Fim
    #cria arquivo status
    tmp = CriaArquivoStatus(ArqStatus,ArqControle)
    if tmp==0:
        print "Erro ao criar arquivo de status"
        raise

    # ajusta os flags e os parametros a serem chamados no programa
    if MinTorques==[]:
        FlagTorque=False
        MinTorques=[0]
    else:
        FlagTorque=True            
    if Tolerances==[]:
        FlagTol=False
        Tolerances=[0]
    else:
        FlagTol=True
    if TimeSteps==[]:
        FlagTimeStep=False
        TimeSteps=[0]
    else:
        FlagTimeStep=True
    tmp=1
    #inicia o loop do programa
    for torque in MinTorques:
        for tol in Tolerances:
            for ts in TimeSteps:
                if FlagTimeStep:
                    ListaMortos=FazTudo(ListaMortos, 1, ts, tol, torque, ArqStatus)
                    if ListaMortos==0:
                        print "Erro na funcao FazTudo 1."
                        raise
                    elif ListaMortos==1:
                        raise Fim
            if FlagTol:
                ListaMortos=FazTudo(ListaMortos, 2, ts, tol, torque, ArqStatus)
                if ListaMortos==0:
                    print "Erro na funcao FazTudo 2."
                    raise
                elif ListaMortos==1:
                    raise Fim
        if FlagTorque:
            ListaMortos=FazTudo(ListaMortos,3,ts, tol, torque, ArqStatus)
            if ListaMortos==0:
                print "Erro na funcao FazTudo 3."
                raise
            elif ListaMortos==1:
                raise Fim
    #fim dos loops
    #atualisa e fecha arquivo de status
    tmp = FechaArquivoStatus(ArqStatus, ListaMortos)
    if tmp==0:
        print "Erro ao fechar arquivo de status"
        raise
except Fim:
    print "Deu sorte!"
except:
    print "Melhor sorte na proxima vez ;)"
finally:
    if UserName!=[]:
        AvisaAcabou(ListaMortos,UserName)
    print "Game over."
        


