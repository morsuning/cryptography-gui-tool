# 密码学图形界面工具（cryptography-gui-tool）

英文版：[English README](README.md)

> 没有进行性能优化，加密大于1MB的文件可能会导致界面长时间冻结。

## 简介

- 一个基于 PyQt5 的图形化密码学工具，支持字符串与文件的加密、解密，以及 MD5 摘要。
- 算法库与 GUI 解耦，`algorithm` 目录下的实现可单独作为库使用。
- 当前版本未做性能优化，处理大文件时界面可能卡顿；建议用于演示与教学或小型数据。

## 功能特性

- 覆盖 11 种经典密码、2 种流密码、2 种分组密码、2 种公钥密码、1 种哈希算法。
- 同时支持“字符串模式”和“文件模式”的加/解密。
- 提供密钥导入/导出、明文导入、密文导出、密钥显示切换、默认输出路径等实用功能。

### 支持的算法与密钥要求

经典密码（字符串）：

- 凯撒（Caesar）：密钥为整数偏移量。
- 关键词（Keyword）：密钥为字符串关键词。
- 仿射（Affine）：密钥为两个整数 `a b`（用空格分隔），且 `a` 与 26 互素（不可为偶数或 13 的倍数）。
- 多表（Multilateral）：密钥为字符串。
- 维吉尼亚（Vigenere）：密钥为字符串。
- 自动密钥·密文（Autokey Ciphertext）：密钥为字符串；推荐密钥长度大于明文长度。
- 自动密钥·明文（Autokey Plaintext）：密钥为字符串。
- 普莱菲尔（Playfair）：密钥为字符串。
- 置换（Permutation）：密钥为字符串。
- 列置换（Column Permutation）：密钥为字符串；加密前会去除明文中的空格。
- 双重置换（Double-Transposition）：密钥为两个字符串，用一个空格分隔。

流密码（字符串与文件）：

- RC4：密钥为字符串。
- CA：密钥为整数，范围 `0-255`。

分组密码（字符串与文件）：

- DES-64：密钥长度需为 8 个字符。
- AES-64：密钥长度需为 8 个字符（当前实现如此要求）。

公钥密码（字符串与文件）：

- RSA：支持生成密钥对；公钥文件保存为 `rsa_public_key_<随机>.txt`（两行：`e` 与 `n`），私钥（`d`）显示在界面并可导出。
- ECC：支持生成密钥对；公钥文件保存为 `ecc_public_key_<随机>.txt`（两行：椭圆曲线点 `x`、`y`），私钥显示在界面并可导出。

哈希算法：

- MD5：支持对字符串或文件生成 MD5；同一时刻仅能选择其一。

## 运行环境

- Python 3.x
- 依赖见 `requirements.txt`：`pyqt5`、`pyqt5-qt5`、`pyqt5-sip`

## 安装与启动

推荐使用虚拟环境：

```bash
# 1) 创建虚拟环境
python -m venv .env

# 2) 激活虚拟环境
# Windows (cmd)
.\.env\Scripts\activate.bat
# Windows (PowerShell)
.\.env\Scripts\Activate.ps1
# Linux / macOS
source ./.env/bin/activate

# 3) 安装依赖并启动
pip install -r requirements.txt
python3 main.py
```

使用 `uv`（推荐）：

```bash
# 安装（macOS 推荐）
brew install uv
# 或通用脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 运行 GUI 程序（可不激活环境直接运行）
uv run python main.py
```

## 图形界面使用指南

界面布局：

- 左侧为算法分类切换（经典密码、流密码、分组密码、公钥密码、哈希、关于）。
- 右侧包含“有密钥/字符串/文件”等页签和输入框、按钮、状态栏提示。

通用操作：

- 密钥显示：勾选“显示密钥”复选框可切换密钥明文显示与隐藏。
- 明文导入：点击“导入明文”选择 UTF-8 文本文件，内容将填入对应文本框。
- 密文导出：点击“导出密文”选择目标文件，密文将追加写入。
- 文件输入：点击“导入文件”选择待处理文件。
- 输出路径：点击“保存至”选择输出文件；未设置时，程序将自动在输入文件路径后追加后缀并保存：加密为 `.encrypted`，解密为 `.decrypted`。
- 状态信息：操作完成或失败时，底部状态栏会显示提示信息。

