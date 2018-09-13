
# from Crypto.PublicKey import ECC
import collections
import random
import func
import sm3

# TODO 支持多种曲线
# TODO 可以以PEM格式导入和导出密钥

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')
# T=(p,a,b,g,n,h)。
# （p为模 用来将曲线离散化如y^2=x^3+ax+b(mod p)此时称曲线在模p后的取值Fp为有限域
# Fp中只有p（p为素数）个元素0,1,2 …… p-2,p-1；
#    Fp 的加法（a+b）法则是 a+b≡c (mod p)；即，(a+c)÷p的余数 和c÷p的余数相同。
#    Fp 的乘法(a×b)法则是  a×b≡c (mod p)；
#    Fp 的除法(a÷b)法则是  a/b≡c (mod p)；即 a×b-1≡c  (mod p)；（b-1也是一个0到p-1之间的整数，但满足b×b-1≡1 (mod p)；具体求法可以参考初等数论，或我的另一篇文章）。
#    Fp 的单位元是1，零元是 0。
# 、a 、b 用来确定一条椭圆曲线，
# g为基点，
# n为点G的阶，
# h 是椭圆曲线上所有点的个数m与n相除的整数部分）
# 这几个参量取值的选择，直接影响了加密的安全性。参量值一般要求满足以下几个条件：
# 1、p 当然越大越安全，但越大，计算速度会变慢，200位左右可以满足一般安全要求；
# 2、p≠n×h；
# 3、pt≠1 (mod n)，1≤t<20；
# 4、4a3+27b2≠0 (mod p)；
# 5、n 为素数；
# 6、h≤4。

# 根据国家密码管理局公告
# （第 21 号）
# 推荐曲线 公式：y^2 = x^3 + ax +b
# 各参数如下
curve = EllipticCurve(
    "sm2p256v1",
    p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF,
    a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC,
    b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93,
    g=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,
       0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0),
    n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123,
    h=1,
)

default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}
standard_public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB818' \
                           '72266C87C018FB4162F5AF347B483E24620207'
standard_private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'


