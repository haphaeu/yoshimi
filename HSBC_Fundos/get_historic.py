url = 'https://wwws3.hsbc.com.br/ITE/hwb/HistoricoCotaDia.htm'
source='''
<html>
	<head>
	<title>HSBC Bank Brasil S.A. - Banco M&uacute;ltiplo</title>
<!--
	<meta http-equiv="expires" content="Fri,20 Mar 1998 08:00:00 GMT">
	<meta http-equiv="pragma" content="no-cache">
-->
	</head>
	<frameset name="frameprincipal" id="frameprincipal" border="0" frameborder="0" noresize="noresize" framespacing="0" scroling="auto" rows="90%,10%,*">
		<frame name="central" src="/HWB-SIMULADOR/servlets/SrvSimulador?ServletState=10" noresize="noresize" marginwidth="0" marginheight="0" scrolling="yes"\>
		<frame name="buttons" src="/ITE/common/html/buttons.html" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" noresize="noresize"\>
		<frame name="nada" src="/ITE/common/html/nada.htm" marginwidth="0" marginheight="0" scrolling="0" frameborder="0" noresize="noresize"\>
	</frameset>
	<noframes>
	<body>
		<p>
		Seu Browser não suporta frames.
		</p>
	</body>
	</noframes>
</html>
'''

url2 = 'https://wwws3.hsbc.com.br/HWB-SIMULADOR/servlets/SrvSimulador?ServletState=10'

url3 = 'https://wwws3.hsbc.com.br/HWB-SIMULADOR/servlets/SrvSimulador?ServletState=30'


import sys
import mechanize

request = mechanize.Request(url)
response = mechanize.urlopen(request)
forms = mechanize.ParseResponse(response, backwards_compat=False)
#response.close()
## f = open("example.html")
## forms = mechanize.ParseFile(f, "http://example.com/example.html",
##                              backwards_compat=False)
## f.close()
form = forms[0]
print form  # very useful!
