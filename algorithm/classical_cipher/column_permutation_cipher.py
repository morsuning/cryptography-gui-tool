class ColumnPermutationCipher:

    def transpose(self, chunks, order):
        result = ''
        for i in range(len(chunks[0])):
            for j in range(len(chunks)):
                result += chunks[order[j]][i]
        return result.replace(' ', '')

    def msgToChunks(self, msg, key):
        msg = msg.replace(' ', '')
        while len(msg) % len(key) != 0:
            msg += ' '
        chunks = []
        # lenBlock = len(msg) // len(key)
        for i in range(0, len(key)):
            chunks.append(msg[i:len(msg):len(key)])
        return chunks

    def keyToOrder(self, key):
        order = []
        sorted_key = ''.join(sorted(key))
        for x in key:
            order.append(sorted_key.find(x))
        return order

    def keyToEncrptyOrder(self, key):
        order = [0] * len(key)
        sorted_key = ''.join(sorted(key))
        for i, x in enumerate(key):
            order[i] = sorted_key.find(x)
        return order

    def keyToDecrptyOrder(self, key):
        order = [0] * len(key)
        sorted_key = ''.join(sorted(key))
        for i, x in enumerate(key):
            order[sorted_key.find(x)] = i
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
    c = ColumnPermutationCipher()
    print(c.encrypt('encryptionalgorithms', 'dbac'))
    print(c.decrypt('rnecipytlnoaiogrshtm', 'dbac'))