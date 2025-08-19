# -*- coding: utf-8 _*_
"""
Implementation of the Caesar cipher.

The Caesar cipher is a simple substitution cipher where each letter in the
plaintext is shifted a certain number of places down or up the alphabet.
"""


def _process_text(text: str, key: int, mode: str) -> str:
    """
    Encrypts or decrypts a string using the Caesar cipher.

    Args:
        text: The input string to process.
        key: The shift value.
        mode: 'encrypt' or 'decrypt'.

    Returns:
        The processed string.
    """
    if mode == "decrypt":
        key = -key

    result = []
    for char in text:
        if "a" <= char <= "z":
            shifted = ord("a") + (ord(char) - ord("a") + key) % 26
            result.append(chr(shifted))
        elif "A" <= char <= "Z":
            shifted = ord("A") + (ord(char) - ord("A") + key) % 26
            result.append(chr(shifted))
        else:
            result.append(char)
    return "".join(result)


def caesar_encrypt(plaintext: str, key: int = 3) -> str:
    """
    Encrypts a string using the Caesar cipher.

    Args:
        plaintext: The string to encrypt.
        key: The shift value (default is 3).

    Returns:
        The encrypted string.
    """
    return _process_text(plaintext, key, "encrypt")


def caesar_decrypt(ciphertext: str, key: int = 3) -> str:
    """
    Decrypts a string using the Caesar cipher.

    Args:
        ciphertext: The string to decrypt.
        key: The shift value (default is 3).

    Returns:
        The decrypted string.
    """
    return _process_text(ciphertext, key, "decrypt")


def main():
    """Demonstrates the Caesar cipher functions."""
    plaintext = "Hello, World! 123"
    key = 4
    encrypted = caesar_encrypt(plaintext, key)
    decrypted = caesar_decrypt(encrypted, key)

    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")


if __name__ == "__main__":
    main()
