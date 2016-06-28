import os
import sys

def LeArquivoControle(NomeArquivoDAT):
# le o arquivo com os parametros
# no seguinte formato:
#
# Keyfile1T TopAngle
#
# por exemplo
# 01_P55_A2_45T 7.0
#
# essa funcao eh temporaria - os nomes
# serao passados como argumento - logo
# o tratamento de erro eh pobre
# somente um key file suportado no arquivo controle
#
    try:
        try:
            pArquivoDAT = open(NomeArquivoDAT,'r')
        except:
            print "Erro ao abrir arquivo %s" % NomeArquivoDAT
            raise
        Conteudo=pArquivoDAT.readlines()
        #pega a primeira linha do arquivo!!
        Linha=Conteudo[0]
        Linha=Linha.split()
        KeyFile=Linha[0]
        TopAngle=float(Linha[1])
        #retorna os valores de controle
        print "Arquivo de controle com os seguintes parametros:"
        print "Arquivo KEY: %s" % KeyFile
        print "Top Angle: ", TopAngle
        return KeyFile, TopAngle
    except:
        print "Erro no arquivo de controle."
        return [],[]
    
    
    



def CopiaKeyFile(KeyFile):
#faz uma copia do arquivo KEY 
#essa copia eh usada no resto do programa
    try:
        #abre arquivos
        pArquivoKEY = open(KeyFile+'.key','r')
        pArquTmpKEY = open('TopAngle.key','w')
        #copia o conteudo
        Conteudo=pArquivoKEY.readlines()
        pArquTmpKEY.writelines(Conteudo)
        #fecha arquivos
        pArquivoKEY.close()
        pArquTmpKEY.close()
    except:
        print "Erro na funcao CopiaKeyFile"
        return 0
   


def RodaFLEXCOM(KeyFile):
# funcao que roda o FLEXCOM para o arquivo KEY
# retorna 1 caso sucesso e 0 caso erro
    try:
        LinhaComando = 'CALL RUNFLEX ' + KeyFile
        os.system(LinhaComando)
        return 1
    except:
        print "Erro ao tentar rodar o FLEXCOM"
        return 0    
def StatusTitle(maxIter,nIter,TopAngleRequired,TopAngle_i):
# muda o titulo da janela pra mostrar status
    Titulo='Iter: '+str(nIter)+' of '+str(maxIter)+' - Top Angle: '+str(TopAngle_i)+' of '+str(TopAngleRequired)
    LinhaComando='title '+Titulo
    os.system(LinhaComando)
def LeTopAngle(KeyFile):
#le o top angle no arquivo OUT
    try:
        #altera a extensao do arquivo    
        OutFile=KeyFile +'.OUT'
        #abre arquivp pra leitura
        try:
            pFile=open(OutFile,'r')
        except:
                print "Erro ao abrir arquivo %s" % OutFile
                raise
        Conteudo = pFile.readlines()
        lineCounter=0
        #procura pela strin "NODAL LOADS"
        for Linhas in Conteudo:
            tmp = Linhas.find("NODAL LOADS")
            lineCounter+=1
            if tmp!=-1: break
        #retorna 7 linhas (onde acaba a tabela dos DOFs)
        # pega o conteudo da ultima linha da tabela e separa
        lineCounter-=7
        tmp = Conteudo[lineCounter]
        tmp=tmp.split()
        #salva o valor do top angle
        TopAngle=float(tmp[7])
        return TopAngle
    except:
        print "Erro na funcao LeTopAngle"
        return -1


def ReadWaterDepth(KeyFile):
#abre arquivo KEY e le a lamina dagua
# para o calculo inicial da catenaria
    try:
        try:
            pFile=open(KeyFile+'.KEY','r')
        except:
                print "Erro ao abrir arquivo %s" % KeyFile
                raise
        Conteudo = pFile.readlines()
        lineCounter=0
        #procura pela string "OCEAN"
        for Linhas in Conteudo:
            tmp = Linhas.find("*OCEAN")
            lineCounter+=1
            if tmp!=-1: break
        #le o valor da WD logo na linha abaixo de *OCEAN
        tmp=Conteudo[lineCounter]
        tmp=tmp.split()
        WaterDepth=float(tmp[0])
        return WaterDepth
    except:
        print "Erro na funcao ReadWaterDepth"
        return 0
    
def ReadHorizDist(KeyFile):
#le o DOF2 do no 1 no arquivo key
    try:
        pFile=open(KeyFile+'.key','r')
        Conteudo=pFile.readlines()
        pFile.close()
        lineCounter=0
        for linhas in Conteudo:
            tmp = linhas.find("*NODE")
            lineCounter+=1
            if tmp!=-1: break
        FoundNode1=False
        while not FoundNode1:
            linha=Conteudo[lineCounter]
            values=linha.split()
            try:
                node=int(values[0])
                Check=True
            except:
                Check=False
                lineCounter+=1
            if Check:
                if node==1:
                    FoundNode1=True
                    DOF2=abs(float(values[2]))
                else: lineCounter+=1
        return DOF2
    except:
        print "Erro na funcao ReadHorizDist"
        return 0

