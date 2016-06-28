import sys
import time

# output is printed in the same line by not
# printing the 'new line' character '\n'
# instead, the carriage return is printed
# '\r', which bringes the cursor back to
# the start of the same line
#
# Note: maybe it is needed to call the function
# sys.stdout.flush() at some point to clear
# the buffer, in this simple example is was not
# needed
    
sys.stdout.write('some data\r')
sys.stdout.flush()
time.sleep(1) # wait 1 second...
sys.stdout.write('other different data\r')
sys.stdout.flush()
time.sleep(1) # wait 1 second...

#clear line
sys.stdout.write('                      \r')
sys.stdout.flush()

#print a moving progress bar and percentage
# Progress [=======] 40%
# every '=' represents 3% increment [range(i/3)]
for i in range(101):
    sys.stdout.write('Progress [')
    sys.stdout.flush()
    for j in range(i/3):
        sys.stdout.write('=')
    sys.stdout.write('] %i%%\r' % i)
    sys.stdout.flush()
    time.sleep(0.02)

time.sleep(1)

