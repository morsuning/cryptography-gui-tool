#! /usr/bin/env python
# -*- coding:UTF-8 -*-

# 将字母A-Z转化成0-26的数
def str2ascii2mirr26(str):
    if len(str) == 1:
        return ord(str) - 65
    else:
        tmpstr = []
        for i in range(len(str)):
            tmpstr.append(ord(str[i]) - 65)
        return tmpstr


# 将0-26的数转化为字母A-Z
def mirr262str(str):
    tmpstr = ""
    for i in str:
        tmpstr += chr(i + 65)
    return tmpstr


# 转化为大写
def strupper(str):
    s = ""
    s += str
    return s.upper()


# 使得密钥长度和明文一致
def expendkey(key, length):
    if len(key) > length:
        return key[:length]
    elif len(key) == length:
        return key
    else:
        while len(key) < length:
            key += key
        if len(key) != length:
            return key[:length]
        else:
            return key


# 加密
def encrypt(plaintext, key):
    plaintext = strupper(plaintext)
    tmpkey = strupper(key)
    Key = expendkey(tmpkey, len(plaintext))
    tmpciphertext = []
    for index, item in enumerate(plaintext):
        tmpciphertext.append(((str2ascii2mirr26(Key[index]) + str2ascii2mirr26(item)) % 26))
    return mirr262str(tmpciphertext)


# 解密
def decrypt(ciphertext, key):
    tmpkey = strupper(key)
    Key = expendkey(tmpkey, len(ciphertext))
    tmpplaintext = []
    for index, item in enumerate(ciphertext):
        tmpplaintext.append(((str2ascii2mirr26(item) - str2ascii2mirr26(Key[index])) % 26))
    return mirr262str(tmpplaintext)


# 实验主流程
def main():
    print("-------------------------")
    print("-----Vigenère Cipher-----")
    print("-------------------------")
    plaintext = input("请输入要加密的密文：\n")
    key = input("请输入密钥：\n")
    ciphertext = encrypt(plaintext, key)
    print("加密后的结果是：\n%s" % ciphertext)
    choice = input("请输入d解密：\n")
    if choice == 'd':
        key = input("请输入密钥(如果密钥错误将解出错误的结果)：\n")
        plain = decrypt(ciphertext, key)
        print("原文是(全部以小写形式给出)：\n%s" % (plain.lower()))
    else:
        print("已退出")
    print("实验结束")


if __name__ == "__main__":
    main()
