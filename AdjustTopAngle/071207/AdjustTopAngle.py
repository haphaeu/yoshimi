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
    #########################
    #temp - remove that
    H+=520
    #########################
    return H
                           
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
    
def AdjustTopAngle(KeyFile, TopAngleRequired):
#itera para ajustar o top angle
#
#inicialmente faz uma estimativa da posicao
#da ancora pelo calculo de uma catenaria usando
#a lamina dagua como distancia vertical
#
#roda o flexcom com esse valor aproximado e compara
#o top angle resultante com o requerido

#inicia o processo iterativo:
# TAi=top angle corrent
# TAr=top angle requerido
#   H=distancia horizontal(modulo)
#  dH=variacao da distancia H
#
#01  estima dH (?? 1m? 10m? 1%WD?)
#02  se TAi>TAr
#03     diminui H com passo dH
#04     flag_diminui=True
#05  senao
#06     aumenta H com passo dH
#07     flagdiminui=False
#08  altera KEY
#09  roda Flexcom
#10  le novo TAi
#11  se TAi==TAr: fim
#12  senao
#13     se (TAi>TAr AND flag==aumenta) OR (TAi<TAr AND flag==diminui)
#14     dH=dH/2
#15     va para 02
    try:
        WD=ReadWaterDepth(KeyFile)
        HD=CalcInitCatenary(WD,TopAngleRequired)
        AlteraKey(KeyFile,HD)
        RodaFLEXCOM(KeyFile)
        TopAngle_i=LeTopAngle(KeyFile)
        #estimate dH as 1% of WD- might need further change
        dH = 0.01*WD
        #top angle tolerance
        tol=0.01
        #
        print "Iniciando iteracoes..."
        while True: #dangerous!!!!!
            if abs(TopAngleRequired-TopAngle_i)<=tol:
                print "Top angle tolerance reached."
                return 1
            elif TopAngle_i > TopAngleRequired:
                HD-=dH
                FlagDiminui=True
            else:
                HD+=dH
                FlagDiminui=False
            AlteraKey(KeyFile,HD)
            RodaFLEXCOM(KeyFile)
            TopAngle_i=LeTopAngle(KeyFile)
            print "Target: %f, Current: %f, Horizontal Distance: %f" % (TopAngleRequired, TopAngle_i, HD)
            if (TopAngle_i>TopAngleRequired and not FlagDiminui) or (TopAngle_i<TopAngleRequired and FlagDiminui):
                dH/=2.0
    except:
        #fodeu...
        return 0


ArqControle = 'TopAngle.dat'
KeyFile, TopAngle=LeArquivoControle(ArqControle)
CopiaKeyFile(KeyFile)
AdjustTopAngle('TopAngle',TopAngle)

