import urllib, zipfile, sys


url='http://www.pythonchallenge.com/pc/def/channel.html'
page=urllib.urlopen(url)
pg_contents=page.read()
print pg_contents

url='http://www.pythonchallenge.com/pc/def/channel.zip'

zipfilename = '/home/rafael/Documents/PythonRiddles/test.zp'
urllib.urlretrieve(url,zipfilename)



zipf = zipfile.ZipFile(zipfilename)
listfiles=zipf.filelist
n=len(listfiles)
print [f.orig_filename for f in listfiles]

contents=zipf.read('readme.txt')
print contents

nothing = 90052 #this is in readme.txt

i=0
sortedlist=[]
while i<n:
    nextfile = str(nothing)+'.txt'
    sortedlist.append(nextfile)
    contents=zipf.read(nextfile)
    sys.stdout.write("%s\n" % contents)
    sys.stdout.flush()
    try:
        nothing=int(contents.split('is')[-1])
    except:
        print "\nmudou sintaxe - rever codigo"
        break
    i+=1

s=""
for f in sortedlist:
    s+=zipf.getinfo(f).comment
print s

# HOCKEY (OXYGEN)

