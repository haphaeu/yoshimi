def dummyc():
    cdef a = 0
    cdef i = 0
    for i in range(int(1e7)):
        a += i

def dummy():
    a = 0
    i = 0
    for i in range(int(1e7)):
        a += i