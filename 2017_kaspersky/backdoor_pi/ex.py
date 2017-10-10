import hashlib

user = "b4ckd00r_us3r"
pincode_base = 12171337

while True:
	pincode = str(pincode_base)
	print pincode
	if len(pincode) <= 8:
		val = '{}:{}'.format(user, pincode)
		key = hashlib.sha256(val).hexdigest()
		if key == '34c05015de48ef10309963543b4a347b5d3d20bbe2ed462cf226b1cc8fff222e':
			print val
			break
        	pincode_base += 1
	else:
		break
print "completed"
