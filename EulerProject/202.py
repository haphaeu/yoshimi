'''
Project Euler - Problem 202

- see apreadsheet for some details

- this method properly calculates the reflections but doesn not have
enough accuracy to solve the problem

'''
from math import pi, tan, cos, sin, radians

VERB=False

a_blue  = 0.0
b_blue  = sin(radians(60))
a_black = -tan(radians(60))
b_black = 0
a_red   = tan(radians(60))
b_red   = 0

eps=1e-3
Thetas=[65+d/10. for d in range(2,300,2)]
for i,theta in enumerate(Thetas):
    x=y=0.0
    if VERB: print "i\tx\ty\tQ\ta\tb\tx_blue\ty_blue\tx_black\ty_black\tx_red\ty_red\thit"
    while True:
        a=tan(radians(theta))
        b=y-a*x
        x_blue= (b_blue-b)/(a-a_blue)
        y_blue= a_blue*x_blue+b_blue
        x_black= (b_black-b)/(a-a_black)
        y_black= a_black*x_black+b_black
        x_red= (b_red-b)/(a-a_red)
        y_red= a_red*x_red+b_red
        if i==0:
            hit='blue'
        else:
            if hit=='blue':
                if y_black>0 and x_black>-0.5: hit='black'
                else:                          hit='red'
            elif hit=='black':
                if abs(x_blue)>0.5: hit='red'  #maybe this condition is incomplete
                else:               hit='blue'
            elif hit=='red':
                if abs(x_blue)>0.5: hit='black'
                else:               hit='blue'
            else:
                print "Error."
                break   
        if VERB: print "%d\t%+.2f\t%+.2f\t%d\t" % (i,x,y, theta),
        if VERB: print "%+.2f\t%+.2f\t%+.2f\t%+.2f\t" % (a,b,x_blue,y_blue),
        if VERB: print "%+.2f\t%+.2f\t%+.2f\t%+.2f\t" % (x_black,y_black,x_red,y_red),
        if VERB: print hit
        if hit=='blue':
            x=(b_blue-b)/(a-a_blue)
            y=x*a_blue+b_blue
            theta=360-theta
        elif hit=='black':
            x=(b_black-b)/(a-a_black)
            y=x*a_black+b_black
            theta=240-theta
            if theta<0: theta+=360
        elif hit=='red':
            x=(b_red-b)/(a-a_red)
            y=x*a_red+b_red
            theta=120-theta
            if theta<0: theta+=360
        else:
            print "Error."
            break
        if abs(x)<eps: break   
    print "Theta %.3f - Ray hit %d surfaces" % (Thetas[i], 2*i+1)
