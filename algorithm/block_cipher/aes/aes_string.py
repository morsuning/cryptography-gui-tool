# -*- coding: utf-8 -*-
import string


class AESE:
    def __init__(self, blk, key, Nr):
        self.blk = blk
        self.key = key
        self.Nr = Nr
        self.sbox = (
            0x63,
            0x7C,
            0x77,
            0x7B,
            0xF2,
            0x6B,
            0x6F,
            0xC5,
            0x30,
            0x01,
            0x67,
            0x2B,
            0xFE,
            0xD7,
            0xAB,
            0x76,
            0xCA,
            0x82,
            0xC9,
            0x7D,
            0xFA,
            0x59,
            0x47,
            0xF0,
            0xAD,
            0xD4,
            0xA2,
            0xAF,
            0x9C,
            0xA4,
            0x72,
            0xC0,
            0xB7,
            0xFD,
            0x93,
            0x26,
            0x36,
            0x3F,
            0xF7,
            0xCC,
            0x34,
            0xA5,
            0xE5,
            0xF1,
            0x71,
            0xD8,
            0x31,
            0x15,
            0x04,
            0xC7,
            0x23,
            0xC3,
            0x18,
            0x96,
            0x05,
            0x9A,
            0x07,
            0x12,
            0x80,
            0xE2,
            0xEB,
            0x27,
            0xB2,
            0x75,
            0x09,
            0x83,
            0x2C,
            0x1A,
            0x1B,
            0x6E,
            0x5A,
            0xA0,
            0x52,
            0x3B,
            0xD6,
            0xB3,
            0x29,
            0xE3,
            0x2F,
            0x84,
            0x53,
            0xD1,
            0x00,
            0xED,
            0x20,
            0xFC,
            0xB1,
            0x5B,
            0x6A,
            0xCB,
            0xBE,
            0x39,
            0x4A,
            0x4C,
            0x58,
            0xCF,
            0xD0,
            0xEF,
            0xAA,
            0xFB,
            0x43,
            0x4D,
            0x33,
            0x85,
            0x45,
            0xF9,
            0x02,
            0x7F,
            0x50,
            0x3C,
            0x9F,
            0xA8,
            0x51,
            0xA3,
            0x40,
            0x8F,
            0x92,
            0x9D,
            0x38,
            0xF5,
            0xBC,
            0xB6,
            0xDA,
            0x21,
            0x10,
            0xFF,
            0xF3,
            0xD2,
            0xCD,
            0x0C,
            0x13,
            0xEC,
            0x5F,
            0x97,
            0x44,
            0x17,
            0xC4,
            0xA7,
            0x7E,
            0x3D,
            0x64,
            0x5D,
            0x19,
            0x73,
            0x60,
            0x81,
            0x4F,
            0xDC,
            0x22,
            0x2A,
            0x90,
            0x88,
            0x46,
            0xEE,
            0xB8,
            0x14,
            0xDE,
            0x5E,
            0x0B,
            0xDB,
            0xE0,
            0x32,
            0x3A,
            0x0A,
            0x49,
            0x06,
            0x24,
            0x5C,
            0xC2,
            0xD3,
            0xAC,
            0x62,
            0x91,
            0x95,
            0xE4,
            0x79,
            0xE7,
            0xC8,
            0x37,
            0x6D,
            0x8D,
            0xD5,
            0x4E,
            0xA9,
            0x6C,
            0x56,
            0xF4,
            0xEA,
            0x65,
            0x7A,
            0xAE,
            0x08,
            0xBA,
            0x78,
            0x25,
            0x2E,
            0x1C,
            0xA6,
            0xB4,
            0xC6,
            0xE8,
            0xDD,
            0x74,
            0x1F,
            0x4B,
            0xBD,
            0x8B,
            0x8A,
            0x70,
            0x3E,
            0xB5,
            0x66,
            0x48,
            0x03,
            0xF6,
            0x0E,
            0x61,
            0x35,
            0x57,
            0xB9,
            0x86,
            0xC1,
            0x1D,
            0x9E,
            0xE1,
            0xF8,
            0x98,
            0x11,
            0x69,
            0xD9,
            0x8E,
            0x94,
            0x9B,
            0x1E,
            0x87,
            0xE9,
            0xCE,
            0x55,
            0x28,
            0xDF,
            0x8C,
            0xA1,
            0x89,
            0x0D,
            0xBF,
            0xE6,
            0x42,
            0x68,
            0x41,
            0x99,
            0x2D,
            0x0F,
            0xB0,
            0x54,
            0xBB,
            0x16,
        )

    # xtime process
    def xtime(self, x):
        if x & 0x80:
            return ((x << 1) ^ 0x1B) & 0xFF
        return x << 1

    # MixColumns: Process the entire block
    def MixColumns(self):
        tmp = [0 for t in range(4)]
        xt = [0 for q in range(4)]
        n = 0
        for x in range(4):
            xt[0] = self.xtime(self.blk[n])
            xt[1] = self.xtime(self.blk[n + 1])
            xt[2] = self.xtime(self.blk[n + 2])
            xt[3] = self.xtime(self.blk[n + 3])
            tmp[0] = xt[0] ^ xt[1] ^ self.blk[n + 1] ^ self.blk[n + 2] ^ self.blk[n + 3]
            tmp[1] = self.blk[n] ^ xt[1] ^ xt[2] ^ self.blk[n + 2] ^ self.blk[n + 3]
            tmp[2] = self.blk[n] ^ self.blk[n + 1] ^ xt[2] ^ xt[3] ^ self.blk[n + 3]
            tmp[3] = xt[0] ^ self.blk[n] ^ self.blk[n + 1] ^ self.blk[n + 2] ^ xt[3]
            self.blk[n] = tmp[0]
            self.blk[n + 1] = tmp[1]
            self.blk[n + 2] = tmp[2]
            self.blk[n + 3] = tmp[3]
            n = n + 4

    # ShiftRows:Shifts the entire block
    def ShiftRows(self):
        # 2nd row
        t = self.blk[1]
        self.blk[1] = self.blk[5]
        self.blk[5] = self.blk[9]
        self.blk[9] = self.blk[13]
        self.blk[13] = t
        # 3nd row
        t = self.blk[2]
        self.blk[2] = self.blk[10]
        self.blk[10] = t
        t = self.blk[6]
        self.blk[6] = self.blk[14]
        self.blk[14] = t
        # 4nd row
        t = self.blk[15]
        self.blk[15] = self.blk[11]
        self.blk[11] = self.blk[7]
        self.blk[7] = self.blk[3]
        self.blk[3] = t

    # SubBytes
    def SubBytes(self):
        for x in range(16):
            self.blk[x] = self.sbox[self.blk[x]]

    # AddRoundKey
    def AddRoundKey(self, key):
        x = 0
        k = [0 for m in range(16)]
        for c in range(4):
            for r in range(4):
                k[x] = key[r][c]
                x = x + 1
        for y in range(16):
            self.blk[y] ^= int(k[y])

    def show(self):
        for i in range(16):
            print(hex(self.blk[i]))

    # Schedule a secret key for use.
    def ScheduleKey(self, w, Nk):
        Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        for r in range(4):
            for c in range(4):
                w[0][r][c] = self.key[r + c * 4]
        for i in range(1, self.Nr + 1, 1):
            for j in range(Nk):
                t = [0 for x in range(4)]
                for r in range(4):
                    if j:
                        t[r] = w[i][r][j - 1]
                    else:
                        t[r] = w[i - 1][r][3]
                if j == 0:
                    temp = t[0]
                    for r in range(3):
                        t[r] = self.sbox[t[(r + 1) % 4]]
                    t[3] = self.sbox[temp]
                    t[0] ^= int(Rcon[i - 1])
                for r in range(4):
                    w[i][r][j] = w[i - 1][r][j] ^ t[r]

    # 加密函数
    def AesEncrypt(self):
        outkey = []
        outkey = [[[0 for col in range(4)] for row in range(4)] for s in range(11)]
        self.ScheduleKey(outkey, 4)
        self.AddRoundKey(outkey[0])
        for x in range(1, self.Nr, 1):
            self.SubBytes()
            self.ShiftRows()
            self.MixColumns()
            self.AddRoundKey(outkey[x])
        self.SubBytes()
        self.ShiftRows()
        self.AddRoundKey(outkey[10])
        cText = ""
        for i in range(16):
            xxl = hex(self.blk[i])
            if len(xxl) == 3:
                cText += "0" + xxl[2:]
            else:
                cText += xxl[2:]
        return cText


