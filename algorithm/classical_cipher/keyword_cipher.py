import string

def encrypt(plaintext, ci_key):
    plaintext = list(plaintext.lower())
    ciphertext = list(string.ascii_lowercase)
    ci_key = list(ci_key.lower())
    key = []
    for i in ci_key:
        if i not in key:
            key.append(i)
    for i in ciphertext:
        if i not in key:
            key.append(i)
    all_letter = list(string.ascii_lowercase)
    ciphertext = []
    for i in plaintext:
        for j in range(26):
            if i == all_letter[j]:
                ciphertext.append(key[j])
    return "".join(list(ciphertext)), "".join(list(key))

def decrypt(ciphertext, ci_key):
    str_ciphertext = list(string.ascii_lowercase)
    ci_key = list(ci_key.lower())
    key = []
    for i in ci_key:
        if i not in key:
            key.append(i)
    for i in str_ciphertext:
        if i not in key:
            key.append(i)
    all_letter = string.ascii_lowercase
    plaintext = []
    ciphertext = list(ciphertext)
    for i in ciphertext:
        for j in range(26):
            if i == key[j]:
                plaintext.append(all_letter[j])
    return "".join(list(plaintext))

def main():
    plaintext = input("请输入明文")
    ci_key = input("请输入密匙")
    ciphertext, key = encrypt(plaintext, ci_key)
    plaintext = decrypt(ciphertext, ci_key)
    print("解密结果" + plaintext)

if __name__ == '__main__':
    main()
