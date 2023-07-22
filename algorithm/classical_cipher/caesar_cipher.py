# -*- coding: utf-8 _*_
'''
Caesar cipher加密算法的实现
凯撒加密(Caesar cipher)是一种简单的消息编码方式,
根据字母表将消息中的每个字母移动常量位k,默认k为3，例如A转换为D
'''

def caesar_encrypt(x, k=3):
    """第一个参数为明文字符串，第二个参数为向后移位的位数"""
    result = ''
    move = k % 26
    for i in x:
        pass
        # 如果是大写
        if i.isupper():
            result = result + chr(65 + (ord(i) + move - 65) % 26)
        elif i.islower():
            result = result + chr(97 + (ord(i) + move - 97) % 26)
    return result

def caesar_decrypt(x, k=3):
    """第一个参数为明文字符串，第二个参数为向后移位的位数"""
    result = ''
    move = k % 26
    for i in x:
        # 如果是大写
        if i.isupper():
            result = result + chr(65 + (ord(i) - move - 65) % 26)
        elif i.islower():
            result = result + chr(97 + (ord(i) - move - 97) % 26)
    return result

def main():
    print('Abcd凯撒加密的密文是：', caesar_encrypt('Abcd', 3))
    print('Defg凯撒加密的明文是：', caesar_decrypt('Defg', 3))

if __name__ == "__main__":
    main()
