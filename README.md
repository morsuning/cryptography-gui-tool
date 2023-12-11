# cryptography-gui-tool

## 项目简介

一个带有 GUI 界面的密码学工具，可使用密钥对字符串和文件进行加密

未做任何性能优化，加密大于1MB文件会造成界面长时间卡顿

## 功能特性

- 实现了 11 种古典密码、2 种流密码、2 种分组密码、2 种公钥密码、和 1 种哈希算法。可对字符串和文件进行加密和解密。
- 附带 PyQt 实现的 GUI 界面
- 密码库与 GUI 界面代码分离，可以当做单独的密码库使用

具体实现的密码如下

古典密码（可对字符串加解密）

1. 单表替代密码：

* Caesar Cipher
* Keyword Cipher
* Affine Cipher
* Multilateral Cipher

2. 多表替代密码：

* Vigenere Cipher
* Autokey Ciphertext
* Autokey Plaintext

3. 多图替代密码：

* Playfair Cipher

4. 置换密码：

* Permutation Cipher
* Column Permutation Cipher
* Double-Transposition Cipher

流密码（可对字符串和文件加解密）

* RC4
* CA

分组密码（可对字符串和文件加解密）

* DES-64
* AES-64

公钥密码（可生成密钥对，能对字符串和文件加解密）

* RSA
* ECC

哈希算法（可用于字符串和文件）

* MD5

## 环境依赖

仅有PyQt5，见 requirement.txt , 由 pip freeze 释出

## 部署步骤

建议使用 venv 创建 Python 环境，在项目目录下，依次执行

```shell
# 1. 创建虚拟环境
python -m venv .env

# 2. 激活虚拟环境
# cmd
./.env/Scripts/activate.bat

# powshell
./.env/Scripts/Activate.ps1

# linux or MacOS
source ./.env/Scripts/activate
```

在创建好的 Python 环境中，依次运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动程序
python3 main.py
```

## 目录结构描述

.
├── algorithm 密码算法实现
│ ├── block_cipher
│ │ └── aes
│ ├── classical_cipher
│ ├── hash_algorithm
│ ├── public_cipher
│ │ ├── ecc
│ │ └── rsa
│ └── stream_cipher
│ └── ca
├── assets QSS 配置
│ ├── icons
│ ├── python
│ └── qss
├── event GUI 事件绑定
└── ui GUI 界面定义

## 版本内容更新

1.0 更新文档

1.1 更新代码规范

1.2 更新PyQt5版本；去除QSS

## 声明

公开使用该代码请注明作者 morsuning

## 协议

[Mozilla Public License 2.0](https://github.com/6nosis/cryptography-GUItool/blob/master/LICENSE)

[![Stargazers over time](https://starchart.cc/morsuning/cryptography-GUItool.svg)](https://starchart.cc/morsuning/cryptography-GUItool)
