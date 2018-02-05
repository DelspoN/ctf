f = open("egg_sha", "r")
sha = f.read()
f.close

sha = sha.replace("0x", "0")
sha = sha.replace("\n", "")
sha = sha.decode("hex")

key = "Mh;y;mR1@OijQhHW6Ah=hB"

flag = ""
for i in range(len(key)):
	flag += chr(ord(sha[i]) ^ ord(key[i]))

print flag
