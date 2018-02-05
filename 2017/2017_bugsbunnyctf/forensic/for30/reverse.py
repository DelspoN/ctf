f = open("UNKOWN", "r")
content = f.read()
f.close()

content = content[::-1]
f = open("KNOWN.png", "w")
f.write(content)
f.close()
