import time

print("Calling python")
time.sleep(2)

with open("hello.txt", 'w') as pf:
    pf.write("Hello from Python\n")

print("Done")
time.sleep(1)
