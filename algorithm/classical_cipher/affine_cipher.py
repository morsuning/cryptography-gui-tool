"""
Implementation of the Affine cipher.

The Affine cipher is a monoalphabetic substitution cipher where each letter in
an alphabet is mapped to its numeric equivalent, encrypted using a simple
mathematical function, and converted back to a letter.
"""
import math


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modInverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def encrypt(plaintext: str, key_a: int, key_b: int) -> str:
    """
    Encrypts a string using the Affine cipher.
    E(x) = (ax + b) mod 26
    """
    if math.gcd(key_a, 26) != 1:
        raise ValueError("key_a must be coprime with 26.")

    result = []
    for char in plaintext:
        if "a" <= char <= "z":
            offset = ord("a")
            x = ord(char) - offset
            encrypted_char_code = (key_a * x + key_b) % 26
            result.append(chr(encrypted_char_code + offset))
        elif "A" <= char <= "Z":
            offset = ord("A")
            x = ord(char) - offset
            encrypted_char_code = (key_a * x + key_b) % 26
            result.append(chr(encrypted_char_code + offset))
        else:
            result.append(char)
    return "".join(result)


def decrypt(ciphertext: str, key_a: int, key_b: int) -> str:
    """
    Decrypts a string using the Affine cipher.
    D(y) = a^-1 * (y - b) mod 26
    """
    if math.gcd(key_a, 26) != 1:
        raise ValueError("key_a must be coprime with 26.")

    mod_inv_a = modInverse(key_a, 26)
    result = []
    for char in ciphertext:
        if "a" <= char <= "z":
            offset = ord("a")
            y = ord(char) - offset
            decrypted_char_code = (mod_inv_a * (y - key_b)) % 26
            result.append(chr(decrypted_char_code + offset))
        elif "A" <= char <= "Z":
            offset = ord("A")
            y = ord(char) - offset
            decrypted_char_code = (mod_inv_a * (y - key_b)) % 26
            result.append(chr(decrypted_char_code + offset))
        else:
            result.append(char)
    return "".join(result)


def main():
    """Demonstrates the Affine cipher functions."""
    a = 5
    b = 8
    plaintext = "Affine Cipher Test! 123."

    print(f"Plaintext: {plaintext}")

    try:
        ciphertext = encrypt(plaintext, a, b)
        print(f"Ciphertext: {ciphertext}")

        decrypted_text = decrypt(ciphertext, a, b)
        print(f"Decrypted:  {decrypted_text}")

        assert decrypted_text == plaintext
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
