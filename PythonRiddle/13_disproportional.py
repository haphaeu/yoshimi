import xmlrpclib
phonebook = xmlrpclib.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
print phonebook.system.listMethods()

#riddle 12 dizia algo sobre um Bert.
#usando o methodo phone
print phonebook.phone('Bert')
