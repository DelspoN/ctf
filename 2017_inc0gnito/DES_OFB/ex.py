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