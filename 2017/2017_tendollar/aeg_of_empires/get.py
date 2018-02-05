from pwn import *
import base64

r = remote("45.32.31.134", 20100)
r.recvuntil("(You have 20 sec to solve)")
r.recvline()
r.recvline()

data = ""
while True:
	data += r.recv()
	if "#" in data:
		data = data.replace("\x0a", "")
		data = data.replace("#", "")
		data = base64.decodestring(data)
		break

f = open("aeg", "wb")
f.write(data)
f.close()

