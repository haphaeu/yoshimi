import threading
import Queue
from random import random

theVar = 0

class MyThread ( threading.Thread ):

    def run ( self ):
        global theVar
        while True:
            client=myPool.get()
            print '- iniciando thread-'
            if client=='stop':
                print 'Thread terminou <-'
                return 0
            elif client!=None:
                for x in xrange(int(random()*1000000)): continue
                theVar = theVar + 1
                print '- Thread rodou -'
# ##        

print '#####################################################'

#number of threads
NUMTHREADS = 3
NUMPROCESSES=20
#create a pool manager
myPool = Queue.Queue(0)

#starts only 2 threads
for x in xrange (NUMTHREADS):
    print '-> Iniciando thread', x
    MyThread().start()

#pass data into thread pool
#and run thread a couple of times
for x in xrange(NUMPROCESSES):
    print '- passando dados para thread -'
    myPool.put('dummy')

#stop the threads
for x in xrange(NUMTHREADS):
    print '- Stopping thread -'
    myPool.put('stop')
