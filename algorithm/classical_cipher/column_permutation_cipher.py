#! /usr/bin/env python
# -*- coding:UTF-8 -*-

#获得读取顺序，返回一个读取列号的列表
def getOrder(key):
    result = []
    tmp = []
    for i in key:
        tmp.append(ord(i))
    order = tmp.copy()
    order.sort()
    tmporder = set(order)
    for i in tmporder:
        if order.count(i) == 1:
            result.append(tmp.index(i))
        else:
            uniqueindex = unique_index(tmp,i)
            for j in uniqueindex:
                result.append(j)
    return result

#输入列表和元素，返回列表中和该元素相等的元素的序号的列表
def unique_index(L,e):
    return [i for (i,j) in enumerate(L) if j == e]

#向明文尾部填充字符e
def padding(plaintext,m):
    while len(plaintext) % m != 0:
        plaintext += "e"
    return plaintext

#加密
def encrypt(plaintext, key):
    ciphertext = ""
    m = len(key)
    Plaintext = padding(plaintext, m)
    n = len(Plaintext) // m
    order = getOrder(key)
    for i in order:
        excursion = 0
        for j in range(n):
            ciphertext += Plaintext[i+excursion]
            excursion += m
    return ciphertext

#解密
def decrypt(ciphertext, key):
    plaintext = ""
    m = len(key)
    Ciphertext = padding(ciphertext,m)
    n = len(ciphertext) // m
    order = getOrder(key)
    readorder = []
    for i in range(len(order)):
        readorder.append(order.index(i))
    for i in range(n):
        for j in readorder:
            plaintext += Ciphertext[i+j*n]
    return plaintext

#实验主流程
def main():
    print("-----------------------------------")
    print("-----Column Permutation Cipher-----")
    print("-------------软信1603--------------")
    print("-------------20163754--------------")
    print("--------------薛晨阳---------------")
    print("-----------------------------------")
    plaintext = input("请输入要加密的密文：\n")
    key = input("请输入密钥：\n")
    ciphertext = encrypt(plaintext.replace(" ", ""), key)
    print("加密后的结果是(明文长模密钥长不为零则用e补充)：\n%s" % ciphertext)
    choice = input("请输入d解密：\n")
    if choice == 'd':
        key = input("请输入密钥(如果密钥错误将解出错误的结果)：\n")
        plain = decrypt(ciphertext, key)
        print("原文是(省略所有空格)：\n%s" %plain)
    else:
        print("已退出")
    print("实验结束")

if __name__ == "__main__":
    main()