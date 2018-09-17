

def zhihuan(plaintttext,kkkkey):#此为一次置换，不是两次
    plaintext=plaintttext
    key=kkkkey
    lienum = len(key)
    sortmrx = [0 for i in range(lienum)]
    plainnum = len(plaintext)
    i = plainnum % lienum
    if i == 0:  # 确定列数
        hangnum = int(plainnum / lienum)
    if i != 0:
        hangnum = int(plainnum / lienum) + 1
    matrix = [([0] * lienum) for i in range(hangnum)]
    newrix = [([0] * lienum) for i in range(hangnum)]
    t = 0  # t用于循环判断，填充矩阵
    for x in range(hangnum):  # 循环判断，填充矩阵
        for y in range(lienum):
            if t < plainnum:
                matrix[x][y] = plaintext[t]
                t = t + 1
            if t > plainnum:
                matrix[x][y] = '+'
    for x in range(lienum):  # 对密钥的字母大小进行排序
        for y in range(lienum):
            if x == y:
                sortmrx[x] = sortmrx[x] + 1
                continue
            if ord(key[x]) > ord(key[y]):
                sortmrx[x] = sortmrx[x] + 1
            if ord(key[x]) < ord(key[y]):
                continue
            if (ord(key[x]) == ord(key[y])) & (x > y):
                sortmrx[x] = sortmrx[x] + 1
    keymrx = [0 for i in range((hangnum) * lienum)]  # 声明存储加密字符串的数组
    t = 0
    for i in range(lienum):
        for j in range(hangnum):
            keymrx[t] = matrix[j][sortmrx[i] - 1]
            t = t + 1
    t = hangnum * lienum
    xxxxxxxxxx=''
    for i in range(len(keymrx)):  # 打印输出加密
        xxxxxxxxxx=xxxxxxxxxx+str(keymrx[i])

    return xxxxxxxxxx

def jiemi(keytext,key):#此为一次解密，不是两次
    plaintext=keytext
    lienum = len(key)
    sortmrx = [0 for i in range(lienum)]
    plainnum = len(plaintext)
    i = plainnum % lienum
    if i == 0:  # 确定列数
        hangnum = int(plainnum / lienum)
    if i != 0:
        hangnum = int(plainnum / lienum) + 1
    for x in range(lienum):  # 对密钥的字母大小进行排序
        for y in range(lienum):
            if x == y:
                sortmrx[x] = sortmrx[x] + 1
                continue
            if ord(key[x]) > ord(key[y]):
                sortmrx[x] = sortmrx[x] + 1
            if ord(key[x]) < ord(key[y]):
                continue
            if (ord(key[x]) == ord(key[y])) & (x > y):
                sortmrx[x] = sortmrx[x] + 1
    keymrx = [0 for i in range((hangnum) * lienum)]
    for i in range(len(keytext)):
        keymrx[i]=plaintext[i]
    # 解密过程
    nnnrix = [([0] * lienum) for i in range(hangnum)]
    t = 0
    for i in range(lienum):  # 解密步骤
        for j in range(hangnum):
            nnnrix[j][sortmrx[i] - 1] = keymrx[t]
            t = t + 1
    # print('')
    # print("解密结果为：")
    tttttt=''
    for i in range(hangnum):  # 打印输出解密结果
        for j in range(lienum):
            tttttt=tttttt+str(nnnrix[i][j])
            # print(nnnrix[i][j], end='')
            # if j == lienum - 1:
            #     print('')

    return(tttttt)


def encrypt(mingwen, key1, key2):
    xxx=zhihuan(mingwen,key1)
    yyy=zhihuan(xxx,key2)
    return yyy


def decrypt(miwem, key2, key1):
    xxx=jiemi(miwem,key2)
    t=0
    lens=len(xxx)
    for i in range(lens):
        if xxx[lens-1-i]=='0':
            t=t+1
        else:
            break
    xxxx=xxx[0:lens-t]
    yyy=jiemi(xxxx,key1)
    return yyy.replace('0','')


def main():
    # 示例演示的时候，要先加密再加密。不然对应关系不对
    plaintext = "encryptionalgorithms"
    key = 'dbac'
    print(encrypt("encryptionalgorithms", "dbaasdfc", "abcd"))
    print(decrypt("yatio0gmni0r0en0tlcohprs", "abcd", "dbaasdfc"))


if __name__ == "__main__":
    main()
