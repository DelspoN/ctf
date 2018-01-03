# [2017_34C3CTF] \[REV] morph

## Key words

* gdb script

## Description

```
To get you started :)

files: Link

difficulty: easy
```

## Solution

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  signed int i; // [rsp+14h] [rbp-1Ch]
  void *dest; // [rsp+18h] [rbp-18h]
  __int64 v6; // [rsp+20h] [rbp-10h]
  __int64 v7; // [rsp+28h] [rbp-8h]

  dest = mmap(0LL, 0x1000uLL, 7, 34, -1, 0LL);
  sub_8D0(dest);
  memcpy(dest, src, 0x2F5uLL);
  if ( a1 != 2 )
    exit(1);
  if ( strlen(a2[1]) != 23 )
    exit(1);
  sub_987();
  for ( i = 0; i <= 22; ++i )
  {
    v6 = *(8LL * i + flag_char_list_202020);
    v7 = *(8 * (i + 1LL) + flag_char_list_202020);
    if ( v7 )
      (*v6)(&a2[1][*(v6 + 9)], *v7, *(v7 + 8));
    else
      (*v6)(&a2[1][*(v6 + 9)], dest, 0LL);
  }
  puts("What are you waiting for, go submit that flag!");
  return 0LL;
}
```

`sub_987`에서 flag를 랜덤 순서로 encrypt한 후, 입력 값과 `flag`를 비교합니다.

랜덤으로 선정된 pos와 그 값을 뽑아내서 argv 값을 하나씩 변경하는 gdb 스크립트를 짜서 해결했습니다.

## Code

```
file ./morph
b *(0x555555554AE9)
b *(0x555555554b35)
r `python -c 'print "3"*23'`

set $argv1 = *(char **)($rax + 8)
set $cnt = 0
c
while($cnt < 23)
set $pos = *($rax + 9)
set $flag = *(*(byte **)$rax + 5)
set *($argv1+$pos) = $flag
printf "[%d] %c %s\n", $pos, $flag, $argv1
c
set $cnt = $cnt + 1
end
```

## 실행 결과

```
Breakpoint 3, 0x0000555555554b35 in ?? ()
[4] _ 34C3_M1GHTY_M0RPh1nG_g0
What are you waiting for, go submit that flag!
[Inferior 1 (process 12754) exited normally]
Warning: not running or target is remote
```

