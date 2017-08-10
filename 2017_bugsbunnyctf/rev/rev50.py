from pwn import *

f = open("rev50_strings", "r")
strings = f.read()
f.close()

strings = strings.split("\n")

for i in range(len(strings)):
	p = process(["./rev50", strings[i]])
	if "Bad" not in p.recv():
		print strings[i]
		break
	p.close()

