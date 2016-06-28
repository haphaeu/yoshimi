import Image

pfile=open('evil2.gfx')
contents=pfile.read()
pfile.close()
#check file header
#contents[0:60]
# '\xff\x89G\x89\xff\xd8PIP\xd8\xffNFN\xff\xe0G8G\xe0\x00 ...
#    |   | |  |   |
#    |   | |  |   +jpg
#    |   | |  +png
#    |   | +gif  
#    |   +png
#    +jpg
#check is header are ok
##>>> contents[0:60:5]
##'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01'
##>>> contents[1:60:5]
##'\x89PNG\r\n\x1a\n\x00\x00\x00\r'
##>>> contents[2:60:5]
##'GIF87a@\x01\xf0\x00\xe7\x00'
##>>> contents[3:60:5]
##'\x89PNG\r\n\x1a\n\x00\x00\x00\r'
##>>> contents[4:60:5]
##'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01'
#ok!
types=['.jpg','.png','.gif','.png','.jpg']
gfx=[]
gfx.append(contents[0::5])
gfx.append(contents[1::5])
gfx.append(contents[2::5])
gfx.append(contents[3::5])
gfx.append(contents[4::5])
for i in range(0,5):
    pfile=open('gfx'+str(i)+types[i],'wb')
    pfile.write(gfx[i])
    pfile.close
    print "saved", types[i]
#disproportional





