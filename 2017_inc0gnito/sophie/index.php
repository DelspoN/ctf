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
