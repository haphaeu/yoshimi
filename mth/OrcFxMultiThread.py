from OrcFxAPI import  *
import threading
import Queue

#number of threads
NUMTHREADS = 3

#orcaflex dat files to run
L=[ '15008-GN-PF-ACOS-CIEEM-O026SW-W0000000000-L-0000.dat',
    '15009-GN-PF-ACOS-CISEM-O026SW-W0000000000-L-0000.dat',
    '15010-GN-PF-ACOS-CISSM-O030NW-W0000000000-L-0000.dat',
    '15011-GN-PF-ACOS-CISWM-O030NW-W0000000000-L-0000.dat',
    '15012-GN-PF-ACOS-CIWWM-O030NW-W0000000000-L-0000.dat',
    '15013-GN-PF-ACOS-CINWM-O030NW-W0000000000-L-0000.dat']

def StaticProgHandler(model, prog):
    # Handler passed to the model
    # to give progress report when
    # solving statics
    #
    #if the `if` below is not commented, less output will be given 
    #if not (prog[0:4]=='Full' or prog[0:8]=='Catenary'):
    sys.stdout.write('%s\r' % prog)
    return False
# ########################################################################
class MyThread ( threading.Thread ):
    def run ( self ):
        m=Model()
        m.staticsProgressHandler = StaticProgHandler
        while True:
            dat=myPool.get()
            if dat=='stop':
                print 'Thread terminou <-'
                return 0
            elif dat!=None:
                print '- carregando arquivo ', dat
                m.LoadData(dat)
                print '- rodando arquivo ', dat
                m.CalculateStatics()
                print '- salvando arquivo ', dat
                m.SaveSimulation(dat[0:-3]+'sim')
                print '- fim analise -'
# ##
# ###################################################

#create a pool manager
myPool = Queue.Queue(0)

#start threads
Lth=[]
for x in xrange (NUMTHREADS):
    print '-> Iniciando thread', x
    Lth.append(MyThread())
    Lth[x].start()

#pass data into thread pool
for dat in L:
    print '- passando dados para thread -'
    myPool.put(dat)

#stop the threads
for x in xrange(NUMTHREADS):
    print '- Stopping thread -'
    myPool.put('stop')

#this 'join' command magically
#makes the program waits for all
#threads to finish before exit
for x in xrange (NUMTHREADS):
    print 'Joining threads'
    Lth[x].join()

print 'End'