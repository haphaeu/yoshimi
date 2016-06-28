
pFile = open('Timetrace.csv')
cont = pFile.readlines()

# remove two first lines
cont.pop(0)
cont.pop(0)

pFile2 = open('ShortTimeTrace.csv','w')

for line in cont:
    #tmpline = line.replace(',',' ')
    #tmpline = tmpline.replace('  ',' ')
    tmpline = line.split(',')
    nEntries = (len(tmpline)-1)/9
    print nEntries
    key = tmpline[0]
    tmpstr = key + ',   '
    for i in range(nEntries):
        max = tmpline[i*9+4]
        min = tmpline[i*9+6]
        tmpstr = tmpstr + max + ',   ' + min + ',   '
    tmpstr = tmpstr + '\n'
    pFile2.write(tmpstr)
    del tmpstr
pFile2.close()

    
        
    
