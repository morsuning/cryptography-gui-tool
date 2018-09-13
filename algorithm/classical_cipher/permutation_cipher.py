# -*- coding: utf-8 -*-
class PermutationCipher:

        def transpose(self, chunks, order):
                result = ''
                for x in chunks:
                        for pos in order:
                                result += x[pos]
                return result.replace(' ','')

        def msgToChunks(self, msg, key):
                msg = msg.replace(' ', '')
                while len(msg) % len(key) != 0:
                        msg += ' '
                chunks = []
                for i in range(0, len(msg), len(key)):
                        chunks.append(msg[i:i+len(key)])
                return chunks

        def keyToEncrptyOrder(self, key):
                order = [0] * len(key)
                sorted_key = ''.join(sorted(key))
                for i, x in enumerate(key):
                        order[sorted_key.find(x)] = i
                # print(order)
                return order

        def keyToDecrptyOrder(self, key):
                order = [0] * len(key)
                sorted_key = ''.join(sorted(key))
                for i, x in enumerate(key):
                        order[i] = sorted_key.find(x)
                # print(order)
                return order

        def encrypt(self, msg, key):
                msg = msg.replace(' ', '')
                chunks = self.msgToChunks(msg, key)
                order = self.keyToEncrptyOrder(key)
                return self.transpose(chunks, order)

        def decrypt(self, msg, key):
                msg = msg.replace(' ', '')
                chunks = self.msgToChunks(msg, key)
                order = self.keyToDecrptyOrder(key)
                return self.transpose(chunks, order)


def test():
    c = PermutationCipher()
    print(c.encrypt('get the ball', '34152'))
    print(c.decrypt('thgetalebl', '34152'))
