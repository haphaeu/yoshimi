#
# DynUnstable.py
#
# this script goes thru every .SIM file in the
# current folder and check is its state is
# SimulationStoppedUnstable. Results are reported
# to file.
#
# R.Rossi - 14/10/2011
#
from OrcFxAPI import *
import glob

print "Loading OrcaFlex. This might take a few seconds."
m = Model()
# Load a list of SIM files and count them
print "Creating list of SIM files."
ListSimulationFiles = glob.glob('.\*.sim')
NumOfSimFiles = len(ListSimulationFiles)
ListUnstableSims=[]
ResultsFile='CheckOrcFxUnstable.txt'
print NumOfSimFiles, "SIM files found."
print "Starting the loop."
counter=0
for SimulationFile in ListSimulationFiles:
    counter+=1
    m.LoadSimulation(SimulationFile)
    if m.state == ModelState.SimulationStoppedUnstable:
        ListUnstableSims.append(SimulationFile+'\n')
        print "File", counter, "out of", NumOfSimFiles, "- Simulation unstable - File:",SimulationFile
#save results to file        
pFile = open(ResultsFile,'w')
pFile.writelines(ListUnstableSims)
pFile.close()
print "Done. Results saved in file", ResultsFile