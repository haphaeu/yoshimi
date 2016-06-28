digs='0123456789abcdefghijklmnopqrstuvwxyz'

def int2base(x, base):
  if x < 0: sign = -1
  elif x==0: return '0'
  else: sign = 1
  x *= sign
  digits = []
  while x:
    digits.append(digs[x % base])
    x /= base
  if sign < 0:
    digits.append('-')
  digits.reverse()
  return ''.join(digits)

n=2
k=2
seq=[n]
while n:
  n=int(int2base(n,k),k+1)-1
  seq.append(n)
  k+=1