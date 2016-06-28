"""
a little bit more sofisticated print

again, if this is used as:
import script2

the function say_hi will be run as it is imported

alternatively, the main script doesn't need to call say_hi, in this case
you can import the script and have the function available, but the script cannot
be run as a stand alone script.
"""
def say_hi():
    print("Hi! I'm script2.py - just a function say_hi()")

say_hi()