示例流程：

- 字符串加密/解密（以 RC4 为例）
  1. 左侧选择“流密码”→“RC4”。
  2. 在密钥输入框填入字符串密钥。
  3. 在明文框输入内容，点击“加密”；密文将显示在右侧框。
  4. 将密文粘贴至密文框，填入相同密钥，点击“解密”可还原明文。
- 文件加密/解密（以 DES 为例）
  1. 左侧选择“分组密码”→“DES”。
  2. 填入 8 位密钥。
  3. 点击“导入文件”选择输入文件；可选“保存至”指定输出。
  4. 点击“加密”或“解密”；未设置输出时将自动以 `.encrypted` 或 `.decrypted` 后缀保存。
- 公钥密码（以 RSA 为例）
  1. 左侧选择“公钥密码”→“RSA”。
  2. 点击“生成密钥对”；公钥写入 `rsa_public_key_<随机>.txt`，私钥显示在界面。
  3. 字符串模式：在明文框输入内容，点击“加密”；解密时在密文框粘贴密文，保持私钥文本框有值即可。
  4. 文件模式：同理选择输入/输出路径后执行加/解密。
- MD5
  1. 在“哈希”页签下，输入字符串或选择文件（同一时刻仅能选其一）。
  2. 点击“生成 MD5”，结果显示在界面。

注意事项：

- 大文件性能：加密/解密 >1MB 的文件可能导致界面长时间冻结。
- 文本编码：明文文件需为 UTF-8 文本；导入非文本或其他编码将提示失败。
- 密钥规范：
  - DES/AES：8 位密钥。
  - CA：整数 0-255。
  - 仿射：`a b` 且 `a` 与 26 互素。
  - 双重置换：两个密钥以空格分隔。

## 目录结构

```
.
├── algorithm            # 密码算法实现（可单独作为库使用）
│   ├── block_cipher
│   │   └── aes
│   ├── classical_cipher
│   ├── hash_algorithm
│   ├── public_cipher
│   │   ├── ecc
│   │   └── rsa
│   └── stream_cipher
│       └── ca
├── assets               # 图标与（可选）QSS 样式
│   ├── icons
│   ├── python
│   └── qss
├── event                # GUI 事件绑定与操作流程
├── ui                   # GUI 界面定义
├── test_file            # 示例/测试文件
├── main.py              # 程序入口
├── requirements.txt     # 依赖清单
└── pyproject.toml       # 项目配置（可选）
```

## 开发者用法（不依赖 GUI）

你可以直接调用 `algorithm` 目录下的实现：

```python
# RC4 字符串加/解密
from algorithm.stream_cipher.rc4_cipher import RC4
cipher = RC4()
c = cipher.encrypt('key', 'plaintext')
p = cipher.decrypt('key', c)

# DES 文件加/解密
from algorithm.block_cipher import des_cipher
desc = des_cipher.DESCipher()
desc.new('12345678')
desc.encrypt_file('input.txt', 'output.encrypted')
desc.decrypt_file('output.encrypted', 'output.decrypted')

# AES 字符串加/解密
from algorithm.block_cipher.aes import aes_string
c = aes_string.encrypt('hello world', '12345678')
p = aes_string.decrypt(c, '12345678')

# MD5
from algorithm.hash_algorithm import md5_string, md5_file
md5_s = md5_string.md5('hello')
md5_f = md5_file.md5('path/to/file')
```

## 常见问题（FAQ）

- 加密/解密无响应：确认已选择算法分类，并正确填写密钥与输入内容/文件路径。
- 密钥长度错误：分组密码（DES/AES）需 8 位密钥，否则状态栏会提示错误。
- CA 密钥范围：必须是整数且在 0-255 之间。
- 文本导入失败：确保导入的是 UTF-8 文本文件；二进制文件请使用“文件模式”。

## 版本与致谢

- 版本记录：见提交历史与仓库说明。
- 若公开使用此项目，请注明作者：morsuning。

## 许可证

[Mozilla Public License 2.0](https://github.com/morsuning/cryptography-GUItool/blob/master/LICENSE)

[![Stargazers over time](https://starchart.cc/morsuning/cryptography-GUItool.svg)](https://starchart.cc/morsuning/cryptography-GUItool)