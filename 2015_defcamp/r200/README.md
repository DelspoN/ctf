# [2015_Defcamp] \[Reversing] r200

### Problem

```c
signed __int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  _BYTE *v3; // rax@2
  signed __int64 result; // rax@6
  __int64 v5; // rcx@9
  signed int i; // [sp+4h] [bp-1Ch]@1
  char s; // [sp+10h] [bp-10h]@4
  __int64 v8; // [sp+18h] [bp-8h]@1

  v8 = *MK_FP(__FS__, 40LL);
  for ( i = 1; i <= 10; ++i )
  {
    v3 = malloc(0x10uLL);
    *(_DWORD *)v3 = i;
    v3[4] = *(_DWORD *)v3 + 109;
    a3 = (char **)qword_601080;
    *((_QWORD *)v3 + 1) = qword_601080;
    qword_601080 = (__int64)v3;
  }
  printf("Enter the password: ", a2, a3);
  if ( fgets(&s, 7, stdin) )
  {
    if ( sub_40074D(&s, 7LL) )
    {
      puts("Incorrect password!");
      result = 1LL;
    }
    else
    {
      puts("Nice!");
      result = 0LL;
    }
  }
  else
  {
    result = 0LL;
  }
  v5 = *MK_FP(__FS__, 40LL) ^ v8;
  return result;
}
```

분기문이 있습니다. r100과는 다르게 반복문이 있고 더 복잡합니다. 그래서 기존의 방식을 이용하면 시간도 많이 걸립니다. 특히 state explosion에 문제가 생겨서 오류가 난다는데 veritesting 옵션을 걸어주면 이 오류를 해결할 수 있습니다.(path group을 이용하여 veritesting을 걸어주려고 했는데 안되더군요 -_-;)



### Solution

```python
import angr
p = angr.Project("r200", load_options={'auto_load_libs': False})
ex = p.surveyors.Explorer(find=(0x400936, ), avoid=(0x400947,), enable_veritesting=True)
ex.run()
print ex.found[0].state.posix.dumps(0)
```