def CalcInitCatenary(WaterDepth, TopAngle):
#calculo da distancia horizontal da catenaria
    from math import radians
    from math import cos
    from math import tan
    from math import log
    from math import sqrt
    #calcs top angle with vertical in radians
    alpha = radians(90.0 - TopAngle)
    #calcs (approx.) the minimum bend radius
    MBR=WaterDepth*cos(alpha)/(1.0-cos(alpha))
    #calcs horizontal distance
    x=tan(alpha)
    H=MBR*log(x+sqrt(1.0+x**2))
    return H
def CalcCatenary(VertDist, HorizDist):
#funcao usada temporariamente para teste
#para nao ter que rodar o Flexcom
#a funcao CalcInitcatenary eh resolvida
#numericamente
    #chute tosco inicial
    TopA=45
    #calculo inicial
    H = CalcInitCatenary(VertDist,TopA)
    #H tolerance, numero max de iter
    tol=0.01
    maxIter=1000
    #passo inicial
    dTA=10.
    nIter=0
    while nIter<maxIter:
        if abs(HorizDist-H)<=tol:
            return TopA
        elif H > HorizDist:
            TopA-=dTA
            FlagDiminui=True
        else:
            TopA+=dTA
            FlagDiminui=False
        H = CalcInitCatenary(VertDist,TopA)
        #print "Iter: %i, Target: %.2f, Current: %.2f, Top Angle: %.1f" % (nIter, HorizDist, H, TopA)
        if (H>HorizDist and not FlagDiminui) or (H<HorizDist and FlagDiminui):
            dTA/=2.0
        nIter+=1
    

def AlteraKey(KeyFile,HorizDist):
#altera o DOF2 do no 1 no arquivo key
    try:
        pFile=open(KeyFile+'.key','r')
        Conteudo=pFile.readlines()
        pFile.close()
        lineCounter=0
        for linhas in Conteudo:
            tmp = linhas.find("*NODE")
            lineCounter+=1
            if tmp!=-1: break
        FoundNode1=False
        while not FoundNode1:
            linha=Conteudo[lineCounter]
            values=linha.split()
            try:
                node=int(values[0])
                Check=True
            except:
                Check=False
                lineCounter+=1
            if Check:
                if node==1:
                    FoundNode1=True
                    values='   ' + values[0] + '   ' + values[1] + '   -' + str(HorizDist) + '   ' + values[3] + '\n'
                else: lineCounter+=1
        del Conteudo[lineCounter]
        Conteudo.insert(lineCounter,values)
        pFile=open(KeyFile+'.key','w')
        pFile.writelines(Conteudo)
        pFile.close()
        return 1
    except:
        print "Erro na funcao AlteraKey"
        return 0
def ComentaKey(KeyFile):
#salva a linha original do keyfile com um comentario
    try:
        pFile=open(KeyFile+'.key','r')
        Conteudo=pFile.readlines()
        pFile.close()
        lineCounter=0
        for linhas in Conteudo:
            tmp = linhas.find("*NODE")
            lineCounter+=1
            if tmp!=-1: break
        FoundNode1=False
        while not FoundNode1:
            linha=Conteudo[lineCounter]
            values=linha.split()
            try:
                node=int(values[0])
                Check=True
            except:
                Check=False
                lineCounter+=1
            if Check:
                if node==1: FoundNode1=True
                else: lineCounter+=1
        Conteudo.insert(lineCounter,'C '+linha)
        Conteudo.insert(lineCounter,'C linha original salva pelo programa AdjustTopAngle:\n')
        pFile=open(KeyFile+'.key','w')
        pFile.writelines(Conteudo)
        pFile.close()
        return 1
    except:
        print "Erro na funcao ComentaKey"
        return 0
def VerificaRodou(KeyFile):
# verifica se a analise rodou sem erros
#
# para arquivo em keyFile, procura por uma
# string para ver se a analyse nao rodou
#
#return True se rodou, False se deu pau ou error na funcao
    try:
        Indice_Lista = 0
        tmp=0
        Indice_MortosFeridos = []
        ListaMortosFeridos=[]
        try:
            pFile = open(KeyFile+'.out','r')
        except:
            print "Erro ao ler arquivo %s.out" % KeyFile
            raise
        Conteudo = pFile.readlines()
        Rodou=False
        for Linhas in Conteudo:
            tmp = Linhas.find("SUCCESSFUL FLEXCOM ANALYSIS")
            if tmp != -1:
                Rodou=True
                break
        if Rodou: return True
        else: return False
    except:
        print "Erro ao tentar verificar se a analise rodou com sucesso."
        return False
    
