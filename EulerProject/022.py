def alpha(name):
    #note that ord(a)=65
   return sum([ord(c)-64 for c in name]) 

pfile=open("022.txt", 'r')
tmp=pfile.read()
pfile.close()
tmp=tmp.split(",")
names=[n.replace("\"", "") for n in tmp]
names.sort()
score = sum( [ (i+1)*alpha(names[i]) for i in range(len(names))])
print score
