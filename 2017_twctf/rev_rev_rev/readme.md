# [2017_TWCTF] \[Reversing] rev_rev_rev

### Problem

```c
int __cdecl main()
{
  int result; // eax@7
  int v1; // edx@7
  char s; // [sp+1Bh] [bp-2Dh]@1
  int v3; // [sp+3Ch] [bp-Ch]@1

  v3 = *MK_FP(__GS__, 20);
  puts("Rev! Rev! Rev!");
  printf("Your input: ");
  if ( !fgets(&s, 33, stdin) )
  {
    puts("Input Error.");
    exit(0);
  }
  sub_80486B9(&s);
  sub_80486DB(&s);
  sub_8048738(&s);
  sub_80487B2(&s);
  if ( !strcmp(&s, s2) )
    puts("Correct!");
  else
    puts("Invalid!");
  result = 0;
  v1 = *MK_FP(__GS__, 20) ^ v3;
  return result;
}
```

한눈에 봐도 Angr를 돌리기 쉽게 생겼습니다.



### Solution

```python
import angr

project = angr.Project("./rev_rev_rev", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x08048679,avoid=0x0804868B)

print path_group.found[0].state.posix.dumps(0)
```



### 실행 결과

```
# python ex.py 
WARNING | 2017-09-04 14:48:51,007 | claripy | Claripy is setting the recursion limit to 15000. If Python segfaults, I am sorry.
?TWCTF{qpzisyDnbmboz76oglxpzYdk}
```

