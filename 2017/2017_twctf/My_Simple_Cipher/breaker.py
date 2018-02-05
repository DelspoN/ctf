#!/usr/bin/python2

import sys
import random
import string



def encrypt(key, flag):

	assert len(key) == 13
	assert max([ord(char) for char in key]) < 128
	assert max([ord(char) for char in flag]) < 128

	encrypted = '\x7c'
	message = flag + '|' + key

	for i in range(0, len(message)):
	  encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)

	return encrypted

def main():
	encrypted = "7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e".decode("hex")

	"""
	# Brute force key[0:6]
	flag = "TWCTF{flagflagflagfl}"
	key = "keykeykeykeyk"
	message = flag + "|" + key
	for i in range(6):
		for j in range(len(string.printable)):
			key = list(key)
			key[i] = string.printable[j]
			key = ''.join(key)
			tmp = encrypt(key, flag)

			if tmp[1:i+2] == encrypted[1:i+2]:
				print "key = " + key
				break
	"""

	# Brute force key[6:]
	# key = "ENJ0YHkeykeyk"
	# chr((ord(encrypted[28]) + ord(key[2]) + ord('O') % 128) == encrypted[29]
	# chr((ord(encrypted[29]) + ord(key[3]) + ord('L')) % 128) == encrypted[30]
	# ...
	# key = "ENJ0YHOLIDAY!"


	# Brute force flag
	flag = "TWCTF{flagflagflagfl}"
	key = "ENJ0YHOLIDAY!"
	for i in range(6,20):
		for j in range(len(string.printable)):
			flag = list(flag)
			flag[i] = string.printable[j]
			flag = ''.join(flag)
			tmp = encrypt(key, flag)

			if tmp[6:i+2] == encrypted[6:i+2]:
				print "flag = " + flag
				break

if __name__ == "__main__":
	main()

"""
key length is 13
encrypted length is 36
message length is 35
flag length is 21

flag = "TWCTF{flagflagflagfl}"
message = "TWCTF{flagflagflagfl}|keykeykeykeyk"

key = "ENJ0YHkeykeyk"
message = "TWCTF{flagflagflagfl}|ENJ0YHkeykeyk"
		   ENJ0YHkeykeykENJ0YHkeykeykENJ0YHkey


"""