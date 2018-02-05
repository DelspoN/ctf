# [2017_TWCTF] \[Crypto] My Simple Cipher

### Problem

```python
#!/usr/bin/python2

import sys
import random

key = sys.argv[1]
flag = '**CENSORED**'

assert len(key) == 13
assert max([ord(char) for char in key]) < 128
assert max([ord(char) for char in flag]) < 128

message = flag + "|" + key

encrypted = chr(random.randint(0, 128))

for i in range(0, len(message)):
  encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)

print(encrypted.encode('hex'))
```

Encryption 코드는 위와 같습니다. encrypted의 이전 바이트 + message의 이전 바이트 + key의 이전 바이트가 연산되어 암호문의 다음 바이트가 됩니다. (`encrypted[n+1] = chr((ord(encrypted[n]) + ord(message[n]) + ord(key[n])) % 128)`)

`7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e`을 복호화하면 flag가 나옵니다.



### Solution

플래그 형식이 `TWCTF{`로 시작한다는 점에서 Brute forcing을 통해 key 값 첫 6바이트를 알아낼 수 있습니다.

이를 통해 구한 key의 첫 6바이트는 `ENJ0YH`입니다

코드를 분석해보며 알겠지만 key의 길이는 13바이트입니다. 암호문은 36바이트, 그러면 message는 36바이트가 되고 결국 flag는 21바이트가 됩니다.

저는 key가 반복 사용된다는 점에 주목했습니다. 그러면 결국 아래와 같이 맵핑되어 연산이 수행될 것입니다.

```
TWCTF{flagflagflagfl}|ENJ0YHkeykeyk
ENJ0YHkeykeykENJ0YHkeykeykENJ0YHkey
```

임의로 사용한 더미 바이트, `key`라는 문자열과 진짜 key 값에 존재하는, `J0Y`라는 문자열이 연산된다는 점을 이용해 key를 구할 수 있습니다. 

```
# Brute force key[6:]
# key = "ENJ0YHkeykeyk"
# chr((ord(encrypted[28]) + ord(key[2]) + ord('O') % 128) == encrypted[29]
# chr((ord(encrypted[29]) + ord(key[3]) + ord('L')) % 128) == encrypted[30]
# ...
```

위와 같은 방식을 통해 key 값을 브루트 포싱을 해보면 `ENJ0YHOLIDAY!`가 나옵니다.

이제 flag 값을 브루트 포싱하여 구하면 됩니다.

```
#!/usr/bin/python2

import sys
import random
import string



def encrypt(key, flag):

	assert len(key) == 13
	assert max([ord(char) for char in key]) < 128
	assert max([ord(char) for char in flag]) < 128

	encrypted = '\x7c'
	message = flag + '|' + key

	for i in range(0, len(message)):
	  encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)

	return encrypted

def main():
	encrypted = "7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e".decode("hex")

	"""
	# Brute force key[0:6]
	flag = "TWCTF{flagflagflagfl}"
	key = "keykeykeykeyk"
	message = flag + "|" + key
	for i in range(6):
		for j in range(len(string.printable)):
			key = list(key)
			key[i] = string.printable[j]
			key = ''.join(key)
			tmp = encrypt(key, flag)

			if tmp[1:i+2] == encrypted[1:i+2]:
				print "key = " + key
				break
	"""

	# Brute force key[6:]
	# key = "ENJ0YHkeykeyk"
	# chr((ord(encrypted[28]) + ord(key[2]) + ord('O') % 128) == encrypted[29]
	# chr((ord(encrypted[29]) + ord(key[3]) + ord('L')) % 128) == encrypted[30]
	# ...
	# key = "ENJ0YHOLIDAY!"


	# Brute force flag
	flag = "TWCTF{flagflagflagfl}"
	key = "ENJ0YHOLIDAY!"
	for i in range(6,20):
		for j in range(len(string.printable)):
			flag = list(flag)
			flag[i] = string.printable[j]
			flag = ''.join(flag)
			tmp = encrypt(key, flag)

			if tmp[6:i+2] == encrypted[6:i+2]:
				print "flag = " + flag
				break

if __name__ == "__main__":
	main()

"""
key length is 13
encrypted length is 36
message length is 35
flag length is 21

flag = "TWCTF{flagflagflagfl}"
message = "TWCTF{flagflagflagfl}|keykeykeykeyk"

key = "ENJ0YHkeykeyk"
message = "TWCTF{flagflagflagfl}|ENJ0YHkeykeyk"
		  ENJ0YHkeykeykENJ0YHkeykeykENJ0YHkey


"""
```



### 실행 결과

```
$ python breaker.py 
flag = TWCTF{Clagflagflagfl}
flag = TWCTF{Cragflagflagfl}
flag = TWCTF{Crygflagflagfl}
flag = TWCTF{Crypflagflagfl}
flag = TWCTF{Cryptlagflagfl}
flag = TWCTF{Cryptoagflagfl}
flag = TWCTF{Crypto-gflagfl}
flag = TWCTF{Crypto-iflagfl}
flag = TWCTF{Crypto-islagfl}
flag = TWCTF{Crypto-is-agfl}
flag = TWCTF{Crypto-is-fgfl}
flag = TWCTF{Crypto-is-fufl}
flag = TWCTF{Crypto-is-funl}
flag = TWCTF{Crypto-is-fun!}
```

