from OrcFxAPI import  *
import threading
import Queue

#number of threads
NUMTHREADS = 2

#orcaflex dat files to run

L=[ 'simple1.dat',
    'simple2.dat',
    'simple3.dat',
    'simple4.dat']
"""
L=[ '15008-GN-PF-ACOS-CIEEM-O026SW-W0000000000-L-0000.dat',
'15009-GN-PF-ACOS-CISEM-O026SW-W0000000000-L-0000.dat',
'15010-GN-PF-ACOS-CISSM-O030NW-W0000000000-L-0000.dat',
'15011-GN-PF-ACOS-CISWM-O030NW-W0000000000-L-0000.dat',
'15012-GN-PF-ACOS-CIWWM-O030NW-W0000000000-L-0000.dat',
'15013-GN-PF-ACOS-CINWM-O030NW-W0000000000-L-0000.dat',
'15014-GN-PF-ACOS-CIEEM-O026SW-W0000000000-L-0000.dat',
'15015-GN-PF-ACOS-CISEM-O026SW-W0000000000-L-0000.dat',
'15016-GN-PF-ACOS-CISSM-O030NW-W0000000000-L-0000.dat',
'15017-GN-PF-ACOS-CISWM-O030NW-W0000000000-L-0000.dat',
'15018-GN-PF-ACOS-CIWWM-O030NW-W0000000000-L-0000.dat',
'15019-GN-PF-ACOS-CINWM-O030NW-W0000000000-L-0000.dat',
'15020-GN-PF-ACOS-CIEEM-O026SW-W0000000000-L-0000.dat',
'15021-GN-PF-ACOS-CISEM-O026SW-W0000000000-L-0000.dat',
'15022-GN-PF-ACOS-CISSM-O030NW-W0000000000-L-0000.dat',
'15023-GN-PF-ACOS-CISWM-O030NW-W0000000000-L-0000.dat',
'15024-GN-PF-ACOS-CIWWM-O030NW-W0000000000-L-0000.dat',
'15025-GN-PF-ACOS-CINWM-O030NW-W0000000000-L-0000.dat',
'15026-GN-PF-ACOS-CIEEM-O026SW-W0000000000-L-0000.dat',
'15027-GN-PF-ACOS-CISEM-O026SW-W0000000000-L-0000.dat',
'15028-GN-PF-ACOS-CISSM-O030NW-W0000000000-L-0000.dat',
'15029-GN-PF-ACOS-CISWM-O030NW-W0000000000-L-0000.dat',
'15030-GN-PF-ACOS-CIWWM-O030NW-W0000000000-L-0000.dat',
'15031-GN-PF-ACOS-CINWM-O030NW-W0000000000-L-0000.dat',
'15032-GN-PF-ACOS-CIEEM-O026SW-W0000000000-L-0000.dat',
'15033-GN-PF-ACOS-CISEM-O026SW-W0000000000-L-0000.dat',
'15034-GN-PF-ACOS-CISSM-O030NW-W0000000000-L-0000.dat',
'15035-GN-PF-ACOS-CISWM-O030NW-W0000000000-L-0000.dat',
'15036-GN-PF-ACOS-CIWWM-O030NW-W0000000000-L-0000.dat',
'15037-GN-PF-ACOS-CINWM-O030NW-W0000000000-L-0000.dat']
"""
def StaticProgHandler(model, prog):
    # Handler passed to the model
    # to give progress report when
    # solving statics
    #
    #if the `if` below is not commented, less output will be given 
    if not (prog[0:4]=='Full' or prog[0:8]=='Catenary'):
        thisReport=report()
        thisReport.id= int(model.general.GetData('Comments',0)[-3:])
        thisReport.progress = prog
        myRepPool.put(thisReport)
    
    return False
# ########################################################################
class report:
    pass

class progReport(threading.Thread):
    nCases=0
    def setup(self, nt, nc):
        self.nThreads = nt
        self.nCases   = nc
    def run(self):
        self.nCasesDone=0
        self.nCasesOk=0
        self.ListReports =[''] * (1+self.nThreads)
        self.ListNames   =[''] * (1+self.nThreads)
        while True:
            rep=myRepPool.get()
            if rep=='stop':
                #print "report thread terminou"
                return 0
            elif rep=='incrDone': self.nCasesDone +=1
            elif rep=='incrOk':   self.nCasesOk   +=1                
            elif rep!=None:
                #update progress rows
                try:
                    self.ListNames[rep.id]   = rep.modelName
                except: pass
                self.ListReports[rep.id] = self.ListNames[rep.id] + ' - ' + rep.progress
                #and output to screen
                os.system('cls') 
                print "Cases processed: %d out of %d" % (self.nCasesDone, self.nCases)
                print "Converged: %d     Unconverged: %d" % (self.nCasesOk, self.nCasesDone-self.nCasesOk)
                for s in self.ListReports:
                    if s!=' - ':
                        print s

class MyThread ( threading.Thread ):
    def setID(self, n):
        self.id = n
    def run ( self ):
        thisReport=report()
        thisReport.id=self.id
        thisReport.modelName='Thread %d' % self.id
        thisReport.progress='Loading OrcaFlex...'
        myRepPool.put(thisReport)
        m=Model()
        m.staticsProgressHandler = StaticProgHandler        
        while True:
            dat=myPool.get()
            if dat=='stop':
                thisReport.modelName=''
                thisReport.progress=''
                myRepPool.put(thisReport)
                return 0
            elif dat!=None:
                thisReport.id=self.id
                thisReport.modelName=dat
                thisReport.progress='Loading data...'
                myRepPool.put(thisReport)
                m.LoadData(dat)
                m.general.SetData('Comments',0,m.general.GetData('Comments',0)+'   id%03d' % self.id )
                thisReport.progress='Calculating statics...'
                myRepPool.put(thisReport)
                try:
                    m.CalculateStatics()
                    myRepPool.put('incrOk')
                except:
                    pass
                finally:
                    myRepPool.put('incrDone')
                thisReport.progress='Saving simulation...'
                myRepPool.put(thisReport)
                m.SaveSimulation(dat[0:-3]+'sim')
                thisReport.progress='Done.'
                myRepPool.put(thisReport)
# ###################################################

#create pool managers
myPool    = Queue.Queue(0)
myRepPool = Queue.Queue(0)

#start threads
print 'Starting simulations.'
Lth=[]
for x in xrange (NUMTHREADS):
    Lth.append(MyThread())
    Lth[x].setID(x)
    Lth[x].start()

myReport=progReport()
myReport.setup(NUMTHREADS, len(L))
myReport.start()

#pass data into thread pool
for dat in L:
    #print '- passando dados para thread -'
    myPool.put(dat)

#stop the threads
for x in xrange(NUMTHREADS):
    #print '- Stopping thread -'
    myPool.put('stop')

#this 'join' command magically
#makes the program waits for all
#threads to finish before exit
for x in xrange (NUMTHREADS):
    #print 'Joining threads'
    Lth[x].join()

myRepPool.put('stop')
myReport.join()

#print 'End'