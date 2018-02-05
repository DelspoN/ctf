# [2017_Inc0gnito] \[Crypto] DES_OFB

 ### Problem

```
$ xxd flag.enc 
00000000: 7e1f c55b 4b62 1ca8 546e 4b20 e388 0340  ~..[Kb..TnK ...@
00000010: a3c5 8178 7f28 dad3 a105 02b8 fa81 a15c  ...x.(.........\
00000020: 32d7 0474 4360 2491 07e9 5946 3963 e4fb  2..tC`$...YF9c..
```

```python
#!/usr/bin/env python

import pyDes
from struct import pack, unpack

def xors(a, b):
    return pack('<Q', unpack('<Q', a)[0] ^ unpack('<Q', b)[0])

# pyDes do not support OFB mode
# so I have to implement myself T_T

class DES_OFB:
    def __init__(self, iv, key):
        self.iv = iv
        self.key = key
    def encrypt(self, data):
        data += '\x00' * (-len(data) % 8)
        ret = ''
        prev = self.iv
        for i in xrange(0, len(data), 8):
            blk = pyDes.des(self.key, pyDes.ECB).encrypt(prev)
            ret += xors(blk, data[i:i+8])
            prev = blk
        return ret

# I want to be sure that my precious file is not corrupted!!

legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_0123456789'

with open('flag', 'rb') as f:
    flag = f.read()
    for ch in flag:
        assert ch in legal

# iv and key are same as plaintext, but anyway it's secret
# so I think it's absolutely safe :p

k = DES_OFB(flag[:8], flag[:8])

with open('flag.enc', 'wb') as f:
    f.write(k.encrypt(flag))
```

encrypt된 플래그 파일이 하나 주어지고 encrypt 소스코드가 주어졌습니다. DES_OFB 방식으로 암호화되는데, 이는 암호화/복호화 함수가 동일합니다. 위 소스코드를 보면 알 수 있듯이 8바이트 단위로 암호화되며, iv와 key값은 같습니다. 맨 앞의 8바이트가 iv와 key로 사용되는 것을 확인할 수 있습니다.



### Solution

우리는 플래그가 `INC0{...}` 형식인 것을 알고 있습니다. 따라서 맨 앞의 5바이트는 `INC0{`일 것입니다. 브포로 뒤의 3바이트만 맞추면 됩니다.

```python
#!/usr/bin/env python

import pyDes
from struct import pack, unpack

def xors(a, b):
    return pack('<Q', unpack('<Q', a)[0] ^ unpack('<Q', b)[0])

# pyDes do not support OFB mode
# so I have to implement myself T_T

class DES_OFB:
    def __init__(self, iv, key):
        self.iv = iv
        self.key = key
    def encrypt(self, data):
        data += '\x00' * (-len(data) % 8)
        ret = ''
        prev = self.iv
        for i in xrange(0, len(data), 8):
            blk = pyDes.des(self.key, pyDes.ECB).encrypt(prev)
            ret += xors(blk, data[i:i+8])
            prev = blk
        return ret

# I want to be sure that my precious file is not corrupted!!

f = open("flag.enc","rb")
encoded = f.read()
f.close()

legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_0123456789'

flag = "INC0{"          # result : INC0{1t_

tmpFlag = flag
for a in range(len(legal)):
    tmpFlag1 = flag + legal[a]
    for b in range(len(legal)):
        tmpFlag2 = tmpFlag1 + legal[b]
        for c in range(len(legal)):
            tmpFlag3 = tmpFlag2 + legal[c]
            k = DES_OFB(tmpFlag3[:8], tmpFlag3[:8])
            if k.encrypt(tmpFlag3) in encoded:
                print tmpFlag3
                exit()
```

주어진 flag.enc 파일의 맨 앞 8바이트를 `INC0{1t_`로 하여 flag를 구했습니다.

```
$ cat flag_complete.enc 
~?[Kb?wAs_jUSt_an_3A5Y_bf___I_was_stupid__T_T}

INC0{1t_wAs_jUSt_an_3A5Y_bf___I_was_stupid__T_T}
```

