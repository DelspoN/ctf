# [2017_Kaspersky] \[Crypto] decrypt the message

## Key words

- Padding oracle attack | 패딩 오라클 어택

## Description

```
Could your decrypt the message? http://95.85.51.183
```

## Analysis

정상적인 요청 - `user_info = "+JscCdxACjR6RrQsUDgJbh9jDjl2FsKBcYAiaoS0Nztol5rc1/vYGKaBg6K11LKG7C21izSk0fTKkBhxPm4qsw=="`

```
Hello ddd
```



비정상적인 요청1 - `user_info = "+JscCdxACjR6RrQsUDgJbh9jDjl2FsKBcYAiaoS0Nztol5rc1/vYGKaBg6K11LKG7C21izSk0fTKkBhxPm4qsa=="`

```
Traceback (most recent call last):
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1612, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1598, in dispatch_request
return self.view_functions[rule.endpoint](**req.view_args)
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 53, in index
user_info_decrypted = json.loads(aes_decrypt(user_info).decode())
File "/usr/lib/python2.7/json/__init__.py", line 339, in loads
return _default_decoder.decode(s)
File "/usr/lib/python2.7/json/decoder.py", line 364, in decode
obj, end = self.raw_decode(s, idx=_w(s, 0).end())
File "/usr/lib/python2.7/json/decoder.py", line 382, in raw_decode
raise ValueError("No JSON object could be decoded")
ValueError: No JSON object could be decoded
```

input에 따라 오류 메시지를 확인할 수 있습니다.



비정상적인 요청2 - `user_info = "+JscCdxACjR6RrQsUDgJbh9jDjl2FsKBcYAiaoS0Nztol5rc1/vYGKaBg6K11LKG7C21izSk0fTKkBhxPm4qsaa=="`

```
Traceback (most recent call last):
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1612, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1598, in dispatch_request
return self.view_functions[rule.endpoint](**req.view_args)
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 53, in index
user_info_decrypted = json.loads(aes_decrypt(user_info).decode())
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 35, in aes_decrypt
return unpad(cipher.decrypt( enc[16:] ))
File "/usr/local/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 295, in decrypt
return self._cipher.decrypt(ciphertext)
ValueError: Input strings must be a multiple of 16 in length
```

`return unpad(cipher.decrypt( enc[16:] ))`를 보아 16바이트 블록 암호인 것으로 추정됩니다.



비정상적인 요청3 - `user_info = "+JscCdxACjR6RrQsUDgJ7h9jDjl2FsKBcYAiaoS0Nztol5rc1/vYGKaBg6K11LKG7C21izSk0fTKkBhxPm4qsw=="`

```
Traceback (most recent call last):
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1612, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1598, in dispatch_request
return self.view_functions[rule.endpoint](**req.view_args)
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 53, in index
user_info_decrypted = json.loads(aes_decrypt(user_info).decode())
UnicodeDecodeError: 'ascii' codec can't decode byte 0xa0 in position 15: ordinal not in range(128)
```

16번째 바이트를 `\xee`로 바꿔서 보냈더니 위와 같은 오류 메시지를 확인할 수 있었습니다. 이 오류를 통해 `aes_decrypt(user_info).decode()`의 결과 즉, 최종적으로 완성되는 암호문을 확인할 수 있습니다.

3번의 오류 메시지를 이용하여 패딩 오라클 공격이 가능합니다.

## Exploit

```
조작된 암호문 xor 조작된 평문 = intermediary
intermediary xor Inital Vector = 평문
```

위의 식을 이용하여 브루트포싱을 해줍니다.

``` python
import requests
import base64

url = "http://95.85.51.183/"

def get_mal_plain(mal_cipher):
	cookie = dict(user_info="\""+base64.b64encode(mal_cipher)+"\"")

        r = requests.get(url, cookies = cookie)
        response = r.text

        if "UnicodeDecodeError: 'ascii' codec" in response:
		tmp = response.split("decode byte 0x")[1].split(" ")
		return int(tmp[0],16)
	return -1

cipher = "S6rw59a355xp9NJXwMxl0r/ZywhlX6d619xjQ71Q4KQGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg=="
cipher = base64.decodestring(cipher)
block_size = 16
plain = ""

# mal_cipher ^ mal_plain = intermediary
# intermediary ^ iv = plain

for i in range(4):
	for idx in range(block_size):
		for bf in range(0x100):
			mal_cipher = list(cipher[i*block_size:])
			mal_cipher[idx] = chr(bf)
			mal_cipher = ''.join(mal_cipher)

			mal_plain = get_mal_plain(mal_cipher)
			if mal_plain != -1:
				plain += chr(ord(cipher[i*block_size+idx]) ^ ord(mal_cipher[idx]) ^ mal_plain)
				print "plain = {}".format(plain)
				break
```

실행 결과는 다음과 같습니다.

