import base64
f = open('rev75_tmp','r')
c = f.read()
f.close()

f = open('rev75_flag.png','w')
f.write(base64.decodestring("".join(c[:-4])))
f.close()
