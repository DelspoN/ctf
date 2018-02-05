import requests

url = "http://52.78.188.150/rbsql_4f6b17dc3d565ce63ef3c4ff9eef93ad/?page=login_chk"
#url  = "http://192.168.124.139/rbSql/tmp/?page=login_chk"
data = {
        "uid" : "aaa10",
        "upw" : "ccc",
        }
r = requests.post(url, data=data)
print r.status_code
response = r.text
print response
