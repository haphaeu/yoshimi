
#exemplo de utilizacao da biblioteca ystockquote



import ystockquote

print "Google share price: " + ystockquote.get_price('GOOG')
print "OGX share price: " + ystockquote.get_price('OGXP3.SA')
print "Petrobras share price: " + ystockquote.get_price('PETR4.SA')
print
print "Petrobras details"
print ystockquote.get_all('PETR4.SA')