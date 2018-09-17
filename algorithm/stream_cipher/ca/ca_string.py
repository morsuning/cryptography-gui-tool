cell = "00010100"


def encrypt(Plaintext, rule):
    if(rule<0 or rule>255):
        return "rule超过范围"
    Plaintext=Plaintext.encode('utf-8')
    rule=bin(rule)[2:].zfill(8)
    key=[]
    key.append(int(cell,2))
    for i in range(len(Plaintext)):
        new_key=""
        old_key=bin(key[-1])[2:].zfill(8)
        for i in range(0,len(old_key)):
            tmp=""
            tmp+=old_key[i-1]+old_key[i]
            if(i==len(old_key)-1):
                tmp+=old_key[0]
            else:
                tmp+=old_key[i+1]
            new_key+=str(rule[int(tmp,2)])
        key.append(int(new_key,2))
    result=[]
    for i,j in zip(Plaintext,key):
        result.append(i^j)
    ciphertext="0x"
    for i in result:
        ciphertext+=hex(i)[2:].zfill(2)
    return ciphertext[2:]


def decrypt(ciphertext, rule):
    if (rule < 0 or rule > 255):
        return "rule超过范围"
    rule = bin(rule)[2:].zfill(8)
    if ("0x" in ciphertext):
        ciphertext = ciphertext[2:]
    blk=[]
    i=0
    while(i+2<=len(ciphertext)):
        blk.append(int(ciphertext[i:i + 2], 16))
        i = i + 2
    ciphertext=blk
    key = []
    key.append(int(cell, 2))
    for i in range(len(ciphertext)):
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
    for i, j in zip(ciphertext, key):
        result.append(i ^ j)
    return bytes(result).decode("utf-8")