class EccCipher:

    def __init__(self, private_key=standard_private_key, public_key=standard_public_key, ecc_table=default_ecc_table):
        self.private_key = private_key
        self.public_key = public_key
        self.para_len = len(ecc_table['n'])
        self.ecc_table = ecc_table
        self.ecc_a3 = (
            int(ecc_table['a'], base=16) + 3) % int(ecc_table['p'], base=16)

    def inverse_mod(self, k, p):
        """
        求k模p的逆元x(x满足(x * k) % p == 1)k必须非零，p必须是素数
        """
        if k == 0:
            raise ZeroDivisionError('division by zero')

        if k < 0:
            # k ** -1 = p - (-k) ** -1  (mod p)
            return p - self.inverse_mod(-k, p)

        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = p, k

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        gcd, x, y = old_r, old_s, old_t
        assert gcd == 1
        assert (k * x) % p == 1
        return x % p

    # 判断点是否在曲线上
    @staticmethod
    def is_on_curve(point):
        if point is None:
            return True
        x, y = point
        return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0

    # 返回点关于x轴对称的一点 对称映射
    def point_neg(self, point):
        assert self.is_on_curve(point)
        if point is None:
            # -0 = 0
            return None

        x, y = point
        result = (x, -y % curve.p)

        assert self.is_on_curve(result)

        return result

    # 点1和点2相加 根据群论公式
    def point_add(self, point1, point2):
        assert self.is_on_curve(point1)
        assert self.is_on_curve(point2)

        if point1 is None:
            # 0 + point2 = point2
            return point2
        if point2 is None:
            # point1 + 0 = point1
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            # 即关于x轴对称
            return None

        if x1 == x2:
            # 即点1和点2重合时,此时直线为曲线的切线，切线斜率则为
            m = (3 * x1 * x1 + curve.a) * self.inverse_mod(2 * y1, curve.p)
        else:
            # 点1和点2不重合
            # m = (y2 - y1) * (x2 - x1) ^ (-1) mod p; ^(-1)意为逆元
            m = (y1 - y2) * self.inverse_mod(x1 - x2, curve.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % curve.p,
                  -y3 % curve.p)

        assert self.is_on_curve(result)
        return result

    # 做k * 点运算，生成的点还是在曲线上
    def scalar_multiply(self, k, point):
        """
        生成Pa = kG中的Pa
        """
        assert self.is_on_curve(point)

        if k % curve.n == 0 or point is None:
            return None

        if k < 0:
            # k * point = -k * (-point)
            return self.scalar_multiply(-k, self.point_neg(point))

        result = None
        addend = point

        while k:
            if k == 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        assert self.is_on_curve(result)

        return result

    # 生成ECC公钥和私钥
    def make_key_pair(self):
        # 生成随机数K用作私钥 公式 Pa = kG中的k
        private_key = random.randrange(1, curve.n)
        # 计算公钥中的Pa，与G共同组成公钥
        # 传入k和基点G：curve.g
        public_key = self.scalar_multiply(private_key, curve.g)
        return private_key, public_key

    def generate(self):
        return self.make_key_pair()

    def _double_point(self, point):
        """倍点"""
        l = len(point)
        len_2 = 2 * self.para_len
        if l < self.para_len * 2:
            return None
        else:
            x1 = int(point[0:self.para_len], 16)
            y1 = int(point[self.para_len:len_2], 16)
            if l == len_2:
                z1 = 1
            else:
                z1 = int(point[len_2:], 16)

            T6 = (z1 * z1) % int(self.ecc_table['p'], base=16)
            T2 = (y1 * y1) % int(self.ecc_table['p'], base=16)
            T3 = (x1 + T6) % int(self.ecc_table['p'], base=16)
            T4 = (x1 - T6) % int(self.ecc_table['p'], base=16)
            T1 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (y1 * z1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * 8) % int(self.ecc_table['p'], base=16)
            T5 = (x1 * T4) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * 3) % int(self.ecc_table['p'], base=16)
            T6 = (T6 * T6) % int(self.ecc_table['p'], base=16)
            T6 = (self.ecc_a3 * T6) % int(self.ecc_table['p'], base=16)
            T1 = (T1 + T6) % int(self.ecc_table['p'], base=16)
            z3 = (T3 + T3) % int(self.ecc_table['p'], base=16)
            T3 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            x3 = (T3 - T5) % int(self.ecc_table['p'], base=16)

            if (T5 % 2) == 1:
                T4 = (T5 + ((T5 + int(self.ecc_table['p'], base=16)) >> 1) - T3) % int(self.ecc_table['p'], base=16)
            else:
                T4 = (T5 + (T5 >> 1) - T3) % int(self.ecc_table['p'], base=16)

            T1 = (T1 * T4) % int(self.ecc_table['p'], base=16)
            y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)

            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (x3, y3, z3)

    def _add_point(self, P1, P2):
        """点加函数，P2点为仿射坐标即z=1，P1为Jacobian加重射影坐标"""
        len_2 = 2 * self.para_len
        l1 = len(P1)
        l2 = len(P2)
        if (l1 < len_2) or (l2 < len_2):
            return None
        else:
            X1 = int(P1[0:self.para_len], 16)
            Y1 = int(P1[self.para_len:len_2], 16)
            if l1 == len_2:
                Z1 = 1
            else:
                Z1 = int(P1[len_2:], 16)
            x2 = int(P2[0:self.para_len], 16)
            y2 = int(P2[self.para_len:len_2], 16)

            T1 = (Z1 * Z1) % int(self.ecc_table['p'], base=16)
            T2 = (y2 * Z1) % int(self.ecc_table['p'], base=16)
            T3 = (x2 * T1) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T3 - X1) % int(self.ecc_table['p'], base=16)
            T3 = (T3 + X1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * T2) % int(self.ecc_table['p'], base=16)
            T1 = (T1 - Y1) % int(self.ecc_table['p'], base=16)
            Z3 = (Z1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T5 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T4 = (X1 * T4) % int(self.ecc_table['p'], base=16)
            X3 = (T5 - T3) % int(self.ecc_table['p'], base=16)
            T2 = (Y1 * T2) % int(self.ecc_table['p'], base=16)
            T3 = (T4 - X3) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T3) % int(self.ecc_table['p'], base=16)
            Y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)
            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (X3, Y3, Z3)

    def _convert_jacb_to_nor(self, point):
        """Jacobian加重射影坐标转换成仿射坐标"""
        len_2 = 2 * self.para_len
        x = int(point[0:self.para_len], 16)
        y = int(point[self.para_len:len_2], 16)
        z = int(point[len_2:], 16)
        z_inv = pow(z, int(self.ecc_table['p'], base=16) - 2, int(self.ecc_table['p'], base=16))
        z_invSquar = (z_inv * z_inv) % int(self.ecc_table['p'], base=16)
        z_invQube = (z_invSquar * z_inv) % int(self.ecc_table['p'], base=16)
        x_new = (x * z_invSquar) % int(self.ecc_table['p'], base=16)
        y_new = (y * z_invQube) % int(self.ecc_table['p'], base=16)
        z_new = (z * z_inv) % int(self.ecc_table['p'], base=16)
        if z_new == 1:
            form = '%%0%dx' % self.para_len
            form = form * 2
            return form % (x_new, y_new)
        else:
            return None

    def _kg(self, k, point):  # kP运算
        # 末尾加字符1,表示映射到z轴
        point = '%s%s' % (point, '1')
        mask_str = '8'
        for i in range(self.para_len - 1):
            mask_str += '0'
        mask = int(mask_str, 16)
        temp = point
        flag = False
        for n in range(self.para_len * 4):
            if flag:
                temp = self._double_point(temp)
            if (k & mask) != 0:
                if flag:
                    temp = self._add_point(temp, point)
                else:
                    flag = True
                    temp = point
            k = k << 1
        return self._convert_jacb_to_nor(temp)

    def encrypt(self, data):
        # 加密函数，data消息(bytes)
        msg = data.hex()  # 消息转化为16进制字符串
        k = func.random_hex(self.para_len)
        c1 = self._kg(int(k, 16), self.ecc_table['g'])
        xy = self._kg(int(k, 16), self.public_key)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:2 * self.para_len]
        ml = len(msg)
        t = sm3.sm3_kdf(xy.encode('utf8'), ml / 2)
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % ml
            c2 = form % (int(msg, 16) ^ int(t, 16))
            c3 = sm3.sm3_hash([
                i for i in bytes.fromhex('%s%s%s' % (x2, msg, y2))
            ])
            return bytes.fromhex('%s%s%s' % (c1, c3, c2))

    def decrypt(self, data):
        # 解密函数，data密文（bytes）
        data = data.hex()
        len_2 = 2 * self.para_len
        len_3 = len_2 + 64
        c1 = data[0:len_2]
        c3 = data[len_2:len_3]
        c2 = data[len_3:]
        xy = self._kg(int(self.private_key, 16), c1)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:len_2]
        cl = len(c2)
        t = sm3.sm3_kdf(xy.encode('utf8'), cl / 2)
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % cl
            M = form % (int(c2, 16) ^ int(t, 16))
            u = sm3.sm3_hash([
                i for i in bytes.fromhex('%s%s%s' % (x2, M, y2))
            ])
            return bytes.fromhex(M)


