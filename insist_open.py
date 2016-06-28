from OrcFxAPI import Model
from time     import sleep
from os       import system

flag=True
while flag:
    try:
        print "Trying to open OrcaFlex.",
        m = Model()
        print "Ok. Openning program."
        system('"C:\\program files (x86)\\orcina\\orcaflex\\9.5\\orcaflex.exe"')
        flag=False
    except:
        print "No deal. Trying again in 1s."
        sleep(1)
