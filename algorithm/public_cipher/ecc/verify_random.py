#!/usr/bin/env python3

import collections
import hashlib


class VerificationFailed(Exception):
    pass


EllipticCurve = collections.namedtuple("EllipticCurve", "seed p a b")

# 除了最后一条曲线外，下面所有的曲线都来自于OpenSSL
# 源代码(crypto/ec/ec_curv .c)。最后四个是假曲线
# 没有通过种子验证。

curves = {
    "prime192v1": EllipticCurve(
        seed=0x3045AE6FC8422F64ED579528D38120EAE12196D5,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
        b=0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1,
    ),
    "secp224r1": EllipticCurve(
        seed=0xBD71344799D5C7FCDC45B59FA3B9AB8F6A948BC5,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000001,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFE,
        b=0xB4050A850C04B3ABF54132565044B0B7D7BFD8BA270B39432355FFB4,
    ),
    "secp384r1": EllipticCurve(
        seed=0xA335926AA319A27A1D00896A6773A4827ACDAC73,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC,
        b=0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF,
    ),
    "secp521r1": EllipticCurve(
        seed=0xD09E8800291CB85396CC6717393284AAA0DA64BA,
        p=0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
        a=0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC,
        b=0x0051953EB9618E1C9A1F929A21A0B68540EEA2DA725B99B315F3B8B489918EF109E156193951EC7E937B1652C0BD3BB1BF073573DF883D2C34F1EF451FD46B503F00,
    ),
    "prime192v2": EllipticCurve(
        seed=0x31A92EE2029FD10D901B113E990710F0D21AC6B6,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
        b=0xCC22D6DFB95C6B25E49C0D6364A4E5980C393AA21668D953,
    ),
    "prime192v3": EllipticCurve(
        seed=0xC469684435DEB378C4B65CA9591E2A5763059A2E,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
        b=0x22123DC2395A05CAA7423DAECCC94760A7D462256BD56916,
    ),
    "prime239v1": EllipticCurve(
        seed=0xE43BB460F0B80CC0C0B075798E948060F8321B7D,
        p=0x7FFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFF8000000000007FFFFFFFFFFF,
        a=0x7FFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFF8000000000007FFFFFFFFFFC,
        b=0x6B016C3BDCF18941D0D654921475CA71A9DB2FB27D1D37796185C2942C0A,
    ),
    "prime239v2": EllipticCurve(
        seed=0xE8B4011604095303CA3B8099982BE09FCB9AE616,
        p=0x7FFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFF8000000000007FFFFFFFFFFF,
        a=0x7FFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFF8000000000007FFFFFFFFFFC,
        b=0x617FAB6832576CBBFED50D99F0249C3FEE58B94BA0038C7AE84C8C832F2C,
    ),
    "prime239v3": EllipticCurve(
        seed=0x7D7374168FFE3471B60A857686A19475D3BFA2FF,
        p=0x7FFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFF8000000000007FFFFFFFFFFF,
        a=0x7FFFFFFFFFFFFFFFFFFFFFFF7FFFFFFFFFFF8000000000007FFFFFFFFFFC,
        b=0x255705FA2A306654B1F4CB03D6A750A30C250102D4988717D9BA15AB6D3E,
    ),
    "prime256v1": EllipticCurve(
        seed=0xC49D360886E704936A6678E1139D26B7819F7E90,
        p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
        b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    ),
    "secp112r1": EllipticCurve(
        seed=0x00F50B028E4D696E676875615175290472783FB1,
        p=0xDB7C2ABF62E35E668076BEAD208B,
        a=0xDB7C2ABF62E35E668076BEAD2088,
        b=0x659EF8BA043916EEDE8911702B22,
    ),
    "secp112r2": EllipticCurve(
        seed=0x002757A1114D696E6768756151755316C05E0BD4,
        p=0xDB7C2ABF62E35E668076BEAD208B,
        a=0x6127C24C05F38A0AAAF65C0EF02C,
        b=0x51DEF1815DB5ED74FCC34C85D709,
    ),
    "secp128r1": EllipticCurve(
        seed=0x000E0D4D696E6768756151750CC03A4473D03679,
        p=0xFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFC,
        b=0xE87579C11079F43DD824993C2CEE5ED3,
    ),
    "secp128r2": EllipticCurve(
        seed=0x004D696E67687561517512D8F03431FCE63B88F4,
        p=0xFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFF,
        a=0xD6031998D1B3BBFEBF59CC9BBFF9AEE1,
        b=0x5EEEFCA380D02919DC2C6558BB6D8A5D,
    ),
    "secp160r1": EllipticCurve(
        seed=0x1053CDE42C14D696E67687561517533BF3F83345,
        p=0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFF,
        a=0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFC,
        b=0x001C97BEFC54BD7A8B65ACF89F81D4D4ADC565FA45,
    ),
    "secp160r2": EllipticCurve(
        seed=0xB99B99B099B323E02709A4D696E6768756151751,
        p=0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC73,
        a=0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC70,
        b=0x00B4E134D3FB59EB8BAB57274904664D5AF50388BA,
    ),
    "sm2p256v1": EllipticCurve(
        seed=0xB99B99B099B323E02709A4D696E6768756151751,
        p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF,
        a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC,
        b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93,
    ),
    # This is prime192v1 with a wrong value for seed.
    "wrong192v1": EllipticCurve(
        seed=0x123,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
        b=0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1,
    ),
    # This is prime192v1 with a wrong value for p.
    "wrong192v2": EllipticCurve(
        seed=0x3045AE6FC8422F64ED579528D38120EAE12196D5,
        p=0x123,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
        b=0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1,
    ),
    # This is prime192v1 with a wrong value for a.
    "wrong192v3": EllipticCurve(
        seed=0x3045AE6FC8422F64ED579528D38120EAE12196D5,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
        a=0x123,
        b=0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1,
    ),
    # This is prime192v1 with a wrong value for b.
    "wrong192v4": EllipticCurve(
        seed=0x3045AE6FC8422F64ED579528D38120EAE12196D5,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
        a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
        b=0x123,
    ),
}


