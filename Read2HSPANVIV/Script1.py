def GetKeypointDamages(ArquivoResultados):
#
    try:
        try:
            pFile = open(ArquivoResultados,'r')
        except:
            print "Erro ao ler arquivo %s" % ArquivoResultados
            raise
        Conteudo = pFile.readlines()
        pFile.close()
        FlagVIV_CF=False
        FlagVIV_IL=False
        for Linhas in Conteudo:
            tmp = Linhas.find("Crossflow Screen Test Result: Fatigue Analysis Needed")
            if tmp != -1:
                FlagVIV_CF=True
            tmp = Linhas.find("Inline Screen Test Result: Fatigue Analysis Needed")
            if tmp != -1:
                FlagVIV_IL=True
                break
        # fim do loop nas linhas crossflow do arquivo

        if not FlagVIV_CF and not FlagVIV_IL:
            return [], [], []
        else:
            CrossflowStart=0        
            if FlagVIV_CF:
                linnum=0
                for Linhas in Conteudo:
                    tmp = Linhas.find("----CROSSFLOW VIV DAMAGE ASSESSMENT----")
                    if tmp!=-1:
                        CrossflowStart=linnum+2
                        break
                    linnum+=1

            InlineStart=0
            if FlagVIV_IL:
                linnum=0
                for Linhas in Conteudo:
                    tmp = Linhas.find("----INLINE VIV DAMAGE ASSESSMENT----")
                    if tmp!=-1:
                        InlineStart=linnum+2
                        break
                    linnum+=1
            del tmp

            Flagkp=True
            linCF=CrossflowStart
            linIL=InlineStart
            SCF=[]
            DamCF=[]
            DamIL=[]
            while Flagkp:
                if FlagVIV_CF:
                    linhaCF=Conteudo[linCF]
                    tmp=linhaCF.split()
                    try:
                        test=int(tmp[0])
                    except:
                        break
                    tmp.pop()
                    DamCF.append(float(tmp.pop()))
                    SCF.append(float(tmp.pop()))
                    del tmp[:]
                    linCF+=1
                if FlagVIV_IL:
                    linhaIL=Conteudo[linIL]
                    tmp = linhaIL.split()
                    try:
                        test=int(tmp[0])
                    except:
                        break
                    tmp.pop()
                    DamIL.append(float(tmp.pop()))
                    if not FlagVIV_CF: SCF.append(float(tmp.pop()))
                    del tmp [:]
                    linIL+=1
            return SCF, DamCF, DamIL
    except:
        print "Erro ao tentar pegar os resultados."
        return 0


MyFileName1='VIV Results (IPC).txt'
MyFileName2='VIV Results (OPC).txt'

[SCF1, IPCDamCF, IPCDamIL]=GetKeypointDamages(MyFileName1)
[SCF2, OPCDamCF, OPCDamIL]=GetKeypointDamages(MyFileName2)

NoVIV='No VIV'

#check size of outputs
maxLen=max(len(SCF1),len(SCF2),len(IPCDamCF),len(IPCDamIL),len(OPCDamCF),len(OPCDamIL))

sumDamageFile = 'sumDamage.txt'
sumLifeFile   = 'sumLife.txt'

if maxLen==0:
    pFileDam=open(sumDamageFile,'w')
    pFileLif=open(sumLifeFile,'w')
    print >> pFileDam, "No VIV Occurs"
    print >> pFileLif, "No VIV Occurs"
    pFileDam.close()
    pFileLif.close()
