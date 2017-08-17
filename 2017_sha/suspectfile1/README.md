# [2017_SHA] \[Reversing] Suspect File 1

### Problem

```
root@inj3ct:~/labs/ctf/2017_sha/suspectfile1# ./100
Sorry
```

무조건 Sorry가 뜹니다



### Solution

```
   0x08049dcc <+5468>:	lea    esp,[ebp-0xc]
   0x08049dcf <+5471>:	pop    esi
   0x08049dd0 <+5472>:	pop    edi
   0x08049dd1 <+5473>:	pop    ebx
   0x08049dd2 <+5474>:	pop    ebp
   0x08049dd3 <+5475>:	ret    
   0x08049dd4 <+5476>:	call   0x8048850 <sorry>
   0x08049dd9 <+5481>:	call   0x8048850 <sorry>
   0x08049dde <+5486>:	call   0x8048850 <sorry>
End of assembler dump.
pwndbg> b * 0x08049dd4
Breakpoint 1 at 0x8049dd4
pwndbg> r
Starting program: /root/labs/ctf/2017_sha/suspectfile1/100 
Sorry
[Inferior 1 (process 19083) exited normally]
Warning: not running or target is remote
pwndbg> r a
Starting program: /root/labs/ctf/2017_sha/suspectfile1/100 a

[----------------------------------registers-----------------------------------]
EAX: 0xb3fdf676 
EBX: 0x8048164 (<_init>:	push   ebx)
ECX: 0x9ebe6441 
EDX: 0xe6cbc1fb 
ESI: 0x80ea0c4 --> 0x8068270 (<__strcpy_sse2>:	mov    edx,DWORD PTR [esp+0x4])
EDI: 0xd ('\r')
EBP: 0xffffd448 --> 0x80002001 
ESP: 0xffffd2c0 ("flag{57201791ea"...)
EIP: 0x8049dd4 (<main+5476>:	call   0x8048850 <sorry>)
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8049dd1 <main+5473>:	pop    ebx
   0x8049dd2 <main+5474>:	pop    ebp
   0x8049dd3 <main+5475>:	ret    
=> 0x8049dd4 <main+5476>:	call   0x8048850 <sorry>
   0x8049dd9 <main+5481>:	call   0x8048850 <sorry>
   0x8049dde <main+5486>:	call   0x8048850 <sorry>
   0x8049de3:	xchg   ax,ax
   0x8049de5:	xchg   ax,ax
No argument
[------------------------------------stack-------------------------------------]
0000| 0xffffd2c0 ("flag{57201791ea"...)
0004| 0xffffd2c4 ("{57201791ea24f3"...)
0008| 0xffffd2c8 ("01791ea24f3acd8"...)
0012| 0xffffd2cc ("1ea24f3acd852ce"...)
0016| 0xffffd2d0 ("4f3acd852cee327"...)
0020| 0xffffd2d4 ("cd852cee3271333"...)
0024| 0xffffd2d8 ("2cee3271333a8}\002"...)
0028| 0xffffd2dc ("3271333a8}\002\002")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x08049dd4 in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[──────────────────────────────────REGISTERS───────────────────────────────────]
*EAX  0xb3fdf676
*EBX  0x8048164 (_init) ◂— push   ebx
*ECX  0x9ebe6441
*EDX  0xe6cbc1fb
*EDI  0xd
*ESI  0x80ea0c4 (_GLOBAL_OFFSET_TABLE_+12) —▸ 0x8068270 (__strcpy_sse2) ◂— mov    edx, dword ptr [esp + 4]
*EBP  0xffffd448 ◂— 0x80002001
*ESP  0xffffd2c0 ◂— 0x67616c66 ('flag')
*EIP  0x8049dd4 (main+5476) —▸ 0xffea77e8 ◂— 0xffea77e8
[────────────────────────────────────DISASM────────────────────────────────────]
 ► 0x8049dd4 <main+5476>             call   sorry                         <0x8048850>
        arg[0]: 0x67616c66 ('flag')
        arg[1]: 0x3237357b ('{572')
        arg[2]: 0x39373130 ('0179')
        arg[3]: 0x32616531 ('1ea2')
 
   0x8049dd9 <main+5481>             call   sorry                         <0x8048850>
 
   0x8049dde <main+5486>             call   sorry                         <0x8048850>
 
   0x8049de3                         nop    
   0x8049de5                         nop    
   0x8049de7                         nop    
   0x8049de9                         nop    
   0x8049deb                         nop    
   0x8049ded                         nop    
   0x8049def                         nop    
   0x8049df0 <generic_start_main>    push   esi
[────────────────────────────────────STACK─────────────────────────────────────]
00:0000│ esp  0xffffd2c0 ◂— 0x67616c66 ('flag')
01:0004│      0xffffd2c4 ◂— 0x3237357b ('{572')
02:0008│      0xffffd2c8 ◂— 0x39373130 ('0179')
03:000c│      0xffffd2cc ◂— 0x32616531 ('1ea2')
04:0010│      0xffffd2d0 ◂— 0x61336634 ('4f3a')
05:0014│      0xffffd2d4 ◂— 0x35386463 ('cd85')
06:0018│      0xffffd2d8 ◂— 0x65656332 ('2cee')
07:001c│      0xffffd2dc ◂— 0x31373233 ('3271')
[──────────────────────────────────BACKTRACE───────────────────────────────────]
 ► f 0  8049dd4 main+5476
   f 1  804a011 generic_start_main+545
   f 2  804a20d __libc_start_main+285
Breakpoint * 0x08049dd4
pwndbg> x/10s #esp
Invalid character '#' in expression.
pwndbg> x/10s #esp
Invalid character '#' in expression.
pwndbg> x/10s $esp
0xffffd2c0:	"flag{57201791ea"...
0xffffd2cf:	"24f3acd852cee32"...
0xffffd2de:	"71333a8}\002\002"
```

마지막에 sorry를 호출하는 부분에 bp를 건 후, 인자를 넣어서 실행했더니 flag가 스택에 저장되었다.

문제의 의도는 모르겠다 -_-;;