import urllib
import re

symbol='NYSE:PBR'

base_url = 'http://finance.google.com/finance?q='
content = urllib.urlopen(base_url + symbol).read()
m = re.search('class="pr".*?>(.*?)<', content)
if m:
    quote = m.group(1)
else:
    quote = 'no quote available for: ' + symbol

print quote
