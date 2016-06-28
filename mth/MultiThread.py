
import threading
from random import random

theVar = 0

class MyThread ( threading.Thread ):

    def run ( self ):
        global theVar
        for x in xrange(int(random()*700000)): continue
        theVar = theVar + 1
        print 'Thread', theVar, 'terminou <-'
##        

for x in xrange ( 20 ):
    print '-> Iniciando thread', x
    MyThread().start()
