import Image, sys

im=Image.open('wire.png')
print im.format, im.mode, im.size
im2=Image.new(im.mode,(100,100),0)

#put first line
for i in range(0,100):
    im2.putpixel((i,0),im.getpixel((i,0)))
#now fill the spiral
dirs=[(0,1),(-1,0),(0,-1),(1,0)]
x=99
y=0
z=100
for i in range(99):
    for k in range(2):
        count = k + 2*i
        d=dirs[count % 4]
        for j in range(100-i-1):
            x += d[0]
            y += d[1]
            #print x,y,z
            im2.putpixel((x,y),im.getpixel((z,0)))
            z += 1
im2.save('wire2.png')
#image is a cat - cat.html -> name is uzi - youll here from him later
