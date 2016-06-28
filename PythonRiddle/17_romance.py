import urllib2, cookielib, urllib, bz2, xmlrpclib

auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password('inflate', 'www.pythonchallenge.com', 'huge', 'file')
jar = cookielib.CookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(auth_handler, cookie_handler)
print opener.open('http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing=12345').read()
list(jar)
#cookies here show a hidden message

i=0
message=[]
busynothing=12345
while i<400:
    url='http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing='+str(busynothing)
    contents=opener.open(url).read()
    try:
        busynothing=int(contents.split('is')[-1])
        message.append(list(jar)[0].value)
        print message[-1], contents
    except:
        break

message2=''.join(message)
print message2
message3=urllib.unquote(message2)
print message3
message4=urllib.unquote_plus(message2)
message5=bz2.BZ2Decompressor().decompress(message4)
#'is it the 26th already? call his father and inform him that "the flowers are on their way". he\'ll understand.'
#
# Mozart's father is called Leopold
phonebook = xmlrpclib.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
print phonebook.phone('Leopold')
#555-VIOLIN
list(jar)[0].value = 'the+flowers+are+on+their+way'
print opener.open('http://www.pythonchallenge.com/pc/stuff/violin.php').read()

# BALLOONS !!!
