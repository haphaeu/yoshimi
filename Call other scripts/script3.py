"""
a little bit more sofisticated print

this is a proper way of making a script that can run stand alone and that you
can use its functions after importing it with
import script3

nothing will be run and the function say_hi() will be available to be called.
"""
def say_hi(name):
    print("Hi %s! I'm script3.py, the sofisticated through __name__ and main()" % name)


def main(name):
    say_hi(name)

_name='Raf'
if __name__=='__main__':     
    main(_name)