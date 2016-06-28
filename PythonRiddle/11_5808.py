import Image

im=Image.open('cave.jpg')
for i in range(0,10):
    print im.getpixel((i,0))

w,h=im.size
for i in range(w):
    for j in range(h):
        if (i+j)%2==1:
            im.putpixel((i,j),0)
im.save('cave2.png')
#evil
