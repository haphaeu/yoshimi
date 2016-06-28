import Image

im=Image.open('mozart.gif')
print im.format, im.mode, im.size
w,h=im.size
#check colors or first line
pos=[]
for j in range(h):
    ct=0
    c= im.getpixel((0,j))
    for i in range(1,w):
        d=im.getpixel((i,j))
        if c==d:
            ct += 1
            if ct ==5:
                #print j, ct, c
                if c==195:
                    pos.append(i-5)
        else:
            c  = d
            ct = 1
    
#from the results one can tell that the pattern is 5 pixels in c=195
#the position of this sequence is saved in pos
#adjust image
im2=Image.new(im.mode, im.size, 0)
for j in range(h):
    for i in range(1,w):
        x=pos[j]+i
        if x>=w: x -= w
        im2.putpixel((i,j), im.getpixel((x,j)))
im2.save('mozart2.gif')

import os
os.system('display mozart2.gif')
