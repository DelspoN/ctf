f = open("hex", "r")
text = f.read()
f.close()

f = open("parsed", "w")
s = text.split("\n")
for i in range(len(s)):
	t = s[i].split(": ")[1].split("  ")[0]
	f.write(t+"\n")
f.close()
