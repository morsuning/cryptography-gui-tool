import collections

def encrypt(pla, key):
    pla = pla.lower()
    key = key.lower()
    cip = []
    # 定义好矩阵
    table = [['', key[0], key[1], key[2], key[3], key[4]], [key[0], 'a', 'b', 'c', 'd', 'e'],
             [key[1], 'f', 'g', 'h', 'i', 'k'], [key[2], 'l', 'm', 'n', 'o', 'p'], [key[3], 'q', 'r', 's', 't', 'u'],
             [key[4], 'v', 'w', 'x', 'y', 'z']]
    for k in pla:
        # 当明文中有“j”的时候，当做“i”进行处理
        if k == 'j':
            k = 'i'
        for i in range(1, 6):
            for j in range(1, 6):
                if k == table[i][j] and k != 'j':
                    cip.append(table[i][0])
                    cip.append(table[0][j])
    cipertext = ''.join(cip)
    return cipertext


def decrypt(cip, key):
    # 将密文拆分，两个两个一组存放
    cip = cip.lower()
    key = key.lower()
    temp = key
    cip_res = []
    for i in range(0, len(cip), 2):
        cip_res.append(cip[i:i + 2])
    # 存放密文的所有组合
    key_res = []
    pla = []
    # 去除重复字母
    key = ''.join(collections.OrderedDict.fromkeys(cip))
    for i1 in key:
        for i2 in key:
            for i3 in key:
                for i4 in key:
                    for i5 in key:
                        if i1 not in (i2 + i3 + i4 + i5) and i2 not in (i1 + i3 + i4 + i5) and i3 not in (
                                i1 + i2 + i4 + i5) and i4 not in (i1 + i2 + i3 + i5) and i5 not in (i1 + i2 + i3 + i4):
                            key_res.append(i1 + i2 + i3 + i4 + i5)
    for z in range(len(key_res)):
        key = key_res[z]
        table = [['', key[0], key[1], key[2], key[3], key[4]], [key[0], 'a', 'b', 'c', 'd', 'e'],
                 [key[1], 'f', 'g', 'h', 'i', 'k'], [key[2], 'l', 'm', 'n', 'o', 'p'],
                 [key[3], 'q', 'r', 's', 't', 'u'], [key[4], 'v', 'w', 'x', 'y', 'z']]
        for i in cip_res:
            for j in range(len(table[0])):
                # 记录第一个下标
                if i[0] == table[0][j]:
                    a = j
                # 记录第二个下标
                if i[1] == table[0][j]:
                    b = j
            s = table[a][b]
            pla.append(s)
    j = 0
    for i in range(0, len(pla), len(cip_res)):
        # f.write("秘钥：" + key_res[j] + " ")
        # print(key_res[j])
        flag = ''.join(pla[i:i + len(cip_res)])
        # f.write("明文：" + ''.join(pla[i:i + len(cip_res)]))
        if temp == key_res[j]:
            break
        # f.write('\n')
        j = j + 1
    return flag

def main():
    # 只能有英文
    pla = input("请输入需要加密的字符串：")
    key = input("请输入秘钥：")
    # 密钥只能有5位，英文
    print(encrypt(pla, key))
    cip = input("请输入需要解密的密文：")
    print(decrypt(cip, key))

if __name__ == '__main__':
    main()
