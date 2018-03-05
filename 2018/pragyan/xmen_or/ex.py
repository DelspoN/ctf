import base64
import hashlib
from Crypto.Cipher import AES

def xor(a, b):
	result = ""
	for i in range(len(a)):
		result += chr(ord(a[i]) ^ ord(b[i]))
	return result

f = open("info_clear.txt", "r")
data_clear=f.read()
f.close()

f = open("info_crypt.txt", "r")
data_crypt=f.read()
f.close()

f = open("superheroes_group_info_crypt.txt", "r")
flag_crypt=base64.b64decode(f.read())
f.close()

dec1 = xor(data_clear, data_crypt).rstrip("\n")
m = hashlib.md5()
m.update(dec1)
key = m.hexdigest()
print "KEY : " + key

aes = AES.new(key, AES.MODE_ECB)
flag = aes.decrypt(flag_crypt)
print "FLAG : " + flag