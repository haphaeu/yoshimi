
pFile = open('Timetrace.csv')
cont = pFile.readlines()

# remove two first lines
cont.pop(0)
cont.pop(0)

pFile2 = open('ShortTimeTrace.csv','w')

for line in cont:
    #tmpline = tmpline.replace('  ',' ')
    #tmpline = tmpline.replace(' ','')
    tmpline = line.split(',')
    nEntries = (len(tmpline)-1)/9
    print nEntries
    key = tmpline[0]
    tmpstr = key + ',   '
    for i in range(nEntries):
        max = tmpline[i*9+4]
        tmpstr = tmpstr + max + ',   '
    tmpstr = tmpstr + '\n'
    pFile2.write(tmpstr)
    del tmpstr
pFile2.close()

    
        
    
