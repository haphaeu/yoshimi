def wordVal(word):
#assuming all letters are capitals!!!
#ord('A')=65
    return sum([ord(c)-64 for c in word])

words=open('042.txt').read().replace('"','').split(',')
#max term required in the triangular sequence:
#tn=1/2n(n+1) and max(wordsVal)=192 => n^2+n=384 => n=20
triangVals=[(n*(n+1))>>1 for n in range(1, 21)]
#now check which word is triangular
print len([wordVal(wd) for wd in words if wordVal(wd) in triangVals])
#output is
#162
