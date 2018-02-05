# [2017_DefCamp] \[Reversing] Working Junks

### Solution

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rax
  __int64 v13; // rax
  __int64 v14; // rax
  __int64 v15; // rax
  char v16; // al
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 v19; // rax
  char v21; // [rsp+Fh] [rbp-1A841h]
  char v22; // [rsp+10h] [rbp-1A840h]
  char v23; // [rsp+30h] [rbp-1A820h]
  char v24; // [rsp+50h] [rbp-1A800h]
  char v25; // [rsp+70h] [rbp-1A7E0h]
  char v26; // [rsp+90h] [rbp-1A7C0h]
  char v27; // [rsp+B0h] [rbp-1A7A0h]
  char v28; // [rsp+D0h] [rbp-1A780h]
  char v29; // [rsp+F0h] [rbp-1A760h]
  char v30; // [rsp+110h] [rbp-1A740h]
  char v31; // [rsp+130h] [rbp-1A720h]
  char v32; // [rsp+150h] [rbp-1A700h]
  char v33; // [rsp+170h] [rbp-1A6E0h]
  char v34; // [rsp+190h] [rbp-1A6C0h]
  char v35; // [rsp+1B0h] [rbp-1A6A0h]
  int v36; // [rsp+1D0h] [rbp-1A680h]
  __int16 v37; // [rsp+1D4h] [rbp-1A67Ch]
  __int64 v38; // [rsp+1E0h] [rbp-1A670h]
  char v39; // [rsp+1E8h] [rbp-1A668h]
  __int64 v40; // [rsp+1F0h] [rbp-1A660h]
  __int16 v41; // [rsp+1F8h] [rbp-1A658h]
  __int64 v42; // [rsp+200h] [rbp-1A650h]
  __int16 v43; // [rsp+208h] [rbp-1A648h]
  __int64 v44; // [rsp+210h] [rbp-1A640h]
  __int16 v45; // [rsp+218h] [rbp-1A638h]
  __int64 v46; // [rsp+220h] [rbp-1A630h]
  __int16 v47; // [rsp+228h] [rbp-1A628h]
  __int64 v48; // [rsp+230h] [rbp-1A620h]
  __int16 v49; // [rsp+238h] [rbp-1A618h]
  __int64 v50; // [rsp+240h] [rbp-1A610h]
  __int16 v51; // [rsp+248h] [rbp-1A608h]
  __int64 v52; // [rsp+250h] [rbp-1A600h]
  __int16 v53; // [rsp+258h] [rbp-1A5F8h]
  char v54[8]; // [rsp+260h] [rbp-1A5F0h]
  char v55[8]; // [rsp+280h] [rbp-1A5D0h]
  __int64 v56; // [rsp+2A0h] [rbp-1A5B0h]
  __int64 v57; // [rsp+2A8h] [rbp-1A5A8h]
  __int64 v58; // [rsp+2B0h] [rbp-1A5A0h]
  __int64 v59; // [rsp+2B8h] [rbp-1A598h]
  __int64 v60; // [rsp+2C0h] [rbp-1A590h]
  int v61; // [rsp+2C8h] [rbp-1A588h]
  char v62[8]; // [rsp+2D0h] [rbp-1A580h]
  char v63[8]; // [rsp+320h] [rbp-1A530h]
  char v64; // [rsp+370h] [rbp-1A4E0h]
  char v65; // [rsp+45F0h] [rbp-16260h]
  char v66; // [rsp+8890h] [rbp-11FC0h]
  char dest; // [rsp+CE60h] [rbp-D9F0h]
  unsigned __int64 v68; // [rsp+1A838h] [rbp-18h]

  v68 = __readfsqword(0x28u);
  memcpy(&dest, a280624ea44e454, 0xD9CFuLL);
  v40 = 4701799037061248344LL;
  v41 = 80;
  v38 = 2896999113894671451LL;
  v39 = 0;
  v42 = 3974782102098501200LL;
  v43 = 125;
  v44 = 5993537119355225380LL;
  v45 = 84;
  v46 = 4696485106490297921LL;
  v47 = 78;
  v48 = 3266047966679812436LL;
  v49 = 84;
  v50 = 4993446652604076869LL;
  v51 = 33;
  v36 = 1210796068;
  v37 = 42;
  std::allocator<char>::allocator(&v21, a280624ea44e454);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(
    &v22,
    "X5O!P%@AP[4PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*",
    &v21);
  std::allocator<char>::~allocator(&v21);
  strcpy(v63, "X5O!P@AP[4PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*");
  strcpy(v55, "Hello!!! Do you know me?");
  strcpy(v62, "My name is EICAR! And I have a big story that no one understands!");
  strcpy(v54, "And this is my code!");
  v56 = 8295758535554264900LL;
  v57 = 8462115404999910766LL;
  v58 = 7575181452902735986LL;
  v59 = 7863396491390885998LL;
  v60 = 7935464881814335073LL;
  v61 = 2192495;
  v3 = strrev(v55);
  v4 = std::operator<<<std::char_traits<char>>(&std::cout, v3);
  std::ostream::operator<<(v4, &std::flush<char,std::char_traits<char>>);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v23);
  std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v23);
  v5 = strrev(v62);
  v6 = std::operator<<<std::char_traits<char>>(&std::cout, v5);
  std::ostream::operator<<(v6, &std::flush<char,std::char_traits<char>>);
  std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v23);
  v7 = strrev(v54);
  v8 = std::operator<<<std::char_traits<char>>(&std::cout, v7);
  std::ostream::operator<<(v8, &std::flush<char,std::char_traits<char>>);
  std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v23);
  v9 = strrev(v63);
  v10 = std::operator<<<std::char_traits<char>>(&std::cout, v9);
  std::ostream::operator<<(v10, &std::flush<char,std::char_traits<char>>);
  v11 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v22);
  std::ostream::operator<<(v11, &std::flush<char,std::char_traits<char>>);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v25, &v22);
  encryptDecrypt((__int64)&v24, (__int64)&v25);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v25);
  v12 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v24);
  std::operator<<<std::char_traits<char>>(v12, "\n");
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v26, &v22);
  encryptDecrypta((__int64)&v27, (__int64)&v26);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(&v24, &v27);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v27);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v26);
  v13 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v24);
  std::operator<<<std::char_traits<char>>(v13, "\n");
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v28, &v22);
  encryptDecryptb((__int64)&v29, (__int64)&v28);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(&v24, &v29);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v29);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v28);
  v14 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v24);
  std::operator<<<std::char_traits<char>>(v14, "\n");
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v30, &v22);
  fail(&v31, &v30);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(&v24, &v31);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v31);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v30);
  v15 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v24);
  std::operator<<<std::char_traits<char>>(v15, "\n");
  v16 = pot();
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(&v24, (unsigned int)v16);
  v17 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v24);
  std::operator<<<std::char_traits<char>>(v17, "\n");
  std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v23);
  v52 = '!!niaaap';
  v53 = 33;
  memcpy(&v65, aPaaa2f7279d461, 0x429BuLL);
  memcpy(&v66, aPaaa5764e24465, 0x45CCuLL);
  memcpy(&v64, aPaaapaaa5764e2, 0x4279uLL);
  std::allocator<char>::allocator(&v21, aPaaapaaa5764e2);
  v18 = strrev(&dest);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v32, v18, &v21);
  encryptDecryptb((__int64)&v33, (__int64)&v32);
  encryptDecrypta((__int64)&v34, (__int64)&v33);
  encryptDecrypt((__int64)&v35, (__int64)&v34);
  v19 = std::operator<<<char,std::char_traits<char>,std::allocator<char>>(&std::cout, &v35);
  std::operator<<<std::char_traits<char>>(v19, "\n");
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v35);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v34);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v33);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v32);
  std::allocator<char>::~allocator(&v21);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v24);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v23);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(&v22);
  return 0;
}
```

소스코드가 길지만 우리가 주의 깊게 보아야 할 부분은 정해져 있습니다.

```c
  encryptDecryptb((__int64)&v33, (__int64)&v32);
  encryptDecrypta((__int64)&v34, (__int64)&v33);
  encryptDecrypt((__int64)&v35, (__int64)&v34);
```

위 함수들은 단순히 xor 연산 기능을 합니다.

```python
def deca(e):
        out = ""
        for i in range(len(e)):
                out += chr(ord(e[i]) ^ 0x58)
        return out

def decb(e):
        out = ""
        for i in range(len(e)):
                out += chr(ord(e[i]) ^ 0x6f)
        return out

def dec(e):
	out = ""
	for i in range(len(e)):
		out += chr(ord(e[i]) ^ 0x4b)
	return out

f = open("encrypted", "r")
enc = f.read()
enc = enc.strip()
f.close()

decrypted = dec(enc)
decrypted = deca(decrypted)
decrypted = decb(decrypted)
print decrypted.decode("hex")

# ./e > encrypted
# Deleting dummy in encrypted
# python sol.py > flag.png
```

암호화 된 데이터를 복호화하면 flag가 적혀있는 png 파일이 나옵니다.

![flag](flag.png)