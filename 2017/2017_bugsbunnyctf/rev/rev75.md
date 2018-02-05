# [2017_BugsBunny] \[Reversing] rev75

### Solution

`strings rev75`를 해서 살펴보면 base64 형식의 문자열이 등장합니다. png 파일이 암호화된 것으로 추측됩니다.

`strings rev75 | grep '^[a-zA-Z0-9+\/=]\{12\}$' > rev75_tmp`로 base64문자열을 모두 추출했습니다

```python
import base64
f = open('rev75_tmp','r')
c = f.read()
f.close()

f = open('rev75_flag.png','w')
f.write(base64.decodestring("".join(c[:-4])))
f.close()
```

뒤의 4줄은 base64로 암호화된 문자열이 아니라서 제외해줬습니다.

위를 통해 추출된 png 파일을 복호화하면 다음과 같은 이미지가 나타납니다.![rev75_flag](rev75_flag.png)

이미지가 손상된 채로 나오는데 이미지 복구 툴을 이용하여 복구하여 문제를 해결하였습니다.

![rev75_flag_recovered](rev75_flag_recovered.png)