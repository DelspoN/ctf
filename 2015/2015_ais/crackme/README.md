# [2015_AIS] \[Reversing] CRACKME

### Problem

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax@2

  if ( argc == 2 )
  {
    if ( verify(argv[1], argv, envp) )
      puts("Correct! that is the secret key!");
    else
      puts("I'm sorry, that's the wrong secret key!");
    result = 0;
  }
  else
  {
    puts("You need to enter the secret key!");
    result = -1;
  }
  return result;
}
```

일반적인 angr를 통한 문제 풀이와는 다르게 scanf, gets와 같은 함수를 통해 입력받지 않고 argv의 값을 이용합니다. 외부 참조 변수를 관리하려면 claripy를 이용해야 합니다.

###Solution

```python
import angr

p = angr.Project("crackme", load_options={'auto_load_libs':False})
argv1 = angr.claripy.BVS("argv1",100*8)
path1 = p.factory.path(args=['./crackme1',argv1])
ex = p.factory.path_group(path1)
ex.explore(find=0x400602, avoid=0x40060E)
print ex.found[0].state.se.any_str(argv1)
```

