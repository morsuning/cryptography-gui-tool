# 密码学图形界面工具

## 概述

一个带有图形界面的密码学工具，可以使用密钥对字符串和文件进行加密。

没有进行性能优化，加密大于1MB的文件可能会导致界面长时间冻结。

## 功能特性

- 实现了11种经典密码、2种流密码、2种分组密码、2种公钥密码和1种哈希算法。可以对字符串和文件进行加密和解密。
- 包含使用PyQt实现的图形界面。
- 密码学库与GUI代码分离，可以单独作为密码学库使用。

具体实现的密码如下：

### 经典密码（用于字符串加密和解密）

1. **单字母替换密码：**
   * 凯撒密码
   * 关键词密码
   * 仿射密码
   * 多表密码

2. **多字母替换密码：**
   * 维吉尼亚密码
   * 自动密钥密文
   * 自动密钥明文

3. **多字母组密码：**
   * 普莱菲尔密码

4. **置换密码：**
   * 置换密码
   * 列置换密码
   * 双重置换密码

### 流密码（用于字符串和文件的加密和解密）

* RC4
* CA

### 分组密码（用于字符串和文件的加密和解密）

* DES-64
* AES-64

### 公钥密码（可生成密钥对，对字符串和文件进行加密和解密）

* RSA
* ECC

### 哈希算法（用于字符串和文件）

* MD5

## 环境依赖

项目依赖列在 `requirements.txt` 中（PyQt5及相关包）。

## 部署步骤

建议使用 `venv` 创建Python环境。在项目目录中执行以下命令：

```shell
# 1. 创建虚拟环境
python -m venv .env

# 2. 激活虚拟环境
# Windows (cmd)
.\\.env\\Scripts\\activate.bat

# Windows (PowerShell)
.\\.env\\Scripts\\Activate.ps1

# Linux 或 macOS
source ./.env/bin/activate
```

在创建的Python环境中运行以下命令：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动程序
python3 main.py
```

## 使用 uv 安装依赖并运行（推荐）

`uv` 是一个快速的Python包管理与执行工具。你可以选择使用 `uv` 管理虚拟环境与安装依赖，并运行本项目。

### 安装 uv

```bash
# macOS（推荐）
brew install uv

# 或通用安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 使用 uv 创建虚拟环境并安装依赖

```bash
# 在项目根目录创建并启用虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖（读取 requirements.txt）
uv pip install -r requirements.txt
```

### 使用 uv 运行项目

```bash
# 直接运行 GUI 程序
uv run python main.py
```

> 说明：若已通过 `uv pip install -r requirements.txt` 安装依赖，`uv run` 将复用当前虚拟环境；亦可在未激活环境的情况下使用 `uv run` 自动解析并运行。

## 目录结构说明

```
.
├── algorithm  密码算法实现
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
├── event  GUI 事件绑定
└── ui  GUI 界面定义
```

## 版本更新

1.0 文档更新

1.1 代码标准更新

1.2 PyQt5版本更新；移除QSS；测试文件移至单独文件夹

## 免责声明

如果你公开使用此代码，请注明作者 morsuning。

## 许可证

[Mozilla Public License 2.0](https://github.com/morsuning/cryptography-GUItool/blob/master/LICENSE)

[![Stargazers over time](https://starchart.cc/morsuning/cryptography-GUItool.svg)](https://starchart.cc/morsuning/cryptography-GUItool)