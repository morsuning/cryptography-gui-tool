def vigenere_encrypt(plaintext, key):
    # 生成 A-Z 的 26×26 维吉尼亚矩阵，用于按行列索引查找替换字符
    matrix = [([0] * 26) for _ in range(26)]
    for x in range(26):
        for y in range(26):
            t = 65 + y + x
            if t > 90:
                matrix[x][y] = chr(t - 26)
            else:
                matrix[x][y] = chr(t)

    # for x in range(26):  # 矩阵输出
    #     for y in range(26):
    #         print(matrix[x][y], end='')
    #         if y == 25:
    #             print(' ')
    uppercase_key = ''  # 将密钥规范为大写形式
    for ch in key:
        if ord(ch) >= 97:
            ch = chr(ord(ch) - 32)
        uppercase_key += ch
    # print("明文为：" + plaintext)
    # print("密钥为：" + key1)
    textsize = len(plaintext)
    keysize = len(key)
    pair_matrix = [([0] * 2) for _ in range(textsize)]  # 明文与密钥逐字符配对

    keytext = ''
    t = 0  # 逐字符配对游标
    for i in range(textsize):
        t = t % keysize
        pair_matrix[i][0] = plaintext[i]
        pair_matrix[i][1] = uppercase_key[t]
        t = t + 1
    # print("加密一对一矩阵： ", end='')
    # print(pkmat)  # 至此，对照表完成，接下来进行转换
    for i in range(textsize):
        if ord(pair_matrix[i][0]) >= 97:  # 明文为小写
            t = ord(pair_matrix[i][0]) - 97
            x = ord(pair_matrix[i][1]) - 65
            keytext += chr(ord(matrix[t][x]) + 32)
        else:  # 明文为大写
            t = ord(pair_matrix[i][0]) - 65
            x = ord(pair_matrix[i][1]) - 65
            keytext += chr(ord(matrix[t][x]))
    return keytext

def vigenere_decrypt(ciphertext, key):
    # 生成 A-Z 的 26×26 维吉尼亚矩阵
    matrix = [([0] * 26) for _ in range(26)]
    for x in range(26):
        for y in range(26):
            t = 65 + y + x
            if t > 90:
                matrix[x][y] = chr(t - 26)
            else:
                matrix[x][y] = chr(t)
    keysize = len(key)
    textsize = len(ciphertext)
    pair_matrix = [([0] * 2) for _ in range(textsize)]  # 密文与密钥逐字符配对
    t = 0  # 逐字符配对游标
    for i in range(textsize):
        t = t % keysize
        pair_matrix[i][0] = ciphertext[i]
        pair_matrix[i][1] = key[t]
        t = t + 1
    plaintext_out = ''
    for i in range(textsize):  # 解密过程，区分大小写
        for x in range(26):
            if ord(pair_matrix[i][0]) < 97:  # 密文为大写
                if ord(pair_matrix[i][1]) <= 90:
                    y = ord(pair_matrix[i][1]) - 65
                else:
                    y = ord(pair_matrix[i][1]) - 97
                if matrix[y][x] == pair_matrix[i][0]:
                    plaintext_out += chr(x + 65)
                    break
            else:  # 密文为小写
                if ord(pair_matrix[i][1]) <= 90:
                    y = ord(pair_matrix[i][1]) - 65
                else:
                    y = ord(pair_matrix[i][1]) - 97
                if matrix[y][x] == chr(ord(pair_matrix[i][0]) - 32):
                    plaintext_out += chr(x + 97)
                    break
    return plaintext_out

def encrypt(plaintext, key):
    # Autokey（密文模式）：扩展密钥为 key + 明文前段，使长度匹配
    len1 = len(plaintext)
    len2 = len(key)
    extended_key = key + plaintext[0:len1 - len2]
    ciphertext = vigenere_encrypt(plaintext, extended_key)
    return ciphertext

def decrypt(ciphertext, key):
    # Autokey（密文模式）解密：分段生成明文并逐步扩展密钥
    len1 = len(ciphertext)
    len2 = len(key)
    t = int(len1 / len2)
    z = len1 % len2
    plaintext = ''
    current_key = key
    for i in range(t):
        current_key = vigenere_decrypt(ciphertext[i * len2:(i + 1) * len2], current_key)
        print(current_key)
        plaintext += current_key
    tail = vigenere_decrypt(ciphertext[len1 - z:len1], current_key[:z])
    plaintext += tail
    return plaintext

def main():
    # 示例：
    print(encrypt("anautokeycipherprovidedesalongkeyword", "cap"))
    print(decrypt("cnpugoexmmmnjmgwvfkzrzlhwdpgnryregspz", "cap"))

if __name__ == "__main__":
    main()
