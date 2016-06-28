#project euler problem 102
#
# went a bit further and did it in 3D...
#
class point():
    def __init__(self,x,y,z=0):
        self.x=x
        self.y=y
        self.z=z
class vector():
    def __init__(self,p1,p2):
        self.x=p2.x-p1.x
        self.y=p2.y-p1.y
        self.z=p2.z-p1.z
class triangle():
    def __init__(self, a, b, c):
        self.a=a
        self.b=b
        self.c=c
    def contain(self, p):
        self.ab=vector(self.a,self.b)
        self.ba=vector(self.b,self.a)
        self.bc=vector(self.b,self.c)
        self.cb=vector(self.c,self.b)
        self.ca=vector(self.c,self.a)
        self.ac=vector(self.a,self.c)
        self.ap=vector(self.a,p)
        self.bp=vector(self.b,p)
        self.cp=vector(self.c,p)
        if dot(cross(self.ab,self.ap),cross(self.ab,self.ac))<0:
            return False
        if dot(cross(self.bc,self.bp),cross(self.bc,self.ba))<0:
            return False
        if dot(cross(self.ca,self.cp),cross(self.ca,self.cb))<0:
            return False
        return True
def dot(a, b):
    return a.x*b.x+a.y*b.y+a.z*b.z
def cross(a, b):
    return point(a.y*b.z-a.z*b.y,
                 a.z*b.x-a.x*b.z,
                 a.x*b.y-a.y*b.x)

cont=[_.split(',') for _ in open('triangles.txt','r').readlines()]
origin=point(0,0)
ct=0
for _ in cont:
    t=triangle(point(int(_[0]),int(_[1])),
               point(int(_[2]),int(_[3])),
               point(int(_[4]),int(_[5])))
    if t.contain(origin): ct+=1
print ct
# 228
