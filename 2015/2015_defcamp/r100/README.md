# [2015_Defcamp] \[Reversing] r100

Angr를 익혀보기 위해 문제를 풀어봤습니다.![r100_1](/Users/inject/labs/ctf/2015_defcamp/r100/r100_1.png)



```python
import angr

project = angr.Project("./r100", load_options={'auto_load_libs':False})
path_group = project.factory.path_group()
path_group.explore(find=0x400849,avoid=0x400855)

print path_group.found[0].state.posix.dumps(0)
```

도달할 주소("Nice!"을 출력해주는 부분) 피해야할 주소("Incorrect password!"을 출력해주는 부분)을 입력한 후 실행했습니다.

```
root@inj3ct:~/labs/ctf/2015_defcamp/r100# python ex.py
WARNING | 2017-08-11 15:39:03,130 | claripy | Claripy is setting the recursion limit to 15000. If Python segfaults, I am sorry.
Code_Talkers
```

