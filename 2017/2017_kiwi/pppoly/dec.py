from math import sqrt

enc = "ASSHAIR"
#enc = '\\\\z"!2)41N'
dec = enc[3:] + enc[0:3]
dec = [ord(dec[i]) for i in range(len(dec))]

plain = ""
for i in range(len(dec)):
	plain += chr(dec[i]-i**2 -5 + 53 - 7)
print plain
