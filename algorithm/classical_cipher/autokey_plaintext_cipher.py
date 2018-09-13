def encrypt(plainText, key):
    alphabet = [chr(65 + x) for x in range(26)]
    cipherTable = []
    count1 = 0
    for x in range(26):
        row = alphabet[count1:] + alphabet[:count1]
        cipherTable.append(row)
        count1 += 1
    plainTextList = [x.upper() for x in plainText if
                     (ord(x) >= ord("a") and ord(x) <= ord("z")) or (ord(x) >= ord("A") and ord(x) <= ord("Z"))]
    keyList = [x.upper() for x in key]
    count2 = 0

    cipherTextList, cipherTextPartList = [], []
    for x in plainTextList:
        cipherTextPartList.append(cipherTable[ord(keyList[count2]) - ord("A")][ord(x) - ord("A")])

        count2 += 1
        if count2 == len(keyList):
            for y in cipherTextPartList:
                cipherTextList.append(y)
            keyList = [x for x in cipherTextPartList]
            cipherTextPartList = []
            count2 = 0

    if count2 != 0:
        for x in cipherTextPartList:
            cipherTextList.append(x)
    else:
        pass
    cipherText = ""
    for x in cipherTextList:
        cipherText += x
    return cipherText


def decrypt(cipherText, key):
    alphabet = [chr(65 + x) for x in range(26)]
    cipherTable = []
    count1 = 0
    for x in range(26):
        row = alphabet[count1:] + alphabet[:count1]
        cipherTable.append(row)
        count1 += 1

    keyList = [x.upper() for x in key]
    cipherTextList = [x.upper() for x in cipherText]
    cipherTextList.reverse()
    keyList.reverse()
    plainTextList, count2 = [], 0

    for x in range(len(cipherTextList)):
        plainTextList.append(
            chr((cipherTable[ord(cipherTextList[x + len(keyList)]) - ord("A")].index(cipherTextList[x])) + ord("A")))
        count2 += 1
        if count2 >= len(cipherTextList) - len(keyList):
            break

    for x, y in zip(keyList, cipherTextList[len(cipherTextList) - len(keyList):]):
        plainTextList.append(chr(cipherTable[ord(x) - ord("A")].index(y) + ord("A")))
    plainTextList.reverse()

    plainText = ""
    for x in plainTextList:
        plainText += x
    return plainText


def main():
    plaintext = "hello"
    key = "eii"
    ciphertext = encrypt(plaintext,key)
    print(ciphertext)
    print(decrypt(ciphertext,key))

if __name__ == "__main__":
    main()