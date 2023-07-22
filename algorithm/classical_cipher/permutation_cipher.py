# -*- coding: utf-8 -*-
def msgToChunks(msg, key):
    msg = msg.replace(' ', '')
    while len(msg) % len(key) != 0:
        msg += ' '
    chunks = []
    for i in range(0, len(msg), len(key)):
        chunks.append(msg[i:i + len(key)])
    return chunks

def transpose(chunks, order):
    result = ''
    for x in chunks:
        for pos in order:
            result += x[pos]
    return result.replace(' ', '')

def keyToEncrptyOrder(key):
    order = [0] * len(key)
    sorted_key = ''.join(sorted(key))
    for i, x in enumerate(key):
        order[sorted_key.find(x)] = i
    # print(order)
    return order

def keyToDecrptyOrder(key):
    order = [0] * len(key)
    sorted_key = ''.join(sorted(key))
    for i, x in enumerate(key):
        order[i] = sorted_key.find(x)
    # print(order)
    return order

def encrypt(msg, key):
    msg = msg.replace(' ', '')
    chunks = msgToChunks(msg, key)
    order = keyToEncrptyOrder(key)
    return transpose(chunks, order)

def decrypt(msg, key):
    msg = msg.replace(' ', '')
    chunks = msgToChunks(msg, key)
    order = keyToDecrptyOrder(key)
    return transpose(chunks, order)

def test():
    print(encrypt('get the ball', '34152'))
    print(decrypt('thgetalebl', '34152'))
