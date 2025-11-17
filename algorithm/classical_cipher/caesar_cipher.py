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
