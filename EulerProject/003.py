def isPrime(n):
    i=2L
    while i<n:
        if n%i==0:
            return False
        i += 1
    return True
    
n=600851475143L
#n=13195

i=1L
p=1L
while True: 
    if n%i==0:
        print "factor", i,
        if isPrime(i):
            print "prime!!!"
            p *= i
            if p==n:
                print "done"
                break
        else:
            print "not prime"
            n /= i
    i += 1L



        

