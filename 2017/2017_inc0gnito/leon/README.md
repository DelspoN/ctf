# [2017_Inc0gnito] \[Reversing] leon

### Problem

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v3; // rax@3
  int result; // eax@6
  __int64 v5; // rbx@6
  char s; // [sp+0h] [bp-60h]@3
  __int64 v7; // [sp+48h] [bp-18h]@1

  v7 = *MK_FP(__FS__, 40LL);
  if ( ptrace(0, 0LL, 1LL, 0LL) == -1 )
    exit(1);
  fgets(&s, 64, _bss_start);
  v3 = strlen(buf);
  if ( !strncmp(&s, buf, v3) )
    puts("Good job!");
  else
    puts("Wrong..");
  result = 0;
  v5 = *MK_FP(__FS__, 40LL) ^ v7;
  return result;
}
```

IDA로 열어보면 Angr 돌리기 쉽게 생겼다는 걸 알 수 있습니다.



### Solution

```python
import angr

project = angr.Project("./leon", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x400867,avoid=0x400873)

print path_group.found[0].state.posix.dumps(0)
```

분석하기 귀찮으니깐 그냥 Angr 돌려봅시다

```
# python ex.py 
WARNING | 2017-08-25 12:35:03,398 | claripy | Claripy is setting the recursion limit to 15000. If Python segfaults, I am sorry.
INC0{doesn't_seem_to_be_write_something..}? @@ ??@??@??
```