else:
    KP=range(1,maxLen+1)
    if len(SCF1)==maxLen:
        SCF=SCF1
    elif len(SCF2)==maxLen:
        SCF=SCF2
    if len(IPCDamCF) < maxLen:
        for i in KP: IPCDamCF.append(NoVIV)
    if len(IPCDamIL) < maxLen:
        for i in KP: IPCDamIL.append(NoVIV)
    if len(OPCDamCF) < maxLen:
        for i in KP: OPCDamCF.append(NoVIV)
    if len(OPCDamIL) < maxLen:
        for i in KP: OPCDamIL.append(NoVIV)

    pFileDam=open(sumDamageFile,'w')
    pFileLif=open(sumLifeFile,'w')

    print >> pFileDam, ""
    print >> pFileDam, "VIV FATIGUE DAMAGE"
    print >> pFileDam, "******************"
    print >> pFileDam, ""
    print >> pFileDam, "\t\tInplane\tInplane\tOutplane\tOutplane"
    print >> pFileDam, "\t\tCurrent\tCurrent\tCurrent\tCurrent"
    print >> pFileDam, "\t\tCrossflow\tInline\tCrossflow\tInline"
    print >> pFileDam, "Keypoint\tSCF\tVIV\tVIV\tVIV\tVIV"
    print >> pFileDam, "-\t[-]\t[1/year]\t[1/year]\t[1/year]\t[1/year]"
    for kp in KP:
        print >> pFileDam, "%i\t%s\t%s\t%s\t%s\t%s" % (KP[kp-1], str(SCF[kp-1]), str(IPCDamCF[kp-1]), str(IPCDamIL[kp-1]), str(OPCDamCF[kp-1]), str(OPCDamIL[kp-1]))
    print >> pFileDam, ""
    print >> pFileDam, "\tMax. Damage:\t%s\t%s\t%s\t%s" % (str(max(IPCDamCF)), str(max(IPCDamIL)), str(max(OPCDamCF)), str(max(OPCDamIL)))
    print >> pFileDam, "\tat keypoint:\t%i\t%i\t%i\t%i" % (IPCDamCF.index(max(IPCDamCF))+1, IPCDamIL.index(max(IPCDamIL))+1, OPCDamCF.index(max(OPCDamCF))+1, OPCDamIL.index(max(OPCDamIL))+1)
    print >> pFileDam, ""

        
    print >> pFileLif, ""
    print >> pFileLif, "VIV FATIGUE LIFE"
    print >> pFileLif, "****************"
    print >> pFileLif, ""
    print >> pFileLif, "\t\tInplane\tInplane\tOutplane\tOutplane"
    print >> pFileLif, "\t\tCurrent\tCurrent\tCurrent\tCurrent"
    print >> pFileLif, "\t\tCrossflow\tInline\tCrossflow\tInline"
    print >> pFileLif, "Keypoint\tSCF\tVIV\tVIV\tVIV\tVIV"
    print >> pFileLif, "-\t[-]\t[year]\t[year]\t[year]\t[year]"
    for kp in KP:
        if IPCDamCF[kp-1]==NoVIV:
            kpIPCCF=NoVIV
        else:
            kpIPCCF=1/IPCDamCF[kp-1]
        if IPCDamIL[kp-1]==NoVIV:
            kpIPCIL=NoVIV
        else:
            kpIPCIL=1/IPCDamIL[kp-1]
        if OPCDamCF[kp-1]==NoVIV:
            kpOPCCF=NoVIV
        else:
            kpOPCCF=1/OPCDamCF[kp-1]
        if OPCDamIL[kp-1]==NoVIV:
            kpOPCIL=NoVIV
        else:
            kpOPCIL=1/OPCDamIL[kp-1]
        
        print >> pFileLif, "%i\t%s\t%s\t%s\t%s\t%s" % (KP[kp-1], str(SCF[kp-1]), kpIPCCF, kpIPCIL, kpOPCCF, kpOPCIL)
    print >> pFileLif, ""

    if max(IPCDamCF)==NoVIV:
        IPCMinLifeCF= NoVIV
    else:
        IPCMinLifeCF=str(1/max(IPCDamCF))

    if max(IPCDamIL)==NoVIV:
        IPCMinLifeIL= NoVIV
    else:
        IPCMinLifeIL=str(1/max(IPCDamIL))
        
    if max(OPCDamCF)==NoVIV:
        OPCMinLifeCF= NoVIV
    else:
        OPCMinLifeCF=str(1/max(OPCDamCF))

    if max(OPCDamIL)==NoVIV:
        OPCMinLifeIL= NoVIV
    else:
        OPCMinLifeIL=str(1/max(OPCDamIL))

    print >> pFileLif, "\tMin. Life:\t%s\t%s\t%s\t%s" % (IPCMinLifeCF, IPCMinLifeIL, OPCMinLifeCF, OPCMinLifeIL)
    print >> pFileLif, "\tat keypoint:\t%i\t%i\t%i\t%i" % (IPCDamCF.index(max(IPCDamCF))+1, IPCDamIL.index(max(IPCDamIL))+1, OPCDamCF.index(max(OPCDamCF))+1, OPCDamIL.index(max(OPCDamIL))+1)
    print >> pFileLif, ""

    pFileDam.close()
    pFileLif.close()