class AESD:
    def __init__(self, blk, key, Nr):
        self.blk = blk
        self.key = key
        self.Nr = Nr
        self.sbox = (
            0x63,
            0x7C,
            0x77,
            0x7B,
            0xF2,
            0x6B,
            0x6F,
            0xC5,
            0x30,
            0x01,
            0x67,
            0x2B,
            0xFE,
            0xD7,
            0xAB,
            0x76,
            0xCA,
            0x82,
            0xC9,
            0x7D,
            0xFA,
            0x59,
            0x47,
            0xF0,
            0xAD,
            0xD4,
            0xA2,
            0xAF,
            0x9C,
            0xA4,
            0x72,
            0xC0,
            0xB7,
            0xFD,
            0x93,
            0x26,
            0x36,
            0x3F,
            0xF7,
            0xCC,
            0x34,
            0xA5,
            0xE5,
            0xF1,
            0x71,
            0xD8,
            0x31,
            0x15,
            0x04,
            0xC7,
            0x23,
            0xC3,
            0x18,
            0x96,
            0x05,
            0x9A,
            0x07,
            0x12,
            0x80,
            0xE2,
            0xEB,
            0x27,
            0xB2,
            0x75,
            0x09,
            0x83,
            0x2C,
            0x1A,
            0x1B,
            0x6E,
            0x5A,
            0xA0,
            0x52,
            0x3B,
            0xD6,
            0xB3,
            0x29,
            0xE3,
            0x2F,
            0x84,
            0x53,
            0xD1,
            0x00,
            0xED,
            0x20,
            0xFC,
            0xB1,
            0x5B,
            0x6A,
            0xCB,
            0xBE,
            0x39,
            0x4A,
            0x4C,
            0x58,
            0xCF,
            0xD0,
            0xEF,
            0xAA,
            0xFB,
            0x43,
            0x4D,
            0x33,
            0x85,
            0x45,
            0xF9,
            0x02,
            0x7F,
            0x50,
            0x3C,
            0x9F,
            0xA8,
            0x51,
            0xA3,
            0x40,
            0x8F,
            0x92,
            0x9D,
            0x38,
            0xF5,
            0xBC,
            0xB6,
            0xDA,
            0x21,
            0x10,
            0xFF,
            0xF3,
            0xD2,
            0xCD,
            0x0C,
            0x13,
            0xEC,
            0x5F,
            0x97,
            0x44,
            0x17,
            0xC4,
            0xA7,
            0x7E,
            0x3D,
            0x64,
            0x5D,
            0x19,
            0x73,
            0x60,
            0x81,
            0x4F,
            0xDC,
            0x22,
            0x2A,
            0x90,
            0x88,
            0x46,
            0xEE,
            0xB8,
            0x14,
            0xDE,
            0x5E,
            0x0B,
            0xDB,
            0xE0,
            0x32,
            0x3A,
            0x0A,
            0x49,
            0x06,
            0x24,
            0x5C,
            0xC2,
            0xD3,
            0xAC,
            0x62,
            0x91,
            0x95,
            0xE4,
            0x79,
            0xE7,
            0xC8,
            0x37,
            0x6D,
            0x8D,
            0xD5,
            0x4E,
            0xA9,
            0x6C,
            0x56,
            0xF4,
            0xEA,
            0x65,
            0x7A,
            0xAE,
            0x08,
            0xBA,
            0x78,
            0x25,
            0x2E,
            0x1C,
            0xA6,
            0xB4,
            0xC6,
            0xE8,
            0xDD,
            0x74,
            0x1F,
            0x4B,
            0xBD,
            0x8B,
            0x8A,
            0x70,
            0x3E,
            0xB5,
            0x66,
            0x48,
            0x03,
            0xF6,
            0x0E,
            0x61,
            0x35,
            0x57,
            0xB9,
            0x86,
            0xC1,
            0x1D,
            0x9E,
            0xE1,
            0xF8,
            0x98,
            0x11,
            0x69,
            0xD9,
            0x8E,
            0x94,
            0x9B,
            0x1E,
            0x87,
            0xE9,
            0xCE,
            0x55,
            0x28,
            0xDF,
            0x8C,
            0xA1,
            0x89,
            0x0D,
            0xBF,
            0xE6,
            0x42,
            0x68,
            0x41,
            0x99,
            0x2D,
            0x0F,
            0xB0,
            0x54,
            0xBB,
            0x16,
        )

    def xtime(self, x):
        if x & 0x80:
            return ((x << 1) ^ 0x1B) & 0xFF
        return x << 1

    def ReMixColumns(self):
        tmp = [0 for q in range(4)]
        xt1 = [0 for w in range(4)]
        xt2 = [0 for e in range(4)]
        xt3 = [0 for r in range(4)]
        n = 0
        for x in range(4):
            xt1[0] = self.xtime(self.blk[n])
            xt1[1] = self.xtime(self.blk[n + 1])
            xt1[2] = self.xtime(self.blk[n + 2])
            xt1[3] = self.xtime(self.blk[n + 3])
            xt2[0] = self.xtime(self.xtime(self.blk[n]))
            xt2[1] = self.xtime(self.xtime(self.blk[n + 1]))
            xt2[2] = self.xtime(self.xtime(self.blk[n + 2]))
            xt2[3] = self.xtime(self.xtime(self.blk[n + 3]))
            xt3[0] = self.xtime(self.xtime(self.xtime(self.blk[n])))
            xt3[1] = self.xtime(self.xtime(self.xtime(self.blk[n + 1])))
            xt3[2] = self.xtime(self.xtime(self.xtime(self.blk[n + 2])))
            xt3[3] = self.xtime(self.xtime(self.xtime(self.blk[n + 3])))
            tmp[0] = (
                xt1[0]
                ^ xt2[0]
                ^ xt3[0]
                ^ self.blk[n + 1]
                ^ xt1[1]
                ^ xt3[1]
                ^ self.blk[n + 2]
                ^ xt2[2]
                ^ xt3[2]
                ^ self.blk[n + 3]
                ^ xt3[3]
            )
            tmp[1] = (
                self.blk[n]
                ^ xt3[0]
                ^ xt1[1]
                ^ xt2[1]
                ^ xt3[1]
                ^ self.blk[n + 2]
                ^ xt1[2]
                ^ xt3[2]
                ^ self.blk[n + 3]
                ^ xt2[3]
                ^ xt3[3]
            )
            tmp[2] = (
                self.blk[n]
                ^ xt2[0]
                ^ xt3[0]
                ^ self.blk[n + 1]
                ^ xt3[1]
                ^ xt1[2]
                ^ xt2[2]
                ^ xt3[2]
                ^ self.blk[n + 3]
                ^ xt1[3]
                ^ xt3[3]
            )
            tmp[3] = (
                self.blk[n]
                ^ xt1[0]
                ^ xt3[0]
                ^ self.blk[n + 1]
                ^ xt2[1]
                ^ xt3[1]
                ^ self.blk[n + 2]
                ^ xt3[2]
                ^ xt1[3]
                ^ xt2[3]
                ^ xt3[3]
            )
            self.blk[n] = tmp[0]
            self.blk[n + 1] = tmp[1]
            self.blk[n + 2] = tmp[2]
            self.blk[n + 3] = tmp[3]
            n = n + 4

    def ReShiftRows(self):
        # 2nd row
        t = self.blk[13]
        self.blk[13] = self.blk[9]
        self.blk[9] = self.blk[5]
        self.blk[5] = self.blk[1]
        self.blk[1] = t
        # 3rd row
        t = self.blk[2]
        self.blk[2] = self.blk[10]
        self.blk[10] = t
        t = self.blk[6]
        self.blk[6] = self.blk[14]
        self.blk[14] = t
        # 4th row
        t = self.blk[3]
        self.blk[3] = self.blk[7]
        self.blk[7] = self.blk[11]
        self.blk[11] = self.blk[15]
        self.blk[15] = t

    def ReSubBytes(self):
        for i in range(16):
            for j in range(256):
                if self.sbox[j] == self.blk[i]:
                    self.blk[i] = j
                    break

    def AddRoundKey(self, key):
        x = 0
        k = [0 for m in range(16)]
        for c in range(4):
            for r in range(4):
                k[x] = key[r][c]
                x = x + 1
        for y in range(16):
            self.blk[y] ^= k[y]

    def ScheduleKey(self, w, Nk):
        Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        for r in range(4):
            for c in range(4):
                w[0][r][c] = self.key[r + c * 4]
        for i in range(1, self.Nr + 1, 1):
            for j in range(Nk):
                t = [0 for x in range(4)]
                for r in range(4):
                    if j:
                        t[r] = w[i][r][j - 1]
                    else:
                        t[r] = w[i - 1][r][3]
                if j == 0:
                    temp = t[0]
                    for r in range(3):
                        t[r] = self.sbox[t[(r + 1) % 4]]
                    t[3] = self.sbox[temp]
                    t[0] ^= int(Rcon[i - 1])
                for r in range(4):
                    w[i][r][j] = w[i - 1][r][j] ^ t[r]

    def AesDecrpyt(self):
        outkey = []
        outkey = [[[0 for col in range(4)] for row in range(4)] for s in range(11)]
        self.ScheduleKey(outkey, 4)
        self.AddRoundKey(outkey[10])
        self.ReShiftRows()
        self.ReSubBytes()
        for x in range(self.Nr - 1, 0, -1):
            self.AddRoundKey(outkey[x])
            self.ReMixColumns()
            self.ReShiftRows()
            self.ReSubBytes()
        self.AddRoundKey(outkey[0])
        mText = ""
        for x in range(16):
            mText += chr(self.blk[x])
        return mText.rstrip(chr(0))


def StringToListN(string):
    s = [0 for x in range(16)]
    l = len(string)
    for x in range(l):
        s[x] = int(ord(string[x]))
    return s


def HexToInt(string):
    s = [0 for x in range(16)]
    for i in range(16):
        s[i] = int(string[2 * i : 2 * i + 2], 16)
    return s


def encrypt(plainText, skey):
    cText = ""
    key = StringToListN(skey)
    number = int(len(plainText) / 16)
    if len(plainText) % 16 != 0:
        number = number + 1
    for i in range(0, number):
        blk = StringToListN(plainText[i * 16 : i * 16 + 16])
        a = AESE(blk, key, 10)
        cText = cText + a.AesEncrypt()
    return cText


def decrypt(cText, skey):
    mText = ""
    if len(cText) % 32 != 0:
        print("密文位数错误！")
        exit(0)
    for i in cText:
        if i not in string.digits + string.ascii_letters:
            print("密文格式错误！")
            exit(0)
    key = StringToListN(skey)
    number = int(len(cText) / 32)
    for i in range(0, number):
        rblk = HexToInt(cText[i * 32 : i * 32 + 32])
        b = AESD(rblk, key, 10)
        mText = mText + b.AesDecrpyt()
    return mText
