# [2017_BOB] \[WEB] mencrypt

\* 서버가 닫혀 있어서 기억을 바탕으로 작성합니다.

### Problem

PHP 소스코드를 보여주는데 특정 문자열들을 암호화하여 조건이 맞으면 플래그를 출력해줍니다.

```php
<?
function encrypt($a){ 
$s_vector_iv=mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_3DES, MCRYPT_MODE_ECB)); 
$unpacked=unpack("H*", $a); 
$key="thisisnothingjustctrc^0^"; 
$out_str = mcrypt_encrypt(MCRYPT_3DES, $key, $unpacked[1], MCRYPT_MODE_ECB, $s_vector_iv); 
$baseout = base64_encode($out_str); 
return $baseout; 
} 
?>
```

암호화 함수는 위와 같습니다.



### Solution

```php
<?
function decrypt($baseout){ 
$out_str = base64_decode($baseout); 

$key="thisisnothingjustctrc^0^"; 

$s_vector_iv=mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_3DES, MCRYPT_MODE_ECB)); 
$packed = mcrypt_decrypt(MCRYPT_3DES, $key, $out_str, MCRYPT_MODE_ECB, $s_vector_iv); 

$a=pack("H*",$packed); 
return $a;
} 

echo "\n";
echo decrypt("zgOEDsB65W0GshSvbQYSgxk6TauRq603IOQUo/deoMZX+rHumxJxffRY5Lt2jLUE");
echo "\n";
echo decrypt("NBiXUTco+4u1wWg9PFRkxpMNF4pnylFR");

/*
imtheflag^0^sweetiecook2
cngrtulation
http -f POST http://192.168.32.101/hiprob.php?w=imtheflag^0^ "COOKIE:q=sweetiecook2" e=cngrtulation
*/
?>
```

복호화 함수를 작성한 뒤 복호화해보니 `imtheflag^0^ sweetiecook2 cngrtulation`이 나왔습니다. 조건문에 맞게 입력을 넣으면 플래그가 출력됩니다.