
# -*- coding: utf-8 -*-

# Python3的str没有decode，所以要import codecs
import codecs


class RC4():

	def KSA(self, key):
		# Key Scheduling Algorithm
		len_key = len(key)
		S = list(range(256))
		# S = [0,1,2, ... , 255]
		j = 0
		for i in range(256):
			j = (j + S[i] + key[i % len_key]) % 256
			S[i], S[j] = S[j], S[i]
		return S

	def PRGA(self, S):
		i = 0
		j = 0
		K = []
		while True:
			i = (i + 1) % 256
			j = (j + S[i]) % 256
			S[i], S[j] = S[j], S[i]
			K = S[(S[i] + S[j]) % 256]
			yield K
		# yield语法是为了生成可迭代的容器，因为这里不知道要生成多少K，让第55行来决定

	def get_keystream(self, key):
		S = self.KSA(key)
		return self.PRGA(S)

	def encrypt_logic(self, key, text):
		key = [ord(c) for c in key]
		keystream = self.get_keystream(key)
		res = []
		for c in text:
			val = ("%02X" % (c ^ next(keystream)))
			res.append(val)
		return ''.join(res)

	def encrypt(self, key, plaintext):
		plaintext = [ord(c) for c in plaintext]
		return self.encrypt_logic(key, plaintext)

	def decrypt(self, key, ciphertext):
		ciphertext = codecs.decode(ciphertext, 'hex_codec')
		res = self.encrypt_logic(key, ciphertext)
		return codecs.decode(res, 'hex_codec').decode('utf-8')

	def encrypt_file(self, file_plain, file_ciphered, key):
		with open(file_plain, 'r') as myfile:
			lines = myfile.readlines()
		with open(file_ciphered, 'w') as myfile:
			for plaintext in lines:
				plaintext = [ord(c) for c in plaintext.replace('\n', '')]
				ciphertext = self.encrypt_logic(key, plaintext)
				myfile.write(ciphertext + '\n')

	def decrypt_file(self, file_plain, file_ciphered, key):
		with open(file_ciphered, 'r') as myfile:
			lines = myfile.readlines()
		with open(file_plain, 'w') as myfile:
			for ciphertext in lines:
				ciphertext = codecs.decode(ciphertext.replace('\n', ''), 'hex_codec')
				res = self.encrypt_logic(key, ciphertext)
				decrptedtext = codecs.decode(res, 'hex_codec').decode('utf-8')
				myfile.write(decrptedtext + '\n')


def main():
	rc_instance = RC4()
	key = 'my-rc4-key'
	plaintext = 'An apple a day keeps the doctor away'
	ciphertext = rc_instance.encrypt(key, plaintext)
	print('明文:', plaintext)
	print('加密后的密文:', ciphertext)
	print('重新解密得到的明文:', rc_instance.decrypt(key, ciphertext))
	print('从明文.txt开始加密')
	rc_instance.encrypt_file('明文.txt', '密文.txt', key)
	print('密文.txt生成成功')
	print('从密文.txt开始解密')
	rc_instance.decrypt_file('明文.txt', '密文.txt', key)
	print('明文.txt生成成功')


if __name__ == '__main__':
	main()