def verify_curve(curve):
    """
    Verifies whether the a and b parameters of the given curve were generated
    from the seed.

    Raises a VerificationFailed exception in case the verification fails.
    """
    # What follows is the implementation of the verification algorithm
    # described in "The Elliptic Curve Digital Signature Algorithm (ECDSA)",
    # from Certicom. There just a few difference between the original algorithm
    # and the implementation:
    #
    # * a few variable names have been changed for the sake of clarity;
    # * the document from Certicom allows arbritrary seeds with bit length
    #   >= 160; here we only care about seeds that are exactly 160-bit long.

    if curve.seed.bit_length() > 160:
        raise VerificationFailed("seed too long")

    seed_bytes = curve.seed.to_bytes(length=160 // 8, byteorder="big")

    # Define t, s and v as specified on the document.
    t = curve.p.bit_length()
    s = (t - 1) // 160
    v = t - 160 * s

    # 1. Compute h = SHA-1(seed_bytes) and let c0 denote the bit string of
    #    length v bits obtained by taking the v rightmost bits of h.
    h = hashlib.sha1(seed_bytes).digest()
    h = int.from_bytes(h, byteorder="big")

    c0 = h & ((1 << v) - 1)

    # 2. Let w[0] denote the bit string of length v bits obtained by setting
    #    the leftmost bit of c0 to 0.
    #
    # Note: here we use 160 bit instead of v bits, as required by the document.
    # We do so to make the code easier, and because it does not make any
    # difference (see the step 6).
    w0 = c0 & ((1 << v - 1) - 1)
    w = [w0.to_bytes(length=160 // 8, byteorder="big")]

    # 3. Let z be the integer whose binary expansion is given by 160-bit string
    #    seed_bytes.
    z = curve.seed

    # 4. For i from 1 to s do:
    for i in range(1, s + 1):
        # 4.1 Let s_i be 160-bit string which is the binary expansion of the
        #     integer (z + i) % (2 ** g).
        z_i = (z + i) % (2**160)
        s_i = z_i.to_bytes(length=160 // 8, byteorder="big")

        # 4.2 Compute w_i = SHA-1(s_i).
        w_i = hashlib.sha1(s_i).digest()
        w.append(w_i)

    # 5. Let w be the bit string obtained by concatenating w_0,w_1,...,w_s.
    w = b"".join(w)

    # 6. Let c be the integer whose integer expansion is given by w.
    #
    # On step 2, we said that we used a longer bit length for the first element
    # of w. This is correct because the resulting c does not change: using 160
    # bits instead of v bits is equivalent to add some zeroes to the left of c.
    c = int.from_bytes(w, "big")

    # If b ** 2 * c == a ** 3 (mod p) then accept; otherwise reject.
    if (curve.b * curve.b * c - curve.a * curve.a * curve.a) % curve.p != 0:
        raise VerificationFailed("curve verification failed")


# Check all the curves defined above.
# Should produce the following output:
#
#     prime192v1: ok
#     prime192v2: ok
#     ...
#     secp384r1: ok
#     secp521r1: ok
#     wrong192v1: failed
#     wrong192v2: failed
#     wrong192v3: failed
#     wrong192v4: failed
for name in sorted(curves):
    curve = curves[name]
    print(name, end=": ")
    try:
        verify_curve(curve)
    except VerificationFailed:
        print("failed")
    else:
        print("ok")
