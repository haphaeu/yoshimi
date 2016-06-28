#converts an arabic number into its roman
#representation by following the law of
#minimum set of characters
#http://projecteuler.net/about=roman_numerals
def arabic2roman(n):
    if n>9999: return False
    thousands =n/1000
    hundreds  = (n-thousands*1000)/100
    tenths    = (n-thousands*1000-hundreds*100)/10
    units     = n-thousands*1000-hundreds*100-tenths*10
    #start to put together the roman number
    #thousand is easy:
    roman='M'*thousands
    #hundreds, some rules apply for minimum number of characters
    if hundreds <=3:   roman+='C'*hundreds
    elif hundreds ==4: roman+='CD'
    elif hundreds ==5: roman+='D'
    elif hundreds ==6: roman+='DC'
    elif hundreds ==7: roman+='DCC'
    elif hundreds ==8: roman+='DCCC'
    elif hundreds ==9: roman+='CM'
    #tenths, similar rules as for hundreds
    if tenths <=3:   roman+='X'*tenths
    elif tenths ==4: roman+='XL'
    elif tenths ==5: roman+='L'
    elif tenths ==6: roman+='LX'
    elif tenths ==7: roman+='LXX'
    elif tenths ==8: roman+='LXXX'
    elif tenths ==9: roman+='XC'
    #and finally the units
    if units <=3:   roman+='I'*units
    elif units ==4: roman+='IV'
    elif units ==5: roman+='V'
    elif units ==6: roman+='VI'
    elif units ==7: roman+='VII'
    elif units ==8: roman+='VIII'
    elif units ==9: roman+='IX'
    #done!
    return roman

def roman2arabic(roman):
    arabic=0
    #check for subtractions first
    if not roman.find('IV') == -1: 
        arabic+=4
        roman=roman.replace('IV', '')
    if not roman.find('IIX') == -1: 
        arabic+=8
        roman=roman.replace('IIX', '')
    if not roman.find('IX') == -1: 
        arabic+=9
        roman=roman.replace('IX', '')
    if not roman.find('XL') == -1: 
        arabic+=40
        roman=roman.replace('XL', '')
    if not roman.find('XXC') == -1: 
        arabic+=80
        roman=roman.replace('XXC', '')
    if not roman.find('XC') == -1: 
        arabic+=90
        roman=roman.replace('XC', '')
    if not roman.find('CD') == -1: 
        arabic+=400
        roman=roman.replace('CD', '')
    if not roman.find('CCM') == -1: 
        arabic+=800
        roman=roman.replace('CCM', '')
    if not roman.find('CM') == -1: 
        arabic+=900
        roman=roman.replace('CM', '')
    #now no subtractions are left
    #just add numbers
    for c in roman:
        if c=='M': arabic+=1000
        if c=='D': arabic+=500
        if c=='C': arabic+=100
        if c=='L': arabic+=50
        if c=='X': arabic+=10
        if c=='V': arabic+=5
        if c=='I': arabic+=1
    return arabic

#read file with roman numerals
import urllib
url='http://projecteuler.net/project/roman.txt'
page=urllib.urlopen(url)
contents=page.read()
romans=contents.split('\r\n')
del contents,  page,  url

#convert romans to minimum char size
romans2=[arabic2roman(roman2arabic(c)) for c in romans]

#print them just to some spot checks
#and count chars to compare
size_rom1=0
size_rom2=0
for i in range(1000):
    #print "%s\t%s" % (romans[i],  romans2[i])
    size_rom1+=len(romans[i])
    size_rom2+=len(romans2[i])
print "Reduced from %d to %d characters - saved %d characters" % (size_rom1,  size_rom2,  size_rom1-size_rom2)


