cell="00010100"
def encryption(filename,rule,newfilename):
    if (rule < 0 or rule > 255):
        return "rule超过范围"
    rule = bin(rule)[2:].zfill(8)
    f1 = open(filename, "rb")
    Plaintext = f1.read()
    f1.close()
    key = []
    key.append(int(cell, 2))
    for i in range(len(Plaintext)):
        new_key = ""
        old_key = bin(key[-1])[2:].zfill(8)
        for i in range(0, len(old_key)):
            tmp = ""
            tmp += old_key[i - 1] + old_key[i]
            if (i == len(old_key) - 1):
                tmp += old_key[0]
            else:
                tmp += old_key[i + 1]
            new_key += str(rule[int(tmp, 2)])
        key.append(int(new_key, 2))
    result = []
    for i, j in zip(Plaintext, key):
        result.append(i ^ j)
    f2 = open(newfilename, "wb")
    f2.write(bytes(result))
    f2.close()
def decryption(filename,rule,newfilename):
    if (rule < 0 or rule > 255):
        return "rule超过范围"
    rule = bin(rule)[2:].zfill(8)
    f1 = open(filename, "rb")
    Plaintext = f1.read()
    f1.close()
    key = []
    key.append(int(cell, 2))
    for i in range(len(Plaintext)):
        new_key = ""
        old_key = bin(key[-1])[2:].zfill(8)
        for i in range(0, len(old_key)):
            tmp = ""
            tmp += old_key[i - 1] + old_key[i]
            if (i == len(old_key) - 1):
                tmp += old_key[0]
            else:
                tmp += old_key[i + 1]
            new_key += str(rule[int(tmp, 2)])
        key.append(int(new_key, 2))
    result = []
    for i, j in zip(Plaintext, key):
        result.append(i ^ j)
    f2 = open(newfilename, "wb")
    f2.write(bytes(result))
    f2.close()

