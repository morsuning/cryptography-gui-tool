#!/usr/bin/env python3

def md5(string):
    def encode(s):
        return ''.join([bin(ord(c)).replace('0b', '').zfill(8) for c in s])
    def decode(s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
    plaintext=string
    #链接变量
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476
    bintext=encode(plaintext)
    #print(encrypt(plaintext))
    #print(encrypt(plaintext).__len__())
    t=bintext.__len__()%512
    #print(t)
    houzhui=bin(bintext.__len__())[2:].zfill(64)
    #print(houzhui)
    if t<448:#补齐
        bintext=bintext+'1'
        for i in range(447-t):
            bintext=bintext+'0'
    else:
        bintext=bintext+'1'
        for i in range(959-t):
            bintext=bintext+'0'

    sectext=bintext+houzhui#最终的明文
    #print(sectext)
    #print(sectext.__len__())
    x=sectext.__len__()/512
    M=[[[0] * 1 for _ in range(16) ] for _ in range(int(x))]
    M[0][0][0]=1
    for i in range(int(x)):
        for j in range(16):
            ix=3
            for k in range(1):
                x=sectext[i*512+j*32:i*512+j*32+32]
                y=x[24:32]+x[16:24]+x[8:16]+x[0:8]
                #print(hex(int(y,2)))
                M[i][j][k]=int(y,2)
        #print(M)#初始化完成
    def F(x,y,z):
        return (x&y)|((~x)&z)
    def G(x,y,z):
        return (x&z)|(y&(~z))
    def H(x,y,z):
        return x^y^z
    def I(x,y,z):
        return y^(x|(~z))
    def yiwei(x,z):
        x=x&0xffffffff
        y= bin(x).replace('0b', '')
        #print(y)
        tt=y.__len__()
        #print(tt)
        if tt<32:
            y=y.zfill(32)
            #print(y)
            t = y[z:] + y[:z]
            return int(t, 2)
        else:
            x=y[tt-32:]
            #print(x)
            t=x[z:]+x[:z]
            return int(t,2)
    def FF(a,b,c,d,M,s,t):
        a=b+yiwei((a+F(b,c,d)+M+t),s)
        return a&0xffffffff
    def GG(a,b,c,d,M,s,t):
        a=b+ yiwei((a + G(b, c, d) + M + t), s)
        return a&0xffffffff

    def HH(a, b, c, d, M, s, t):
        a = b + yiwei((a + H(b, c, d) + M + t), s)
        return a&0xffffffff
    def II(a, b, c, d, M, s, t):
        a = b + yiwei((a + I(b, c, d) + M + t), s)
        return a&0xffffffff
    for i in range(int(sectext.__len__()/512)):
        a=A
        b=B
        c=C
        d=D
        #第一轮循环
        a=FF(a, b, c, d, M[i][0][0], 7, 0xd76aa478)
        d=FF(d, a, b, c, M[i][1][0], 12, 0xe8c7b756)
        c=FF(c, d, a, b, M[i][2][0], 17, 0x242070db)
        b=FF(b, c, d, a, M[i][3][0], 22, 0xc1bdceee)
        a=FF(a, b, c, d, M[i][4][0], 7, 0xf57c0faf)
        d=FF(d, a, b, c, M[i][5][0], 12, 0x4787c62a)
        c=FF(c, d, a, b, M[i][6][0], 17, 0xa8304613)
        b=FF(b, c, d, a, M[i][7][0], 22, 0xfd469501)
        a=FF(a, b, c, d, M[i][8][0], 7, 0x698098d8)
        d=FF(d, a, b, c, M[i][9][0], 12, 0x8b44f7af)
        c=FF(c, d, a, b, M[i][10][0], 17, 0xffff5bb1)
        b=FF(b, c, d, a, M[i][11][0], 22, 0x895cd7be)
        a=FF(a, b, c, d, M[i][12][0], 7, 0x6b901122)
        d=FF(d, a, b, c, M[i][13][0], 12, 0xfd987193)
        c=FF(c, d, a, b, M[i][14][0], 17, 0xa679438e)
        b=FF(b, c, d, a, M[i][15][0], 22, 0x49b40821)
        #第二轮循环
        a=GG(a, b, c, d, M[i][1][0], 5, 0xf61e2562)
        d=GG(d, a, b, c, M[i][6][0], 9, 0xc040b340)
        c=GG(c, d, a, b, M[i][11][0], 14, 0x265e5a51)
        b=GG(b, c, d, a, M[i][0][0], 20, 0xe9b6c7aa)
        a=GG(a, b, c, d, M[i][5][0], 5, 0xd62f105d)
        d=GG(d, a, b, c, M[i][10][0], 9, 0x02441453)
        c=GG(c, d, a, b, M[i][15][0], 14, 0xd8a1e681)
        b=GG(b, c, d, a, M[i][4][0], 20, 0xe7d3fbc8)
        a=GG(a, b, c, d, M[i][9][0], 5, 0x21e1cde6)
        d=GG(d, a, b, c, M[i][14][0], 9, 0xc33707d6)
        c=GG(c, d, a, b, M[i][3][0], 14, 0xf4d50d87)
        b=GG(b, c, d, a, M[i][8][0], 20, 0x455a14ed)
        a=GG(a, b, c, d, M[i][13][0], 5, 0xa9e3e905)
        d=GG(d, a, b, c, M[i][2][0], 9, 0xfcefa3f8)
        c=GG(c, d, a, b, M[i][7][0], 14, 0x676f02d9)
        b=GG(b, c, d, a, M[i][12][0], 20, 0x8d2a4c8a)
        #第三轮循环
        a=HH(a, b, c, d, M[i][5][0], 4, 0xfffa3942)
        d=HH(d, a, b, c, M[i][8][0], 11, 0x8771f681)
        c=HH(c, d, a, b, M[i][11][0], 16, 0x6d9d6122)
        b=HH(b, c, d, a, M[i][14][0], 23, 0xfde5380c)
        a=HH(a, b, c, d, M[i][1][0], 4, 0xa4beea44)
        d=HH(d, a, b, c, M[i][4][0], 11, 0x4bdecfa9)
        c=HH(c, d, a, b, M[i][7][0], 16, 0xf6bb4b60)
        b=HH(b, c, d, a, M[i][10][0], 23, 0xbebfbc70)
        a=HH(a, b, c, d, M[i][13][0], 4, 0x289b7ec6)
        d=HH(d, a, b, c, M[i][0][0], 11, 0xeaa127fa)
        c=HH(c, d, a, b, M[i][3][0], 16, 0xd4ef3085)
        b=HH(b, c, d, a, M[i][6][0], 23, 0x04881d05)
        a=HH(a, b, c, d, M[i][9][0], 4, 0xd9d4d039)
        d=HH(d, a, b, c, M[i][12][0], 11, 0xe6db99e5)
        c=HH(c, d, a, b, M[i][15][0], 16, 0x1fa27cf8)
        b=HH(b, c, d, a, M[i][2][0], 23, 0xc4ac5665)

         #第四轮循环
        a=II(a, b, c, d, M[i][0][0], 6, 0xf4292244)
        d=II(d, a, b, c, M[i][7][0], 10, 0x432aff97)
        c=II(c, d, a, b, M[i][14][0], 15, 0xab9423a7)
        b=II(b, c, d, a, M[i][5][0], 21, 0xfc93a039)
        a=II(a, b, c, d, M[i][12][0], 6, 0x655b59c3)
        d=II(d, a, b, c, M[i][3][0], 10, 0x8f0ccc92)
        c=II(c, d, a, b, M[i][10][0], 15, 0xffeff47d)
        b=II(b, c, d, a, M[i][1][0], 21, 0x85845dd1)
        a=II(a, b, c, d, M[i][8][0], 6, 0x6fa87e4f)
        d=II(d, a, b, c, M[i][15][0], 10, 0xfe2ce6e0)
        c=II(c, d, a, b, M[i][6][0], 15, 0xa3014314)
        b=II(b, c, d, a, M[i][13][0], 21, 0x4e0811a1)
        a=II(a, b, c, d, M[i][4][0], 6, 0xf7537e82)
        d=II(d, a, b, c, M[i][11][0], 10, 0xbd3af235)
        c=II(c, d, a, b, M[i][2][0], 15, 0x2ad7d2bb)
        b=II(b, c, d, a, M[i][9][0], 21, 0xeb86d391)
        A=(A+a)& 0xffffffff
        B=(B+b)& 0xffffffff
        C=(C+c)& 0xffffffff
        D=(D+d)& 0xffffffff

        d=(hex(D)[2:])[6:8]+(hex(D)[2:])[4:6]+(hex(D)[2:])[2:4]+(hex(D)[2:])[0:2]
        c=(hex(C)[2:])[6:8]+(hex(C)[2:])[4:6]+(hex(C)[2:])[2:4]+(hex(C)[2:])[0:2]
        b=(hex(B)[2:])[6:8]+(hex(B)[2:])[4:6]+(hex(B)[2:])[2:4]+(hex(B)[2:])[0:2]
        a=(hex(A)[2:])[6:8]+(hex(A)[2:])[4:6]+(hex(A)[2:])[2:4]+(hex(A)[2:])[0:2]
    return a+b+c+d


if __name__ == '__main__':
    xxxx=md5('128778877')
    print(xxxx)




