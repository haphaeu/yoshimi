from OrcFxAPI import  *
import threading
import Queue

#number of threads
NUMTHREADS = 3

#orcaflex dat files to run
L=[ 'simple1.dat',
    'simple2.dat',
    'simple3.dat',
    'simple4.dat']

def StaticProgHandler(model, prog):
    # Handler passed to the model
    # to give progress report when
    # solving statics
    #
    #if the `if` below is not commented, less output will be given 
    #if not (prog[0:4]=='Full' or prog[0:8]=='Catenary'):
    if model.state != 'Reset':
        thisReport=report()
        thisReport.id= int(model.general.GetData('Comments',0)[-3:])
        print thisReport.id #DEBUG
        thisReport.progress = prog
        myRepPool.put(thisReport)
    
    return False
# ########################################################################
class report:
    pass

class progReport(threading.Thread):
    def setup(self, nt, nc):
        self.nThreads = nt
        self.nCases   = nc
    def run(self):
        nCasesDone=0
        nCases=0
        nCasesOk=0
        ListReports =[''] * (1+self.nThreads)
        ListNames   =[''] * (1+self.nThreads)
        while True:
            rep=myRepPool.get()
            if rep=='stop':
                print "report thread terminou"
                return 0
            if rep=='incrDone': nCasesDone +=1
            if rep=='incrOk':   nCasesOk   +=1                
            if rep!=None:
                #update progress rows
                try:
                    ListNames[rep.id]   = rep.modelName
                except: pass
                ListReports[rep.id] = ListNames[rep.id] + ' - ' + rep.progress
                #and output to screen
                os.system('cls') 
                print "Cases processed: %d out of %d" % (nCasesDone, nCases)
                print "Converged: %d     Unconverged: %d" % (nCasesOk, nCasesDone-nCasesOk)
                for s in ListReports:
                    print s

class MyThread ( threading.Thread ):
    def setID(self, n):
        self.id = n
    def run ( self ):
        thisReport=report()
        m=Model()
        #m.staticsProgressHandler = StaticProgHandler
        #set an ID to the model
        m.general.SetData('Comments',0,m.general.GetData('Comments',0)+'   id%03d' % self.id )
        print m.general.GetData('Comments',0)+'   id%03d' % self.id  #DEBUG
        while True:
            dat=myPool.get()
            if dat=='stop':
                print 'Thread terminou <-'
                return 0
            elif dat!=None:
                thisReport.id=self.id
                thisReport.modelName=dat
                thisReport.progress='Loading data...'
                myRepPool.put(thisReport)
                m.LoadData(dat)
                thisReport.progress='Calculating statics...'
                myRepPool.put(thisReport)
                m.CalculateStatics()
                thisReport.progress='Saving simulation...'
                myRepPool.put(thisReport)
                m.SaveSimulation(dat[0:-3]+'sim')
                thisReport.progress='Done.'
                myRepPool.put(thisReport)
# ###################################################

#create pool managers
myRepPool = Queue.Queue(0)

myReport=progReport()
myReport.setup(NUMTHREADS, 6)
myReport.start()

p=report()
p.id=2
p.progress='fuck off'
myRepPool.put(p)
myRepPool.put('stop')
myReport.join()

print 'End'