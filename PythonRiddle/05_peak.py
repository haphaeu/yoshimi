import pickle, urllib, sys

emb='http://www.pythonchallenge.com/pc/def/banner.p'

page=urllib.urlopen(emb)
pg_contents=page.read()

unpickled = pickle.loads(pg_contents)

for item in unpickled:
    for jtem in item:
        s=jtem[1]*jtem[0]
        sys.stdout.write("%s" % s)
    sys.stdout.write("\n")
    
