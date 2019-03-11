# encrypt-decrypt-pyqt5

可以使用常见加密算法对文件或字符串进行加密和解密，GUI使用PyQt5.11.2编写。

**使用Python版本：3.6.5**

运行start.py即可

## TODO 预计1个月内 ——2019.03.11
1.重构前端代码，增强代码可阅读性，拓展性。整理出一套简单的中型PyQt代码开发结构。

2.重构ECC算法，整理成规范的库格式，并实现选择曲线功能。

3.按规范重写工程简介（中文/English）。

---
## 实现以下古典密码对字符串的加密和解密：
1. 单表替代密码：
* Caesar cipher
* Keyword cipher
* Affine cipher
* Multilateral cipher

2. 多表替代密码：
* Vigenere cipher
* Autokey ciphertext
* Autokey plaintext

3. 多图替代密码：
* Playfair cipher

4. 置换密码：
* Permutation cipher
* Column permutation cipher
* Double-Transposition cipher
---
## 实现以下流密码对字符串和文件的加密和解密：
* RC4
* CA
---
## 实现以下分组密码对字符串和文件的加密和解密：
* DES
* AES
---
## 实现以下公钥密码密钥对的生成及对字符串和文件的加密和解密：
* RSA
* ECC
---
## 实现以下哈希算法，可以对字符串及文件操作：
* MD5
