import sys
print "Hello!"
sys.stdout.write("\x1b[A") # Move the cursor up one line
print "Hello!"