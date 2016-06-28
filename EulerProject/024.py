#this took approx 1h
#
#should try this next:
# http://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order


#items starting with zero
st=123456789
end=9876543210
position=0
zeros=0
while st<=end:
    s=str(st)
    if st==1000000000:
        zeros=1
    if       s.count('1')==1 \
        and s.count('2')==1 \
        and s.count('3')==1 \
        and s.count('4')==1 \
        and s.count('5')==1 \
        and s.count('6')==1 \
        and s.count('7')==1 \
        and s.count('8')==1 \
        and s.count('9')==1 \
        and s.count('0')==zeros:
            position += 1
            print position,  st
            if position==1000000:
                print st
                break
    st+=1
