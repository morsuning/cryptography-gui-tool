# -*- coding: utf-8 _*_
'''维吉尼亚密码使用一个字符串作为密钥，
字符串中的每一个字符都作为移位替换密码的密钥并确定一个替换表
在通常的Vigenere密码中，替换表由26个英文字母组成，
为周期循环,每个表相对前一个表发生一次左移,构成一个26*26的方阵，输入秘钥后
1.用秘钥依次替代明文
2.找出秘钥（假设此时秘钥为字符m）和明文相交处的字符，即为加密后的密文

'''
#########################Vigenere密码#########################

letter_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 字母表


# 根据输入的key生成key列表
def Get_KeyList(key):
    key_list = []
    for ch in key:
        key_list.append(ord(ch.upper()) - 65)
    return key_list


# 加密函数
def Encrypt(plaintext, key_list):
    ciphertext = ""

    i = 0
    for ch in plaintext:  # 遍历明文
        if 0 == i % len(key_list):
            i = 0
        if ch.isalpha():  # 明文是否为字母,如果是,则判断大小写,分别进行加密
            if ch.isupper():
                ciphertext += letter_list[(ord(ch) - 65 + key_list[i]) % 26]
                i += 1
            else:
                ciphertext += letter_list[(ord(ch) - 97 + key_list[i]) % 26].lower()
                i += 1
        else:  # 如果密文不为字母,直接添加到密文字符串里
            ciphertext += ch
    return ciphertext


# 解密函数
def Decrypt(ciphertext, key):
    plaintext = ""

    i = 0
    for ch in ciphertext:  # 遍历密文
        if 0 == i % len(key_list):
            i = 0
        if ch.isalpha():  # 密文为否为字母,如果是,则判断大小写,分别进行解密
            if ch.isupper():
                plaintext += letter_list[(ord(ch) - 65 - key_list[i]) % 26]
                i += 1
            else:
                plaintext += letter_list[(ord(ch) - 97 - key_list[i]) % 26].lower()
                i += 1
        else:  # 如果密文不为字母,直接添加到明文字符串里
            plaintext += ch
    return plaintext


if __name__ == '__main__':
    print("加密请按D,解密请按E:")
    user_input = input();
    while (user_input != 'D' and user_input != 'E'):  # 输入合法性判断
        print("输入有误!请重新输入:")
        user_input = input()

    print("请输入密钥:")
    key = input()
    while (False == key.isalpha()):  # 输入合法性判断
        print("输入有误!密钥为字母,请重新输入:")
        key = input()

    key_list = Get_KeyList(key)

    if user_input == 'D':
        # 加密
        print("请输入明文:")
        plaintext = input()
        ciphertext = Encrypt(plaintext, key_list)
        print("密文为:\n%s" % ciphertext)
    else:
        # 解密
        print("请输入密文:")
        ciphertext = input()
        plaintext = Decrypt(ciphertext, key_list)
        print("明文为:\n%s" % plaintext)
