
def deca(e):
        out = ""
        for i in range(len(e)):
                out += chr(ord(e[i]) ^ 0x58)
        return out

def decb(e):
        out = ""
        for i in range(len(e)):
                out += chr(ord(e[i]) ^ 0x6f)
        return out

def dec(e):
	out = ""
	for i in range(len(e)):
		out += chr(ord(e[i]) ^ 0x4b)
	return out

f = open("encrypted", "r")
enc = f.read()
enc = enc.strip()
f.close()

decrypted = dec(enc)
decrypted = deca(decrypted)
decrypted = decb(decrypted)
print decrypted.decode("hex")

# ./e > encrypted
# Deleting dummy in encrypted
# python sol.py > flag.png