```
plain = {
plain = {"
plain = {"n
plain = {"na
plain = {"nam
plain = {"name
plain = {"name"
plain = {"name":
plain = {"name": 
plain = {"name": "
plain = {"name": "2
plain = {"name": "2"
plain = {"name": "2",
plain = {"name": "2", 
plain = {"name": "2", "
plain = {"name": "2", "s
plain = {"name": "2", "sh
plain = {"name": "2", "sho
plain = {"name": "2", "show
plain = {"name": "2", "show_
plain = {"name": "2", "show_f
plain = {"name": "2", "show_fl
plain = {"name": "2", "show_fla
plain = {"name": "2", "show_flag
plain = {"name": "2", "show_flag"
plain = {"name": "2", "show_flag":
plain = {"name": "2", "show_flag": 
plain = {"name": "2", "show_flag": f
plain = {"name": "2", "show_flag": fa
plain = {"name": "2", "show_flag": fal
plain = {"name": "2", "show_flag": fals
plain = {"name": "2", "show_flag": false
plain = {"name": "2", "show_flag": false}
```

show_flag의 값을 true로 바꾼 후 다시 암호화해야 합니다.

```
평문 xor Initial Vector = intermediary
intermediary xor 조작된 평문 = 조작된 암호문
```

위 식을 이용하여 브루트포싱하면 암호문을 만들 수 있습니다.

평문이 33bytes인데 이 길이와 맞춰주기 위해 `{"name": "2", "show_flag": true }` true 뒤에 공백을 넣어줍니다.

그 후, 두번째 블록의 평문을 연산합니다.(name이 1바이트가 넘으면 평문의 길이가 더 커지므로 세번째 블록도 연산해줘야 합니다.)

이제 첫번째 블록의 값만 브루트포싱하여 암호문을 완성시키면 됩니다.

```python
import requests
import base64

url = "http://95.85.51.183/"

def get_mal_plain(mal_cipher, position):
	cookie = dict(user_info="\""+base64.b64encode(mal_cipher)+"\"")

        r = requests.get(url, cookies = cookie)
        response = r.text

	if "UnicodeDecodeError: 'ascii' codec" in response:
		tmp = response.split("decode byte 0x")[1].split(" ")
		if int(tmp[3].replace(':','')) == position:
			return int(tmp[0], 16)
	return -1

cipher = "S6rw59a355xp9NJXwMxl0r/ZywhlX6d619xjQ71Q4KQGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg=="
cipher = base64.decodestring(cipher)
plain		= '{"name": "2", "show_flag": false}'
mal_plain_text  = '{"name": "2", "show_flag": true }'
mal_cipher_text = ''
block_size = 16

# plain ^ iv = intermediary
# intermediary ^ mal_plain = mal_cipher

mal_cipher = list("\x00"*16 + cipher[16:])
for i in range(16, 32):
	mal_cipher[i] = chr(ord(plain[i]) ^ ord(cipher[i]) ^ ord(mal_plain_text[i]))
mal_cipher = ''.join(mal_cipher)

for idx in range(block_size):
	for bf in range(0x100):
		mal_plain = get_mal_plain(mal_cipher,idx)
		if mal_plain != -1:
			mal_cipher = list(mal_cipher)
			mal_cipher[idx] = chr(ord(mal_cipher[idx]) ^ mal_plain ^ ord(mal_plain_text[idx]))
			mal_cipher = ''.join(mal_cipher)
			print "[{}] mal_cipher = {}".format(idx, mal_cipher.encode("hex"))
			print base64.b64encode(mal_cipher)
			break
		mal_cipher = list(mal_cipher)
                mal_cipher[idx] = chr(bf)
                mal_cipher = ''.join(mal_cipher)
```

실행결과는 다음과 같습니다.

```
[0] mal_cipher = dd000000000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3QAAAAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[1] mal_cipher = dd7e0000000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X4AAAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[2] mal_cipher = dd7e7700000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53AAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[3] mal_cipher = dd7e771c000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[4] mal_cipher = dd7e771ca20000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[5] mal_cipher = dd7e771ca22300000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIjAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[6] mal_cipher = dd7e771ca223fe000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/gAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[7] mal_cipher = dd7e771ca223fefd0000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0AAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[8] mal_cipher = dd7e771ca223fefd0600000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0GAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[9] mal_cipher = dd7e771ca223fefd06bd000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0GvQAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[10] mal_cipher = dd7e771ca223fefd06bddb0000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0GvdsAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[11] mal_cipher = dd7e771ca223fefd06bddb3a00000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6AAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[12] mal_cipher = dd7e771ca223fefd06bddb3a59000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WQAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[13] mal_cipher = dd7e771ca223fefd06bddb3a59900000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WZAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[14] mal_cipher = dd7e771ca223fefd06bddb3a5990a400bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WZCkAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[15] mal_cipher = dd7e771ca223fefd06bddb3a5990a41ebfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WZCkHr/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
```

## Result

```
Hello 2
Flag: KLCTFFDA616A6DAF4E63A9F7B55B43124E548
```

