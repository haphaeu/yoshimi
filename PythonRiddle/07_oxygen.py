import urllib, Image

url='http://www.pythonchallenge.com/pc/def/oxygen.html'
page=urllib.urlopen(url)
contents=page.read()
print contents

url='http://www.pythonchallenge.com/pc/def/oxygen.png'
pngfile='/home/rafael/Documents/PythonRiddles/oxygen.png'
urllib.urlretrieve(url,pngfile)

im=Image.open(pngfile)
print pngfile, im.format, im.size, im.mode
#limiting grey zone
y=0
while True:
    p=im.getpixel((0,y))
    if p[0]==p[1]==p[2]:
        break
    y+=1
x=0
while True:
    p=im.getpixel((x,y))
    if not p[0]==p[1]==p[2]:
        break
    x+=1

#size of boxes got by hand
s=7
message=''
for i in range(0,x,7):
    c=chr(im.getpixel((i,y))[0]) 
    message+=c
print message
#output is
# smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]
chars=[105, 110, 116, 101, 103, 114, 105, 116, 121]
message2=''
for i in chars:
    message2+=chr(i)
print message2
#integrity

    
