# Cryptography GUI Tool (cryptography-gui-tool)

Chinese version: [中文文档](README_CN.md)

## Overview

- A PyQt5-based graphical cryptography tool that supports encrypting and decrypting strings and files, plus MD5 digests.
- The algorithm library is decoupled from the GUI. Implementations under `algorithm` can be used as a standalone library.
- No performance optimization at present. Processing large files may freeze the UI. Recommended for demos, teaching, or small data.

## Features

- Covers 11 classical ciphers, 2 stream ciphers, 2 block ciphers, 2 public-key ciphers, and 1 hash algorithm.
- Supports both “String mode” and “File mode” for encryption and decryption.
- Offers key import/export, plaintext import, ciphertext export, key visibility toggle, and default output path convenience.

### Supported Algorithms and Key Requirements

Classical ciphers (string):

- Caesar: key is an integer shift.
- Keyword: key is a keyword string.
- Affine: key is two integers `a b` (space separated); `a` must be coprime to 26 (not even and not a multiple of 13).
- Multilateral: key is a string.
- Vigenere: key is a string.
- Autokey Ciphertext: key is a string; recommended key length greater than plaintext length.
- Autokey Plaintext: key is a string.
- Playfair: key is a string.
- Permutation: key is a string.
- Column Permutation: key is a string; spaces in plaintext are removed before encryption.
- Double-Transposition: key is two strings separated by a single space.

Stream ciphers (string and file):

- RC4: key is a string.
- CA: key is an integer in `0–255`.

Block ciphers (string and file):

- DES-64: key must be 8 characters long.
- AES-64: key must be 8 characters long (per current implementation).

Public-key ciphers (string and file):

- RSA: supports keypair generation; public key is saved as `rsa_public_key_<random>.txt` (two lines: `e` and `n`); private key (`d`) is shown in the UI and can be exported.
- ECC: supports keypair generation; public key is saved as `ecc_public_key_<random>.txt` (two lines: point `x` and `y`); private key is shown in the UI and can be exported.

Hash:

- MD5: supports generating MD5 for either a string or a file; only one can be chosen at a time.

## Environment

- Python 3.x
- Dependencies in `requirements.txt`: `pyqt5`, `pyqt5-qt5`, `pyqt5-sip`

## Installation and Run

Recommended: virtual environment

```bash
# 1) Create venv
python -m venv .env

# 2) Activate
# Windows (cmd)
.\.env\Scripts\activate.bat
# Windows (PowerShell)
.\.env\Scripts\Activate.ps1
# Linux / macOS
source ./.env/bin/activate

# 3) Install and start
pip install -r requirements.txt
python3 main.py
```

Using `uv` (recommended):

```bash
# Install (macOS recommended)
brew install uv
# Or generic script
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install deps
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Run GUI (can run without activating the venv)
uv run python main.py
```

## GUI Usage Guide

Layout:

- Left: algorithm categories (Classical, Stream, Block, Public-key, Hash, About).
- Right: tabs for “with key / string / file”, inputs, buttons, and a status bar.

Common operations:

- Toggle key visibility via the checkbox.
- Import plaintext from a UTF-8 text file.
- Export ciphertext to a chosen file (appended).
- Import input file for file mode.
- Choose output path; if not set, the program will save to the input path with a suffix: `.encrypted` for encryption and `.decrypted` for decryption.
- Watch the status bar for success/error messages.

Example flows:

- String encrypt/decrypt (RC4)
  1. Select “Stream” → “RC4”.
  2. Enter a string key.
  3. Enter plaintext and click “Encrypt”; ciphertext appears on the right.
  4. Paste ciphertext back, use the same key, click “Decrypt” to restore plaintext.
- File encrypt/decrypt (DES)
  1. Select “Block” → “DES”.
  2. Use an 8-character key.
  3. Import the input file; optionally set output path.
  4. Click “Encrypt” or “Decrypt”; without output path, it uses `.encrypted` / `.decrypted` suffixes.
- Public-key (RSA)
  1. Select “Public-key” → “RSA”.
  2. Click “Generate Keypair”; public key saved as `rsa_public_key_<random>.txt`, private key shown.
  3. String mode: encrypt/decrypt within the text panes.
  4. File mode: similar with input/output paths.
- MD5
  1. Provide either a string or a file.
  2. Click “Generate MD5”.

Notes:

- Large files: >1MB may freeze the UI.
- Text encoding: plaintext import requires UTF-8 text; non-text or other encodings will fail.
- Key specs:
  - DES/AES: 8-character key.
  - CA: integer 0–255.
  - Affine: `a b`, `a` coprime to 26.
  - Double-Transposition: two keys separated by a space.

## Project Structure

```
.
├── algorithm            # Cipher implementations (usable as a library)
│   ├── block_cipher
│   │   └── aes
│   ├── classical_cipher
│   ├── hash_algorithm
│   ├── public_cipher
│   │   ├── ecc
│   │   └── rsa
│   └── stream_cipher
│       └── ca
├── assets               # Icons and optional QSS styles
│   ├── icons
│   ├── python
│   └── qss
├── event                # GUI event bindings and flows
├── ui                   # GUI definitions
├── test_file            # Example/Test files
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── pyproject.toml       # Optional project config
```

## Developer Usage (without GUI)

```python
# RC4 string encrypt/decrypt
from algorithm.stream_cipher.rc4_cipher import RC4
cipher = RC4()
c = cipher.encrypt('key', 'plaintext')
p = cipher.decrypt('key', c)

# DES file encrypt/decrypt
from algorithm.block_cipher import des_cipher
desc = des_cipher.DESCipher()
desc.new('12345678')
desc.encrypt_file('input.txt', 'output.encrypted')
desc.decrypt_file('output.encrypted', 'output.decrypted')

# AES string encrypt/decrypt
from algorithm.block_cipher.aes import aes_string
c = aes_string.encrypt('hello world', '12345678')
p = aes_string.decrypt(c, '12345678')

# MD5
from algorithm.hash_algorithm import md5_string, md5_file
md5_s = md5_string.md5('hello')
md5_f = md5_file.md5('path/to/file')
```

## FAQ

- No response on encrypt/decrypt: ensure an algorithm is selected and inputs/keys are provided.
- Wrong key length: DES/AES require 8 characters; errors shown in the status bar.
- CA key range: must be an integer within 0–255.
- Text import failure: input must be UTF-8 text; use file mode for binary files.

## Version & Credits

- See repository history for version records.
- Please credit the author: morsuning, for public use.

## License

[Mozilla Public License 2.0](https://github.com/morsuning/cryptography-GUItool/blob/master/LICENSE)

[![Stargazers over time](https://starchart.cc/morsuning/cryptography-GUItool.svg)](https://starchart.cc/morsuning/cryptography-GUItool)