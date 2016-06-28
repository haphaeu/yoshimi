import MortosFeridos

# chama LeArquivoControle()
# chama CriaListaArquivosOUT()
# chama ProcuraMortosFeridos()
# chama CriaArquivoStatus()
# loop no torque
#     loop na tolerancia
#        loop nos time-steps
#            loop nos arquivos mortos
#                chama AlteraKEY()
#            chama RodaFLEXCOM()
#            chama ProcuraMortosFeridos(..., Mortos)
#            ????chama ComparaListas()????
#            chama AtualisaArquivoStatus()
# chama FechaArquivoStatus()
#

ArqControle = 'controla.dat'
ArqStatus   = 'MortosFeridosLog.txt'

try:
    # le arquivo de controle e testa parametros
    TipoAnalise, TimeSteps, Tolerances, MinTorques = MortosFeridos.LeArquivoControle(ArqControle)
    if TipoAnalise==[] or (TimeSteps==[] and Tolerances==[] and MinTorques==[]):
        print "Erro nos parametros de entrada. Verifique arquivo de controle"
        raise
    #cria a lista com os arquivos .OUT e testa
    ListaArquivosOUT = MortosFeridos.CriaListaArquivosOUT(TipoAnalise)
    if ListaArquivosOUT == []:
        print "Nenhum arquivo %s.OUT encontrado." % TipoAnalise
        raise
    # procura pelos casos que nao rodaram e retona lista
    ListaMortos = MortosFeridos.ProcuraMortosFeridos(ListaArquivosOUT)
    if ListaMortos==[]:
        print "Todos os arquivos do tipo %s rodaram com sucesso." % TipoAnalise
        raise
    #cria arquivo status
    tmp = MortosFeridos.CriaArquivoStatus(ArqStatus,ArqControle)
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
    #inicia o loop do programa
    for torque in MinTorques:
        for tol in Tolerances:
            for ts in TimeSteps:
                for morto in ListaMortos:
                    NomeKEY = morto[0:-3] + 'key'
                    if FlagTimeStep:
                        tmp1 = MortosFeridos.AlteraKEY(NomeKEY, 1, ts)
                    if FlagTol:
                        tmp2 = MortosFeridos.AlteraKEY(NomeKEY, 2, tol)
                    if FlagTorque:
                        tmp3 = MortosFeridos.AlteraKEY(NomeKEY, 3, torque)
                    if tmp1==0 or tmp2==0 or tmp3==0:
                        print "Erro na alteracao do arquivo KEY"
                        raise
                #re-roda os casos alterados
                tmp = MortosFeridos.RodaFLEXCOM(ListaMortos)
                if tmp ==0:
                    print "Erro ao tentar rodar FLEXCOM"
                    raise
                #procura nos casos re-rodados os que ainda nao rodaram
                ListaMortos2 = MortosFeridos.ProcuraMortosFeridos(ListaMortos)
                #testa a lista de saida
                if ListaMortos2==0:
                    raise
                elif ListaMortos2==[]:
                    print "Todos os arquivos rodaram"
                    raise
                #atualisa as listas dos arquivos que rodaram e dos mortos
                #note que a funcao ProcuraMortosFeridos altera o argumento de entrada
                ListaRoradam = ListaMortos
                ListaMortos = ListaMortos2
                del ListaMortos2
                tmp = AtualisaArquivoStatus(ArqStatus, ListaRodaram, ts, tol, torque)
                if tmp==0:
                    print "Erro ao atualisar o arquivo de status"
                    raise
            
                
    
    

