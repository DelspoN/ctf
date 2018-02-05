from pwn import *
import string

frequency = {}
password = "H4PPyW1THC0nCTF!"
end_flag = 0
string.printable = string.printable.replace("\t\n\r\x0b\x0c", "")

while True:
	for i in range(len(string.printable)):
		p = process(["../../pin/pin", "-t", "./MyPinTool_64.so", "--", "./crackme"])
		p.recv()
		p.sendline(password + string.printable[i])
		response = p.recvuntil("Count [")
		if "FAILED" not in response:
			password += string.printable[i]
			print "=================="
			print password
                        print "=================="
			exit()
		count = p.recvuntil("]")[:-1]
		if count not in frequency:
			frequency[count] = [1, string.printable[i]]
		else:
			frequency[count][0] += 1
		#print "[{}] ".format(string.printable[i]) + str(count)
		p.close()

	for k in frequency.keys():
		if frequency[k][0] == 1:
			password += frequency[k][1]
			frequency.clear()
			break
	print password

