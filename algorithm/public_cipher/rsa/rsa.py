from os import urandom  # 系统随机的字符
import binascii  # 二进制和ASCII之间转换

flag = False
# ===========================================
def Mod_1(x, n):
    '''取模负1的算法:计算x2= x^-1 (mod n)的值，
r = gcd(a, b) = ia + jb, x与n是互素数'''
    x0 = x
    y0 = n
    x1 = 0
    y1 = 1
    x2 = 1
    y2 = 0
    while n != 0:
        q = x // n
        (x, n) = (n, x % n)
        (x1, x2) = ((x2 - (q * x1)), x1)
        (y1, y2) = ((y2 - (q * y1)), y1)
    if x2 < 0:
        x2 += y0
    if y2 < 0:
        y2 += x0
    return x2

# ===========================================
def Fast_Mod(a, p, m):
    '''快速取模指数算法:计算 (a ^ p) % m 的值，可用pow()代替'''
    a, p, m = int(a), int(p), int(m)
    if (p == 0):
        return 1
    r = a % m
    k = 1
    while (p > 1):
        if ((p & 1) != 0):
            k = (k * r) % m
        r = (r * r) % m
        p >>= 1
    return (r * k) % m

# ===========================================
def randint(n):
    '''random是伪随机数，需要更高安全的随机数产生，
所以使用os.urandom()或者SystmeRandom模块，
生成n字节的随机数（8位/字节）,返回16进制转为10进制整数返回'''
    randomdata = urandom(n)
    return int(binascii.hexlify(randomdata), 16)

# ===========================================
def primality_testing_1(n):
    '''测试一，小素数测试，用100以内的小素数检测随机数x，
可以很大概率排除不是素数,#创建有25个素数的元组'''
    Sushubiao = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41
                 , 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    for y in Sushubiao:
        if n % y == 0:
            return False
    return True

# ===========================================
def primality_testing_2(n, k):
    '''测试二,用miller_rabin算法对n进行k次检测'''
    if n < 2:
        return False
    d = n - 1
    r = 0
    while not (d & 1):
        r += 1
        d >>= 1
    for _ in range(k):
        a = randint(120)  # 随机数
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
        if x == 1:
            return False
        if x == n - 1:
            break
    else:
        return False
    return True

# ===========================================
def getprime(byte):
    while True:
        n = randint(byte)
        if primality_testing_1(n):
            if primality_testing_2(n, 10):
                pass
            else:
                continue
        else:
            continue
        return n

# ===========================================
def RSA():
    global flag
    message = []
    ciphertext = []
    plaintext = []
    while not flag:
        message=[]
        ciphertext=[]
        plaintext=[]
        p = getprime(32)  # 1024bit的大整数
        q = getprime(32)
        while p == q:  # 避免p/q值相同
            q = getprime(1)
        n = p * q  # n值公开
        OrLa = (p - 1) * (q - 1)  # 欧拉函数
        e = 524289
        '''e取e=524289时，其二进制为10000000000000000001'''
        d = Mod_1(e, OrLa)
        # print('公钥为（{0},{1}）;\n私钥为（{2},{3}）'.format(n, e, n, d))
        message = 'theKingOfNight'
        # 从标准输入输出流接收数据，数字化再加解密
        message = list(map(ord, message))
        # print('ciphertext数字化:', message)
        ciphertext = []
        for x in message:
            ciphertext.append(pow(x, e, n))
        # print('ciphertext加密：', ciphertext)
        message = ciphertext
        plaintext = []
        for x in message:
            plaintext.append(pow(x, d, n))
        # print('plaintext解密：', plaintext)
        if int(plaintext[0])<=256:
            flag=True

    #print('公钥为（{0},{1}）;\n私钥为（{2},{3}）'.format(n, e, n, d))
    #print("p:"+str(p))
    #print("q:"+str(q))
    return e,n,d

# ===================================================
def encrypt(e, n, message):
    temp=''
    #message = input("输入需要加密的密文")
    # 从标准输入输出流接收数据，数字化再加解密
    message = list(map(ord, message))
    #print('ciphertext数字化:', message)
    ciphertext = []
    for x in message:
        ciphertext.append(pow(x, e, n))
    for x in ciphertext:
        temp=temp+','+str(x)

    temp=temp[1:]
    #print(temp)
    return temp

def decrypt(d, n, ciphertext):
    message = []
    plaintext = []
    temp=''

    message = ciphertext.split(',')
    for x in message:
        plaintext.append(pow(int(x), d, n))
    #print('plaintext解密：', plaintext)
    plaintext = list(map(chr, plaintext))
    #print('plaintext字符化：', plaintext)
    for i in plaintext:
        temp=temp+str(i)
    return temp

def encode_file(e,n,file_name, encrypted_file_name):
    encrpt_file = 'encrpt'
    #file_name = input("输入当前路径的文件")
    # 文件后缀名检测
    decrpt_file_name = file_name.split('.')[1]
    #
    message = []
    plaintext = []
    ciphertext = []
    with open(file_name, 'rb') as origin_file:
        # TODO Wrong Here
        for x in origin_file.read():
            # print(int(x))
            message.append(int(x))
    for x in message:
        # print(x)
        ciphertext.append(pow(int(x), e, n))
    # 写入加密文件
    f = open(encrypted_file_name, 'w')
    for x in ciphertext:
        f.write(str(x) + '\r')
    f.close()
    return encrpt_file+'.'+file_name.split('.')[1]


def decode_file(d, n, encode_file, decrypt_file_name=''):
    plaintext=[]
    decrpt_file = 'decrpt'
    # 文件后缀名检测
    decrpt_file_name = encode_file.split('.')[1]
    with open(encode_file) as f:
        for x in f.readlines():
            plaintext.append(pow(int(x), d, n))
    f = open(decrypt_file_name, 'wb')
    f.write(bytes(plaintext))
    f.close()


def main():
    e, n, d = RSA()
    print(e)
    print(n)
    print(d)
    # public key e,n
    # private key d
    # encode_file(e,n,file_name)
    cipher_text = encrypt(e, n, "1234567")
    print(cipher_text)
    print(decrypt(d, n, cipher_text))
    # decode_file(d,n,decode_file())


if __name__ == '__main__':
    main()
