import urllib

nothing=12345
i=0
while i<400:
  url='http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='+str(nothing)
  page=urllib.urlopen(url)
  contents=page.read()
  print i, contents
  try:
    nothing=int(contents.split('is')[-1])
  except:
    print "mudou o formato"
    if contents=='Yes. Divide by two and keep going.':
      nothing/=2
    else:
      print "either got the answer or need some more implementing here"
      break
  i+=1
   