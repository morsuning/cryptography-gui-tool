def single_transposition(plaintext, key):  # 单次置换（双重置换由两次单次置换组成）
    col_count = len(key)
    sorted_index = [0 for _ in range(col_count)]
    plain_len = len(plaintext)
    rem = plain_len % col_count
    # 计算行数
    if rem == 0:
        row_count = int(plain_len / col_count)
    else:
        row_count = int(plain_len / col_count) + 1
    matrix = [([0] * col_count) for _ in range(row_count)]
    t = 0  # 矩阵填充游标
    for x in range(row_count):
        for y in range(col_count):
            if t < plain_len:
                matrix[x][y] = plaintext[t]
                t += 1
            else:
                matrix[x][y] = '+'
    # 按密钥字符大小排序得到列序
    for x in range(col_count):
        for y in range(col_count):
            if x == y:
                sorted_index[x] += 1
                continue
            if ord(key[x]) > ord(key[y]):
                sorted_index[x] += 1
            if ord(key[x]) < ord(key[y]):
                continue
            if (ord(key[x]) == ord(key[y])) and (x > y):
                sorted_index[x] += 1
    # 读取按列序排列的密文
    column_buffer = [0 for _ in range(row_count * col_count)]
    t = 0
    for i in range(col_count):
        for j in range(row_count):
            column_buffer[t] = matrix[j][sorted_index[i] - 1]
            t += 1
    ciphertext_str = ''
    for i in range(len(column_buffer)):
        ciphertext_str += str(column_buffer[i])
    return ciphertext_str

def single_transposition_decrypt(ciphertext, key):  # 单次置换解密
    col_count = len(key)
    sorted_index = [0 for _ in range(col_count)]
    plain_len = len(ciphertext)
    rem = plain_len % col_count
    if rem == 0:
        row_count = int(plain_len / col_count)
    else:
        row_count = int(plain_len / col_count) + 1
    # 计算列序
    for x in range(col_count):
        for y in range(col_count):
            if x == y:
                sorted_index[x] += 1
                continue
            if ord(key[x]) > ord(key[y]):
                sorted_index[x] += 1
            if ord(key[x]) < ord(key[y]):
                continue
            if (ord(key[x]) == ord(key[y])) and (x > y):
                sorted_index[x] += 1
    column_buffer = [0 for _ in range(row_count * col_count)]
    for i in range(len(ciphertext)):
        column_buffer[i] = ciphertext[i]
    # 回填矩阵以恢复原列序
    matrix_dec = [([0] * col_count) for _ in range(row_count)]
    t = 0
    for i in range(col_count):
        for j in range(row_count):
            matrix_dec[j][sorted_index[i] - 1] = column_buffer[t]
            t += 1
    plaintext_str = ''
    for i in range(row_count):
        for j in range(col_count):
            plaintext_str += str(matrix_dec[i][j])
    return plaintext_str

def encrypt(plaintext, key1, key2):
    first_pass = single_transposition(plaintext, key1)
    second_pass = single_transposition(first_pass, key2)
    return second_pass

def decrypt(ciphertext, key2, key1):
    first_pass = single_transposition_decrypt(ciphertext, key2)
    t = 0
    lens = len(first_pass)
    for i in range(lens):
        if first_pass[lens - 1 - i] == '0':
            t += 1
        else:
            break
    trimmed = first_pass[0:lens - t]
    second_pass = single_transposition_decrypt(trimmed, key1)
    return second_pass.replace('0', '')

def main():
    print(encrypt("encryptionalgorithms", "dbaasdfc", "abcd"))
    print(decrypt("yatio0gmni0r0en0tlcohprs", "abcd", "dbaasdfc"))

if __name__ == "__main__":
    main()
