# [2017_WhiteHatContest] \[REV] crackme

## Key words

- side-channel attack
- pintool

## Solution

```
$ ./crackme 
PASSCODE : aaaaa
FAILED
```

passcode를 맞춰야 하는 문제입니다. 실행되는 인스트럭터의 갯수를 이용하여 사이드 채널 공격이 가능합니다.

```python
from pwn import *
import string

frequency = {}
password = "H4PPyW1THC0nCTF!"
end_flag = 0
string.printable = string.printable.replace("\t\n\r\x0b\x0c", "")

while True:
	for i in range(len(string.printable)):
		p = process(["../../pin/pin", "-t", "./MyPinTool_64.so", "--", "./crackme"])
		p.recv()
		p.sendline(password + string.printable[i])
		response = p.recvuntil("Count [")
		if "FAILED" not in response:
			password += string.printable[i]
			print "=================="
			print password
                        print "=================="
			exit()
		count = p.recvuntil("]")[:-1]
		if count not in frequency:
			frequency[count] = [1, string.printable[i]]
		else:
			frequency[count][0] += 1
		#print "[{}] ".format(string.printable[i]) + str(count)
		p.close()

	for k in frequency.keys():
		if frequency[k][0] == 1:
			password += frequency[k][1]
			frequency.clear()
			break
	print password
```

## Result

```
$ python ex_crackme.py 
[+] Starting local process '../../pin/pin': pid 8529
==================
H4PPyW1THC0nCTF!
==================
[*] Stopped process '../../pin/pin' (pid 8529)
```

