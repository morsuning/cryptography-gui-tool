# -*- coding: utf-8 _*_
'''
仿射加密Affine cipher是单码加密法的一种，其明文的每一个字母映射到一个密文字母
其本质是一个线性变换.
本算法中字母表的每一个字母代表一个数字，a = 0, b = 1,....z=25,
仿射加密的秘钥为0-25之间的数字对(a,b),且满足字母表示的数字最大公约数为1，即
GCD(a,26)=1
'''
import string
plaintext_ = string.ascii_lowercase
ciphertext_ = string.ascii_uppercase

def affineCipher(x,a=7,b = 3):
#其中参数x为明文，a和b为秘钥
    pass
    result = ''
#建立字母和数字对照表为A:0,B:1
    for i in x:
        if i.isupper():
            result = result + chr((a*(ord(i)-65)+b)%26+65)
        elif i.islower():
            result = result + chr((a * (ord(i) - 97) + b)%26 + 97)
    return result
def affinejiemi(x):
    result = ''
    # 建立字母和数字对照表为A:0,B:1
    for i in x:
        if i.isupper():
            result = result + chr((-11 * ((ord(i) - 65 - 3)))%26 + 65)
        elif i.islower():
            result = result + chr((-11 * ((ord(i) - 65 - 3)))% 26 + 97)
    return result



#测试
if __name__ == "__main__":
    print("affineCipher加密hot，密文为：",affineCipher("HOT"))
    print("affineCipher解密AXG，明文为：",affinejiemi("AXG"))