def AdjustTopAngle(KeyFile, TopAngleRequired):
#itera para ajustar o top angle
#
#roda o flexcom e compara
#o top angle resultante com o requerido

#inicia o processo iterativo:
# TAi=top angle corrent
# TAr=top angle requerido
#   H=distancia horizontal(modulo)
#  dH=variacao da distancia H
#
# resumo do processo ietrativo:
#
# se o top angle for maior que o requerido
# a posicao da ancora eh aproximada da
# plataforma de uma distancia dH, e vice-versa.
#
# a cada passo, dH eh corrigido e eh diretamente
# proporcional a diferenca do top angle atual e
# requerido
#
# o valor de dH eh fundamental para uma boa convergencia

    pStat=open(KeyFile+'.taa','w')
    MagicNumber=1.6
    try:
        ###########################################
        #'online' version:
        WD=ReadWaterDepth(KeyFile)
        HD=ReadHorizDist(KeyFile)
        RodaFLEXCOM(KeyFile)
        if not VerificaRodou(KeyFile):
            print "Erro na analise de Flexcom"
            print >> pStat, "Erro na analise de Flexcom"
            raise
        TopAngle_i=LeTopAngle(KeyFile)
        ########################################
        #`offline` version:
        #WD=600.0
        #HD=CalcInitCatenary(WD,TopAngleRequired)
        #TopAngle_i=CalcCatenary(WD,HD)-0.5
        ########################################
        #estimate dH - see calcsheet
        dH = abs(TopAngleRequired-TopAngle_i)*WD*MagicNumber/100.0
        #top angle tolerance and max iter
        maxIter=20
        tol=0.01
        print "Iniciando iteracoes..."
        nIter=0
        while nIter<maxIter:
            #print out status to screen and file
            print "Iter: %i - Target: %.2f, Current: %.2f, Delta H: %.2f, Horizontal Distance: %.3f" % (nIter, TopAngleRequired, TopAngle_i, dH, HD)
            print >> pStat, "Iter: %i - Target: %.2f, Current: %.2f, Delta H: %.2f, Horizontal Distance: %.3f" % (nIter, TopAngleRequired, TopAngle_i, dH, HD)
            StatusTitle(maxIter,nIter,TopAngleRequired,TopAngle_i)
            if abs(TopAngleRequired-TopAngle_i)<=tol:
                print "Top angle tolerance reached."
                print >> pStat, "Top angle tolerance reached."
                pStat.close()
                return 1
            elif TopAngle_i > TopAngleRequired:
                HD-=dH
                FlagDiminui=True
            else:
                HD+=dH
                FlagDiminui=False
            ###############################
            #'online' version:
            AlteraKey(KeyFile,HD)
            RodaFLEXCOM(KeyFile)
            if not VerificaRodou(KeyFile):
                print "Erro na analise de Flexcom"
                print >> pStat, "Erro na analise de Flexcom"
                raise
            TopAngle_ii=LeTopAngle(KeyFile)
            #################################
            #'offline' version:
            #TopAngle_ii=CalcCatenary(WD,HD)
            ##################################
            if nIter==0:
                dH=2*dH*abs((TopAngle_ii-TopAngleRequired)/(TopAngle_ii-TopAngle_i))
            TopAngle_i=TopAngle_ii
            if (TopAngle_i>TopAngleRequired and not FlagDiminui) or (TopAngle_i<TopAngleRequired and FlagDiminui):
                dH=dH/2.0
            nIter+=1
        print >> pStat, "Maximum number of iterations (%i) reached." % maxIter
        pStat.close()
        return 0
    except:
        #fodeu...
        print >> pStat, "Error occured."
        pStat.close()
        return 0





try:
    nArg=len(sys.argv)
    if nArg==3:
        fileName=sys.argv[1]
        if os.path.isfile(fileName+'.key'):
            #caso o usuario entre com algo que nao seja um numero
            #a funcao float() gerara um erro que sera pego
            #pelo try. logo nao eh testado explicitamente
            TopAngleRequired=float(sys.argv[2])
            ComentaKey(fileName)
            AdjustTopAngle(fileName,TopAngleRequired)
        else:
            print "O arquivo %s nao existe." % fileName
            raise
    else:
        print "Numero de argumentos invalido."
        raise
except:
    print "Erro nos argumentos."
    print "A linha de comando deve ser da forma:"
    print ""
    print "    python AdjustTopAngle.py StaticKeyFile TopAngle"
    print ""
    print "por exemplo, para o arquivo P55HM45T.key com um top angle de 17deg:"
    print ""
    print "    python AdjustTopAngle.py P55HM45T 17.0"
    
#ArqControle = 'TopAngle.dat'
#KeyFile, TopAngle=LeArquivoControle(ArqControle)
#CopiaKeyFile(KeyFile)
#AdjustTopAngle('TopAngle',TopAngle)
#offline version
#AdjustTopAngle('TopAngle',8.0)

