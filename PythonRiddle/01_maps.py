abc="abcdefghijklmnopqrstuvwxyz"
n=len(abc)
text="g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
text2=""
for a in text:
    if a==" " or a=="." or a=="'" or a=="(" or a==")": 
      text2+=a
    else:
      i=2+abc.find(a)
      if i >= n: i-=n
      text2+=abc[i]
print text2

# ====
# and now the easy way

import string
table=string.maketrans(string.ascii_lowercase,string.ascii_lowercase[2:]+string.ascii_lowercase[0:2])
print string.translate(text, table)

# =====
# url is 'map'
print string.translate('map',table)
