#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def weiji(plain, kkkkey):
    # plaintext = 'ThisIsThePlaintext'  # 明文
    # key = 'hold'  # 密钥
    plaintext = plain
    key = kkkkey
    matrix = [([0] * 26) for i in range(26)]
    for x in range(26):  # 生成加密的26*26矩阵
        for y in range(26):
            t = 65 + y + x
            if t > 90:
                matrix[x][y] = chr(t - 26)
            if t <= 90:
                matrix[x][y] = chr(t)

    # for x in range(26):  # 矩阵输出
    #     for y in range(26):
    #         print(matrix[x][y], end='')
    #         if y == 25:
    #             print(' ')
    key1 = ''  # 后面的大写密钥
    for x in key:  # 将密钥全部转化为大写
        if ord(x) >= 97:
            x = chr(ord(x) - 32)
        key1 = key1 + x
    # print("明文为：" + plaintext)
    # print("密钥为：" + key1)
    textsize = len(plaintext)  # 明文长度
    keysize = len(key)  # 密钥长度
    pkmat = [([0] * 2) for i in range(textsize)]  # 加密一对一对照矩阵

    keytext = ''
    t = 0  # 用于密钥和明文匹配时循环判断
    for i in range(textsize):
        t = t % keysize
        pkmat[i][0] = plaintext[i]
        pkmat[i][1] = key1[t]
        t = t + 1
    # print("加密一对一矩阵： ", end='')
    # print(pkmat)  # 至此，对照表完成，接下来进行转换
    for i in range(textsize):
        if ord(pkmat[i][0]) >= 97:
            t = ord(pkmat[i][0]) - 97
            x = ord(pkmat[i][1]) - 65
            keytext = keytext + chr(ord(matrix[t][x]) + 32)
        if ord(pkmat[i][0]) < 97:
            t = ord(pkmat[i][0]) - 65
            x = ord(pkmat[i][1]) - 65
            keytext = keytext + chr(ord(matrix[t][x]))
    return keytext


def weijijiemi(miwen, kkkkey):
    len1 = len(miwen)
    len2 = len(kkkkey)
    matrix = [([0] * 26) for i in range(26)]
    for x in range(26):  # 生成加密的26*26矩阵
        for y in range(26):
            t = 65 + y + x
            if t > 90:
                matrix[x][y] = chr(t - 26)
            if t <= 90:
                matrix[x][y] = chr(t)
    key = kkkkey
    keysize = len(key)
    textsize = len(miwen)
    kkmat = [([0] * 2) for i in range(textsize)]  # 解密一对一对照矩阵
    t = 0  # 用于密钥和密文匹配时循环判断
    for i in range(textsize):  # 生成解密一对一矩阵
        t = t % keysize
        kkmat[i][0] = miwen[i]
        kkmat[i][1] = key[t]
        t = t + 1
    pptext = ''
    for i in range(textsize):  # 解密过程，区分大小写的解密
        for x in range(26):
            # print(ord(kkmat[i][1]))
            if ord(kkmat[i][0]) < 97:
                if (ord(kkmat[i][1]) <= 90):
                    y = (ord(kkmat[i][1]) - 65)
                else:
                    y = (ord(kkmat[i][1]) - 97)
                if matrix[y][x] == kkmat[i][0]:
                    pptext = pptext + chr(x + 65)
                    break
            if ord(kkmat[i][0]) >= 97:
                if (ord(kkmat[i][1]) <= 90):
                    y = (ord(kkmat[i][1]) - 65)
                else:
                    y = (ord(kkmat[i][1]) - 97)
                if matrix[y][x] == chr(ord(kkmat[i][0]) - 32):
                    pptext = pptext + chr(x + 97)
                    break
    return pptext


def encrypt(ppplain, kkkey):
    len1 = len(ppplain)
    len2 = len(kkkey)
    key = kkkey + ppplain[0:len1 - len2]
    miwen = weiji(ppplain, key)
    return miwen


def decrypt(ppplain, kkkey):
    len1 = len(ppplain)
    len2 = len(kkkey)
    t = int(len1 / len2)  # 循环次数
    z = len1 % len2
    plaintext = ''
    key = kkkey
    for i in range(t):
        key = weijijiemi(ppplain[i * len2:(i + 1) * len2], key)
        print(key)
        plaintext = plaintext + key
    mmm = weijijiemi(ppplain[len1 - z:len1], key[:z])
    plaintext = plaintext + mmm
    return plaintext


def main():
    # 示例：
    print(encrypt("anautokeycipherprovidedesalongkeyword", "cap"))
    print(decrypt("cnpugoexmmmnjmgwvfkzrzlhwdpgnryregspz", "cap"))


if __name__ == "__main__":
    main()
