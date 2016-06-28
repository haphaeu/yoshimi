#simple use of the lib ystockquote
#just call in DOS with share symbol as argument
#the price will be printed out
import sys
symbol = sys.argv[1]
from ystockquote import get_price
print get_price(symbol)


