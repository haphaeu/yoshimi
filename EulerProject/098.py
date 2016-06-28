'''


NAO FUNCIONA ESSA MERDA

Anagramic Squares - Problem 98

By replacing each of the letters in the word CARE with 1, 2, 9, and 6
respectively, we form a square number: 1296 = 362. What is remarkable is that,
by using the same digital substitutions, the anagram, RACE, also forms a square
number: 9216 = 962. We shall call CARE (and RACE) a square anagram word pair
and specify further that leading zeroes are not permitted, neither may a
different letter have the same digital value as another letter.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file
containing nearly two-thousand common English words, find all the square
anagram word pairs (a palindromic word is NOT considered to be an anagram
of itself).
[http://projecteuler.net/project/words.txt]

What is the largest square number formed by any member of such a pair?

NOTE: All anagrams formed must be contained in the given text file.
'''
def readFile(link):
    '''readFile(link) -> list of words'''
    import urllib.request as req
    contents = str(req.urlopen(link).readall())[2:-1].split('","')
    #remove double quotes from first and last words
    contents[0]=contents[0][1:]
    contents[-1]=contents[-1][:-1]
    return contents

def isAnagram(word1, word2):
    '''isAnagram(word1,word2) -> True or False'''
    l1 = [c for c in word1]
    l2 =[c for c in word2]
    l1.sort()
    l2.sort()
    return l1==l2

######################################################################
words=readFile('https://projecteuler.net/project/resources/p098_words.txt')
size = len(words)
pairs = []
for i in range(size):
    for j in range(i+1,size):
        if isAnagram(words[i],words[j]):
            pairs.append((words[i],words[j]))
            print(words[i],'\t',words[j])
print("Checking squares")
matches=set()
for p in pairs:
    sz = len(p[0]) # length of words = number of digits of square number
    n_o = int((10**(sz-1))**0.5)+1 # starting n
    n_f = int((10**(sz))**0.5)  -1 # final n
    Squares=[i*i for i in range(n_o, n_f+1)]
    for sq1 in Squares:
        l1=[str(sq1)[p[1].index(c)] for c in p[0]]
        n1=''
        for n in l1: n1+=n
        n1=int(float(n1))
        
        if n1 in Squares: print(p[0],'\t',p[1],'\t',sq1,'\t',n1)
        matches.add(sq1)
        matches.add(n1)

#remove repeated
new_matches=set()
for m in matches:
    sz = len(str(m))
    sz2= len({c for c in str(m)})
    if sz==sz2: new_matches.add(m)



