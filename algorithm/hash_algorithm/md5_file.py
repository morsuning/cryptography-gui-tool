#!/usr/bin/env python3


def md5(filename):
    f1 = open(filename, "rb")
    p = f1.read()
    x = p.__len__()
    plaintext = ""
    for i in range(x):
        plaintext = plaintext + bin(p[i])[2:].zfill(8)
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    bintext = plaintext
    # print(bintext)
    # print(encrypt(plaintext))
    # print(encrypt(plaintext).__len__())
    t = bintext.__len__() % 512
    # print(t)
    houzhui = bin(bintext.__len__())[2:].zfill(64)
    # print(houzhui)
    if t < 448:  # ����
        bintext = bintext + "1"
        for i in range(447 - t):
            bintext = bintext + "0"
    else:
        bintext = bintext + "1"
        for i in range(959 - t):
            bintext = bintext + "0"

    sectext = bintext + houzhui  # ���յ�����
    # print(sectext)
    # print(sectext.__len__())
    x = sectext.__len__() / 512
    M = [[[0] * 1 for _ in range(16)] for _ in range(int(x))]
    M[0][0][0] = 1
    for i in range(int(x)):
        for j in range(16):
            ix = 3
            for k in range(1):
                x = sectext[i * 512 + j * 32 : i * 512 + j * 32 + 32]
                y = x[24:32] + x[16:24] + x[8:16] + x[0:8]
                # print(hex(int(y,2)))
                M[i][j][k] = int(y, 2)
        # print(M)#��ʼ�����

    def F(x, y, z):
        return (x & y) | ((~x) & z)

    def G(x, y, z):
        return (x & z) | (y & (~z))

    def H(x, y, z):
        return x ^ y ^ z

    def I(x, y, z):
        return y ^ (x | (~z))

    def yiwei(x, z):
        x = x & 0xFFFFFFFF
        y = bin(x).replace("0b", "")
        # print(y)
        tt = y.__len__()
        # print(tt)
        if tt < 32:
            y = y.zfill(32)
            # print(y)
            t = y[z:] + y[:z]
            return int(t, 2)
        else:
            x = y[tt - 32 :]
            # print(x)
            t = x[z:] + x[:z]
            return int(t, 2)

    def FF(a, b, c, d, M, s, t):
        a = b + yiwei((a + F(b, c, d) + M + t), s)
        return a & 0xFFFFFFFF

    def GG(a, b, c, d, M, s, t):
        a = b + yiwei((a + G(b, c, d) + M + t), s)
        return a & 0xFFFFFFFF

    def HH(a, b, c, d, M, s, t):
        a = b + yiwei((a + H(b, c, d) + M + t), s)
        return a & 0xFFFFFFFF

    def II(a, b, c, d, M, s, t):
        a = b + yiwei((a + I(b, c, d) + M + t), s)
        return a & 0xFFFFFFFF

    for i in range(int(sectext.__len__() / 512)):
        a = A
        b = B
        c = C
        d = D
        # ��һ��ѭ��
        a = FF(a, b, c, d, M[i][0][0], 7, 0xD76AA478)
        d = FF(d, a, b, c, M[i][1][0], 12, 0xE8C7B756)
        c = FF(c, d, a, b, M[i][2][0], 17, 0x242070DB)
        b = FF(b, c, d, a, M[i][3][0], 22, 0xC1BDCEEE)
        a = FF(a, b, c, d, M[i][4][0], 7, 0xF57C0FAF)
        d = FF(d, a, b, c, M[i][5][0], 12, 0x4787C62A)
        c = FF(c, d, a, b, M[i][6][0], 17, 0xA8304613)
        b = FF(b, c, d, a, M[i][7][0], 22, 0xFD469501)
        a = FF(a, b, c, d, M[i][8][0], 7, 0x698098D8)
        d = FF(d, a, b, c, M[i][9][0], 12, 0x8B44F7AF)
        c = FF(c, d, a, b, M[i][10][0], 17, 0xFFFF5BB1)
        b = FF(b, c, d, a, M[i][11][0], 22, 0x895CD7BE)
        a = FF(a, b, c, d, M[i][12][0], 7, 0x6B901122)
        d = FF(d, a, b, c, M[i][13][0], 12, 0xFD987193)
        c = FF(c, d, a, b, M[i][14][0], 17, 0xA679438E)
        b = FF(b, c, d, a, M[i][15][0], 22, 0x49B40821)
        # �ڶ���ѭ��
        a = GG(a, b, c, d, M[i][1][0], 5, 0xF61E2562)
        d = GG(d, a, b, c, M[i][6][0], 9, 0xC040B340)
        c = GG(c, d, a, b, M[i][11][0], 14, 0x265E5A51)
        b = GG(b, c, d, a, M[i][0][0], 20, 0xE9B6C7AA)
        a = GG(a, b, c, d, M[i][5][0], 5, 0xD62F105D)
        d = GG(d, a, b, c, M[i][10][0], 9, 0x02441453)
        c = GG(c, d, a, b, M[i][15][0], 14, 0xD8A1E681)
        b = GG(b, c, d, a, M[i][4][0], 20, 0xE7D3FBC8)
        a = GG(a, b, c, d, M[i][9][0], 5, 0x21E1CDE6)
        d = GG(d, a, b, c, M[i][14][0], 9, 0xC33707D6)
        c = GG(c, d, a, b, M[i][3][0], 14, 0xF4D50D87)
        b = GG(b, c, d, a, M[i][8][0], 20, 0x455A14ED)
        a = GG(a, b, c, d, M[i][13][0], 5, 0xA9E3E905)
        d = GG(d, a, b, c, M[i][2][0], 9, 0xFCEFA3F8)
        c = GG(c, d, a, b, M[i][7][0], 14, 0x676F02D9)
        b = GG(b, c, d, a, M[i][12][0], 20, 0x8D2A4C8A)
        # ������ѭ��
        a = HH(a, b, c, d, M[i][5][0], 4, 0xFFFA3942)
        d = HH(d, a, b, c, M[i][8][0], 11, 0x8771F681)
        c = HH(c, d, a, b, M[i][11][0], 16, 0x6D9D6122)
        b = HH(b, c, d, a, M[i][14][0], 23, 0xFDE5380C)
        a = HH(a, b, c, d, M[i][1][0], 4, 0xA4BEEA44)
        d = HH(d, a, b, c, M[i][4][0], 11, 0x4BDECFA9)
        c = HH(c, d, a, b, M[i][7][0], 16, 0xF6BB4B60)
        b = HH(b, c, d, a, M[i][10][0], 23, 0xBEBFBC70)
        a = HH(a, b, c, d, M[i][13][0], 4, 0x289B7EC6)
        d = HH(d, a, b, c, M[i][0][0], 11, 0xEAA127FA)
        c = HH(c, d, a, b, M[i][3][0], 16, 0xD4EF3085)
        b = HH(b, c, d, a, M[i][6][0], 23, 0x04881D05)
        a = HH(a, b, c, d, M[i][9][0], 4, 0xD9D4D039)
        d = HH(d, a, b, c, M[i][12][0], 11, 0xE6DB99E5)
        c = HH(c, d, a, b, M[i][15][0], 16, 0x1FA27CF8)
        b = HH(b, c, d, a, M[i][2][0], 23, 0xC4AC5665)

        # ������ѭ��
        a = II(a, b, c, d, M[i][0][0], 6, 0xF4292244)
        d = II(d, a, b, c, M[i][7][0], 10, 0x432AFF97)
        c = II(c, d, a, b, M[i][14][0], 15, 0xAB9423A7)
        b = II(b, c, d, a, M[i][5][0], 21, 0xFC93A039)
        a = II(a, b, c, d, M[i][12][0], 6, 0x655B59C3)
        d = II(d, a, b, c, M[i][3][0], 10, 0x8F0CCC92)
        c = II(c, d, a, b, M[i][10][0], 15, 0xFFEFF47D)
        b = II(b, c, d, a, M[i][1][0], 21, 0x85845DD1)
        a = II(a, b, c, d, M[i][8][0], 6, 0x6FA87E4F)
        d = II(d, a, b, c, M[i][15][0], 10, 0xFE2CE6E0)
        c = II(c, d, a, b, M[i][6][0], 15, 0xA3014314)
        b = II(b, c, d, a, M[i][13][0], 21, 0x4E0811A1)
        a = II(a, b, c, d, M[i][4][0], 6, 0xF7537E82)
        d = II(d, a, b, c, M[i][11][0], 10, 0xBD3AF235)
        c = II(c, d, a, b, M[i][2][0], 15, 0x2AD7D2BB)
        b = II(b, c, d, a, M[i][9][0], 21, 0xEB86D391)
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

        d = (
            (hex(D)[2:])[6:8]
            + (hex(D)[2:])[4:6]
            + (hex(D)[2:])[2:4]
            + (hex(D)[2:])[0:2]
        )
        c = (
            (hex(C)[2:])[6:8]
            + (hex(C)[2:])[4:6]
            + (hex(C)[2:])[2:4]
            + (hex(C)[2:])[0:2]
        )
        b = (
            (hex(B)[2:])[6:8]
            + (hex(B)[2:])[4:6]
            + (hex(B)[2:])[2:4]
            + (hex(B)[2:])[0:2]
        )
        a = (
            (hex(A)[2:])[6:8]
            + (hex(A)[2:])[4:6]
            + (hex(A)[2:])[2:4]
            + (hex(A)[2:])[0:2]
        )

    return a + b + c + d


if __name__ == "__main__":
    # 测试
    x = md5("upload.png")
    print(x)