def main():
    print('Curve:', curve.name)
    c = EccCipher()
    private_key, public_key = c.make_key_pair()

    print("生成密钥测试:")
    print("私钥d:", private_key)
    print("公钥K(x,y):", public_key)

    print("加密字符串测试:")
    plain_text = input("请输入要加密的字符串(utf-8字符均可):\n")
    cipher_text = c.encrypt(plain_text.encode('utf-8'))
    print("加密后的密文是:", cipher_text)
    print("解密后的结果是:\n", c.decrypt(cipher_text).decode("utf-8"))

    print("加密文件测试:")
    with open("test.rar", 'rb') as f:
        cc = c.encrypt(f.read())
        print("加密后的文件:\n", cc)
    print("解密后的文件:(应为rar格式)")
    print(c.decrypt(cc))

    print("ECDHE测试:")
    alice_private_key, alice_public_key = c.make_key_pair()
    print("Alice's private key:", hex(alice_private_key))
    print("Alice's public key: (0x{:x}, 0x{:x})".format(*alice_public_key))

    bob_private_key, bob_public_key = c.make_key_pair()
    print("Bob's private key:", hex(bob_private_key))
    print("Bob's public key: (0x{:x}, 0x{:x})".format(*bob_public_key))

    s1 = c.scalar_multiply(alice_private_key, bob_public_key)
    s2 = c.scalar_multiply(bob_private_key, alice_public_key)
    assert s1 == s2

    print('Shared secret in Alice: (0x{:x}, 0x{:x})'.format(*s1))
    print('Shared secret in Bob: (0x{:x}, 0x{:x})'.format(*s2))


if __name__ == '__main__':
    main()
