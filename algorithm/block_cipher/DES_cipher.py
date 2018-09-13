# -*- coding: utf-8 -*-

'''
常量部分：
IP置换表 逆IP置换表
S盒中的8个盒(substitution box)
P盒(permutation box)
压缩置换表1-PC1 压缩置换表2-PC2
拓展置换表E(expansion box)
'''
#IP置换表
IP = [
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7
]

#逆IP置换表
rIP = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
]

#S盒1-8
S1 = [
    14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
    0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
    4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
    15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
]
S2 = [
    15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
    3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
    0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
    13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
]
S3 = [
    10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
    13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
    13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
    1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
]
S4 = [
    7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
    13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
    10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
    3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
]
S5 = [
    2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
    14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
    4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
    11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
]
S6 = [
    12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
    10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
    9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
    4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
]
S7 = [
    4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
    13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
    1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
    6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
]
S8 = [
    13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
    1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
    7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
    2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
]
S = [S1,S2,S3,S4,S5,S6,S7,S8]

#P盒
P = [
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

#压缩置换表PC1
PC1 = [
    57, 49, 41, 33, 25, 17,  9,
    1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

#压缩置换表PC2
PC2 = [
    14, 17, 11, 24,  1,  5,
    3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

#拓展置换表E
E = [
    32,  1,  2,  3,  4, 5,
    4,  5,  6,  7,  8,  9,
    8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]


class DESCipher():

    def __init__(self):
        self.encrypt_result_hex = 0
        self.encrypted_file_name = ""


    # 表映射,输入长度必须与表大小一致---
    def table_mapping(self, table, input):
        result = ""
        for i in table:
            result += input[i - 1]
        return result

    # 均分成n部分,传入一个字符串，返回包含n项的列表---
    @staticmethod
    def separate(entire, n):
        result = []
        per = len(entire) // n
        if len(entire) % n != 0:
            print("分离错误")
            exit(-1)
        while len(entire) != 0:
            result.append(entire[:per])
            entire = entire[per:]
        return result

    # 合并成一部分,传入包含n个字符串的列表，返回一个字符串---
    @staticmethod
    def merge(list):
        return "".join(i for i in list)

    '''
    对密钥操作部分
    '''

    # 左/右移n位---
    @staticmethod
    def l_or_r_move(stream, n, l_or_r):
        if l_or_r == "L":
            if n > len(stream) - 1:
                print("左移错误")
                exit(-1)
            tmp = stream[:n]
            stream = stream[n:]
            result = stream + tmp
        else:
            if n > len(stream) - 1:
                print("右移错误")
                exit(-1)
            tmp = stream[-n:]
            stream = stream[:-n]
            result = tmp + stream
        return result

    # PC1压缩置换---
    def PC1change(self, key):
        result = self.table_mapping(PC1, key)
        return result

    # PC2置换---
    def PC2change(self, endkey):
        result = self.table_mapping(PC2, endkey)
        return result

    # 生成密钥1-16---
    def key_generator(self, key):
        Key = []
        initedKey = self.PC1change(key)  # 对key进行PC1置换
        curCandD = self.separate(initedKey, 2)  # 将key拆成2部分
        for i in range(16):
            if i == 0 or i == 1 or i == 8 or i == 15:
                curCandD[0] = self.l_or_r_move(curCandD[0], 1, "L")
                curCandD[1] = self.l_or_r_move(curCandD[1], 1, "L")
                Key.append(self.PC2change(self.merge(curCandD)))
            else:
                curCandD[0] = self.l_or_r_move(curCandD[0], 2, "L")
                curCandD[1] = self.l_or_r_move(curCandD[1], 2, "L")
                Key.append(self.PC2change(self.merge(curCandD)))
        return Key

    # 初始置换IP输入64位明文---
    def init_permutation(self, block_plain_text):
        result = self.table_mapping(IP, block_plain_text)
        return result

    # F函数---
    def func(self, k_per_turn, r_per_turn):
        curR = self.Echange(r_per_turn)
        beforeS = self.xor(curR, k_per_turn)
        toS = self.separate(beforeS, 8)
        for i, item in enumerate(toS):
            toS[i] = self.Schange(item, i)
        tmpResult = self.merge(toS)
        result = self.Pchange(tmpResult)
        return result

    # S置换---
    def Schange(self, str, turn):
        column = int(str[1:5], 2)  # 列
        row = int((str[0] + str[5]), 2)  # 行
        tmpresult = S[turn][row * 16 + column]
        result = bin(int(tmpresult)).replace("0b", "").zfill(4)
        return result

    # P置换---
    def Pchange(self, str):
        result = self.table_mapping(P, str)
        return result

    # 16轮加密---
    def turn_operation(self, str, key, EorD):
        COUNTTURN = 16
        curLandR = self.separate(str, 2)  # 将明文拆成2部分
        Key = self.key_generator(key)
        j = 15
        for i in range(COUNTTURN):
            nextL = curLandR[1]  # 先保存右侧
            if EorD == "E":
                curLandR[1] = self.func(Key[i], curLandR[1])  # 将右侧和k输入f函数
            elif EorD == "D":
                curLandR[1] = self.func(Key[j], curLandR[1])
                j -= 1
            perR = self.xor(curLandR[0], curLandR[1])  # 将新右侧与左侧异或
            curLandR[0] = nextL  # 原右侧为新左侧
            curLandR[1] = perR  # 运算结果为新右侧
        tmpresult = self.changeleftandright(curLandR)  # 16轮结束后，交换左右
        result = self.merge(tmpresult)  # 合并结果
        return result

    # 交换左右---
    def changeleftandright(self, pair):
        tmp = pair[0]
        pair[0] = pair[1]
        pair[1] = tmp
        return pair

    # E置换---
    def Echange(self, tmp):
        result = self.table_mapping(E, tmp)
        return result

    # 末(rIP)置换---
    def reinitpermutation(self, tmp):
        result = self.table_mapping(rIP, tmp)
        return result

    # 异或操作---
    def xor(self, left, right):
        length = len(left)
        if length != len(right):
            print("异或异常")
            exit(-1)
        result = int(left, 2) ^ int(right, 2)
        return bin(result).replace("0b", "").zfill(length)

    # 采用PKCS7标准填充明文：字节对8取余得r，为0补8个"8",不为0补8-r个8-r
    def PKCS7Padding(self, plaintext):
        toPaddinglen = 8 - (len(plaintext) % 8)
        if toPaddinglen == 8:
            result = plaintext
        else:
            result = plaintext + str(toPaddinglen) * toPaddinglen
        return result

    # 将字符串转化为二进制字符串---
    def str2bin(self, str):
        result = ""
        for i in str:
            result += bin(ord(i)).replace('0b', '').zfill(8)
        return result

    # 将二进制字符串转化为字符串---
    def bin2str(self, bin):
        if len(bin) % 8 != 0:
            print("二进制转字符串错误")
            exit(-1)
        result = ""
        while len(bin) != 0:
            result += chr(int(bin[:8], 2))
            bin = bin[8:]
        return result

    # 对明文分组,每组64位---
    def gruoping(self, plaintext):
        result = []
        while len(plaintext) != 0:
            result.append(plaintext[:64])
            plaintext = plaintext[64:]
        return result

    def inputhandle(self, key):
        dic = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        if len(key) != 8:
            return False
        for i in key:
            if i not in dic:
                return False
        return True

    def cryption(self, plaintext, key, EnorDe):
        Plaintext = self.gruoping(plaintext)  # 将明文分组
        cipherText = ""
        KEY = self.str2bin(key)  # 将密钥转为二进制字符串
        for i in Plaintext:  # 对每组加密
            initedPlaintext = self.init_permutation(i)  # IP变换
            tmp = self.turn_operation(initedPlaintext, KEY, EnorDe)  # 16轮加密
            result = self.reinitpermutation(tmp)  # IP逆变换
            Result = self.bin2str(result)
            cipherText += Result
        return cipherText

    def encryption(self, plaintext, key):
        return self.cryption(plaintext, key, "E")

    def decryption(self, ciphertext, key):
        tmp = self.cryption(ciphertext, key, "D")
        delete = tmp[-1]
        if delete in ["1", "2", "3", "4", "5", "6", "7"]:
            return tmp[:-int(delete)]
        else:
            return tmp

    def new(self, key):
        if self.inputhandle(key) == True:
            self.Key = key
        else:
            raise ValueError("密钥输入不符合规范,必须为8位,且为A-Za-z0-9及键盘符号的组合请重新输入")
        return self

    def result_to_hex(self, result_string):
        encrypt_result_hex = ""
        for i in result_string:
            encrypt_result_hex.join(hex(int(bin(ord(i)).replace("0b", ""), 2)).replace("0x", ""))
        return encrypt_result_hex

    def encrypt_string(self, plain_text):
        Plaintext = self.PKCS7Padding(plain_text)
        encrypt_result = self.encryption(self.str2bin(Plaintext), self.Key)
        self.encrypt_result_hex = self.result_to_hex(encrypt_result)
        return encrypt_result

    def decrypt_string(self, cipher_text):
        self.plain = self.decryption(self.str2bin(cipher_text), self.Key)
        return self.plain

    def encrypt_file(self, file_name):
        with open("./" + file_name, 'rb') as r:
            Plaintext = self.PKCS7Padding(str(r.read()))
            encrypt = self.encryption(self.str2bin(Plaintext), self.Key)
        self.encrypted_file_name = "./" + file_name + ".encrypted"
        with open(self.encrypted_file_name, 'wb') as w:
            w.write(encrypt.encode("utf-8"))
        return self.encrypted_file_name

    def decrypt_file(self, file_name):
        with open("./"+file_name, 'r') as r:
            decry = self.decryption(self.str2bin(r.read()), self.Key)
        self.decrypt_file_name = "./"+file_name + ".decrypted"
        with open(self.decrypt_file_name, 'w') as w:
            w.write(decry.strip("b'"))
        return self.decrypt_file_name


def main():
    """Example"""
    des = DESCipher()
    des.new("12345678")
    encrypt_result = des.encrypt_string("abcdef")
    print(encrypt_result)
    decrypt_result = des.decrypt_string(encrypt_result)
    print(decrypt_result)


if __name__ == '__main__':
    main()
