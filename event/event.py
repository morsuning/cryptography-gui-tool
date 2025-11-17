import os

from PyQt5 import QtCore
from PyQt5.QtCore import QSignalMapper, QObject, Qt
from PyQt5.QtWidgets import QFileDialog, QLineEdit

from algorithm.block_cipher import des_cipher
from algorithm.block_cipher.aes import aes_string, aes_file
from algorithm.classical_cipher import (
    caesar_cipher,
    keyword_cipher,
    affine_cipher,
    multilateral_cipher,
    vigenere_cipher,
    permutation_cipher,
    column_permutation_cipher,
    autokey_plaintext_cipher,
    autokey_ciphertext_cipher,
    double_transposition_cipher,
    playfair_cipher,
)
from algorithm.hash_algorithm import md5_file, md5_string
from algorithm.public_cipher.ecc import ecc
from algorithm.public_cipher.rsa import rsa
from algorithm.stream_cipher import rc4_cipher
from algorithm.stream_cipher.ca import ca_string, ca_file
from ui.main_window import UiMainWindow


class Event(UiMainWindow, QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.about.setText("Author:\nmorsuning\n2018.09.25")
        self.md5_file_name = ""
        self.import_plaintext_button_file_name = ""
        self.export_ciphertext_button_file_name = ""
        self.rsa_public_key_file_name = ""
        self.ecc_public_key_file_name = ""
        self.file_to_encrypt_name = ""
        self.file_to_decrypt_name = ""
        self.encrypted_file_to_save_name = ""
        self.decrypted_file_to_save_name = ""

        # 自定义信号范例
        self._window_switch_signal = QtCore.pyqtSignal(str)
        self.button_mapper = QSignalMapper(self)

        self.show_base_frame = True
        self.is_show_widgets = True
        self.default_page_set()
        self.setup_mapper()
        self.setup_connect()

    def setup_mapper(self):
        self.button_mapper.setMapping(self.caesar, 0)
        self.button_mapper.setMapping(self.keyword, 1)
        self.button_mapper.setMapping(self.affine, 2)
        self.button_mapper.setMapping(self.multilateral, 3)
        self.button_mapper.setMapping(self.vigenere, 4)
        self.button_mapper.setMapping(self.autokey_ciphertext, 5)
        self.button_mapper.setMapping(self.autokey_plaintext, 6)
        self.button_mapper.setMapping(self.playfair, 7)
        self.button_mapper.setMapping(self.permutation, 8)
        self.button_mapper.setMapping(self.column_permutation, 9)
        self.button_mapper.setMapping(self.double_transposition, 10)

        self.button_mapper.setMapping(self.RC4, 11)
        self.button_mapper.setMapping(self.CA, 12)

        self.button_mapper.setMapping(self.DES, 13)
        self.button_mapper.setMapping(self.AES, 14)

        self.button_mapper.setMapping(self.RSA, 15)
        self.button_mapper.setMapping(self.ECC, 16)

        self.button_mapper.setMapping(self.MD5, 17)

    # 连接的另一种写法
    # self.connect(self.button_mapper, self.SIGNAL("mapped(int)"), self.show_widgets)
    # self.connect(self.caesar, self.SIGNAL("clicked()"), self.button_mapper, self.SLOT("map()"))
    def setup_connect(self):
        self.button_mapper.mapped.connect(self.show_widgets)
        self.caesar.toggled["bool"].connect(self.button_mapper.map)
        self.keyword.toggled["bool"].connect(self.button_mapper.map)
        self.affine.toggled["bool"].connect(self.button_mapper.map)
        self.multilateral.toggled["bool"].connect(self.button_mapper.map)
        self.vigenere.toggled["bool"].connect(self.button_mapper.map)
        self.autokey_ciphertext.toggled["bool"].connect(self.button_mapper.map)
        self.autokey_plaintext.toggled["bool"].connect(self.button_mapper.map)
        self.playfair.toggled["bool"].connect(self.button_mapper.map)
        self.permutation.toggled["bool"].connect(self.button_mapper.map)
        self.column_permutation.toggled["bool"].connect(self.button_mapper.map)
        self.double_transposition.toggled["bool"].connect(self.button_mapper.map)
        self.RC4.toggled["bool"].connect(self.button_mapper.map)
        self.CA.toggled["bool"].connect(self.button_mapper.map)
        self.DES.toggled["bool"].connect(self.button_mapper.map)
        self.AES.toggled["bool"].connect(self.button_mapper.map)
        self.RSA.toggled["bool"].connect(self.button_mapper.map)
        self.ECC.toggled["bool"].connect(self.button_mapper.map)
        self.MD5.toggled["bool"].connect(self.button_mapper.map)

        # 默认
        self.encrypt_button.clicked.connect(self.default_clicked)
        self.decrypt_button.clicked.connect(self.default_clicked)
        self.string_encrypt_button.clicked.connect(self.default_clicked)
        self.string_decrypt_button.clicked.connect(self.default_clicked)
        self.file_encrypt_button.clicked.connect(self.default_clicked)
        self.file_decrypt_button.clicked.connect(self.default_clicked)
        self.public_encrypt_button.clicked.connect(self.default_clicked)
        self.public_decrypt_button.clicked.connect(self.default_clicked)
        self.public_file_encrypt_button.clicked.connect(self.default_clicked)
        self.public_file_decrypt_button.clicked.connect(self.default_clicked)
        self.public_generate_keypair_button.clicked.connect(self.default_clicked)
        self.public_file_generate_keypair_button.clicked.connect(self.default_clicked)

        # 各界面通用部件

        # MD5
        self.import_file_toolbox.clicked.connect(self.import_file_toolbox_clicked)
        self.pushButton.clicked.connect(self.md5_clicked)

        # 流密码+分组密码
        self.string_show_key_checkbox.stateChanged.connect(self.check_key_2_click)
        self.file_show_key_checkbox.stateChanged.connect(self.check_key_3_click)
        self.string_import_plaintext_button.clicked.connect(
            self.import_plaintext_button_clicked
        )
        self.string_export_ciphertext_button.clicked.connect(
            self.export_ciphertext_button_clicked
        )
        self.file_encrypt_import_button.clicked.connect(self.import_file_button_clicked)
        self.file_encrypt_output_path_button.clicked.connect(self.path_button_clicked)
        self.file_decrypt_import_button.clicked.connect(self.tool_button_3_clicked)
        self.file_decrypt_output_path_button.clicked.connect(self.path_button_2_clicked)

        # 公钥密码
        self.public_import_plaintext_button.clicked.connect(
            self.import_plaintext_button_clicked
        )
        self.public_export_ciphertext_button.clicked.connect(
            self.export_ciphertext_button_clicked
        )
        self.public_file_encrypt_import_button.clicked.connect(self.import_file_button_3_clicked)
        self.public_file_encrypt_output_path_button.clicked.connect(self.path_button_5_clicked)
        self.public_file_decrypt_import_button.clicked.connect(self.tool_button_5_clicked)
        self.public_file_decrypt_output_path_button.clicked.connect(self.path_button_6_clicked)

        # 古典密码
        self.import_plaintext_button.clicked.connect(
            self.import_plaintext_button_clicked
        )
        self.export_ciphertext_button.clicked.connect(
            self.export_ciphertext_button_clicked
        )
        self.check_key.stateChanged.connect(self.check_key_click)

    def default_page_set(self):
        self.switch_sd.setCurrentIndex(0)
        self.cipher_switch_toolbox.setCurrentIndex(0)
        self.classical_cipher_switch.setCurrentIndex(0)
        self.switch_mode_with_key_tabwidget.setCurrentIndex(0)
        self.switch_mode_without_key_tabwidget.setCurrentIndex(0)

    def default_clicked(self):
        pass

    # 通用辅助方法：减少重复代码
    def _toggle_password_echo(self, checkbox, line_edit):
        """
        根据复选框状态切换密钥输入框的可见性，统一处理显示/隐藏逻辑。
        """
        if checkbox.checkState() == Qt.Checked:
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)

    def _select_file(self, title):
        """
        统一的文件选择对话框，返回选中的文件路径或空字符串。
        """
        file_name, _ = QFileDialog.getOpenFileName(self, title, "")
        return file_name

    def _set_import_path(self, target_line_edit, path, success_prefix):
        """
        打开并验证文件可读性，设置路径到目标输入框，并显示统一的状态栏提示。
        """
        f = None
        try:
            f = open(path, "r")
            target_line_edit.setText(path)
            self.statusbar.showMessage(f"{success_prefix}{path}成功", 2000)
        except Exception:
            self.statusbar.showMessage("文件导入失败", 5000)
        finally:
            if f:
                f.close()

    def _import_key_to(self, target_line_edit):
        """
        通用密钥导入逻辑：读取文本文件内容填充到目标输入框。
        """
        path = self._select_file("请选择要导入的文件")
        if not path:
            return
        f = None
        try:
            f = open(path, "r")
            self.statusbar.showMessage("已成功从" + path + "导入文件", 2000)
            target_line_edit.setText(f.read())
        except (UnicodeDecodeError, IOError):
            self.statusbar.showMessage(
                "打开文件" + path + "失败，可能不是文本文件或非“UTF-8”编码",
                5000,
            )
        finally:
            if f:
                f.close()

    def _export_key_from(self, source_line_edit):
        """
        通用密钥导出逻辑：将源输入框文本追加写入用户选择的文件。
        """
        path, _ = QFileDialog.getOpenFileName(self, "导出至", "")
        if not path:
            return
        f = None
        try:
            f = open(path, "a")
            if not source_line_edit.text():
                self.statusbar.showMessage("没有密钥可以被写入", 5000)
            else:
                f.write(source_line_edit.text())
                self.statusbar.showMessage("已成功将密钥写入" + path, 2000)
        except Exception:
            self.statusbar.showMessage("打开或写入" + path + "文件失败", 5000)
        finally:
            if f:
                f.close()

    # ---------------- 通用校验与路径工具 ----------------
    def _check_key_present(self, key_edit, msg="请输入密钥"):
        """
        检查密钥是否输入，未输入时提示并返回 False。
        """
        if not key_edit.text():
            self.statusbar.showMessage(msg, 5000)
            return False
        return True

    def _check_fixed_key_length(self, key_edit, required_len=8, msg="请输入8位密钥"):
        """
        检查密钥长度是否符合要求，不符合时提示并返回 False。
        """
        if len(key_edit.text()) != required_len:
            self.statusbar.showMessage(msg, 5000)
            return False
        return True

    def _check_ca_key_range(self, key_edit):
        """
        检查 CA 密钥是否在 0-255 区间，不符合时提示并返回 False。
        """
        try:
            val = int(key_edit.text())
        except ValueError:
            self.statusbar.showMessage("密钥只能为0-255之间的整数", 5000)
            return False
        if val > 255 or val < 0:
            self.statusbar.showMessage("密钥只能为0-255之间的整数", 5000)
            return False
        return True

    def _ensure_input_file(self, import_edit):
        """
        确保输入文件路径存在，否则提示并返回 False。
        """
        if not import_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return False
        return True

    def _ensure_decrypt_input_file(self, import_edit):
        """
        确保待解密文件路径存在，否则提示并返回 False。
        """
        if not import_edit.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return False
        return True

    def _get_or_set_default_output(self, output_edit, input_path, suffix):
        """
        若输出路径为空，则以输入路径追加后缀生成默认输出路径并设置到控件。
        返回最终输出路径字符串。
        """
        if not output_edit.text():
            default_path = input_path + suffix
            output_edit.setText(default_path)
            return default_path, True
        return output_edit.text(), False

    # ---------------- 字符串加解密通用流程 ----------------
    def _encrypt_string_flow(self, plain_edit, key_edit, cipher_edit, encrypt_impl, key_check=None, key_hint="请输入正确的密钥"):
        """
        通用字符串加密流程：检查输入，执行算法，显示统一提示。
        """
        if not plain_edit.toPlainText():
            return
        if not self._check_key_present(key_edit, key_hint):
            return
        if key_check and not key_check():
            return
        cipher_edit.setPlainText(encrypt_impl(plain_edit.toPlainText(), key_edit.text()))
        self.statusbar.showMessage("加密成功", 2000)

    def _decrypt_string_flow(self, cipher_edit, key_edit, plain_edit, decrypt_impl, key_check=None, key_hint="请输入密钥"):
        """
        通用字符串解密流程：检查输入，执行算法，显示统一提示。
        """
        if not cipher_edit.toPlainText():
            return
        if not self._check_key_present(key_edit, key_hint):
            return
        if key_check and not key_check():
            return
        plain_edit.setPlainText(decrypt_impl(cipher_edit.toPlainText(), key_edit.text()))
        self.statusbar.showMessage("解密成功", 2000)

    # ---------------- 文件加解密通用流程 ----------------
    def _encrypt_file_flow(self, import_edit, key_edit, output_edit, encrypt_impl, default_suffix=".encrypted", key_check=None):
        """
        通用文件加密流程：统一的路径与校验处理，减少重复代码。
        """
        if not self._ensure_input_file(import_edit):
            return
        if not self._check_key_present(key_edit):
            return
        if key_check and not key_check():
            return
        src = import_edit.text()
        dst, is_default = self._get_or_set_default_output(output_edit, src, default_suffix)
        try:
            encrypt_impl(src, dst, key_edit.text())
            if is_default:
                self.statusbar.showMessage("加密成功，文件默认保存至" + dst, 5000)
            else:
                self.statusbar.showMessage("加密成功，文件已保存至" + dst, 5000)
        except Exception:
            self.statusbar.showMessage("加密失败", 5000)

    def _decrypt_file_flow(self, import_edit, key_edit, output_edit, decrypt_impl, default_suffix=".decrypted", key_check=None):
        """
        通用文件解密流程：统一的路径与校验处理，减少重复代码。
        """
        if not self._ensure_decrypt_input_file(import_edit):
            return
        if not self._check_key_present(key_edit):
            return
        if key_check and not key_check():
            return
        src = import_edit.text()
        dst, is_default = self._get_or_set_default_output(output_edit, src, default_suffix)
        try:
            decrypt_impl(src, dst, key_edit.text())
            if is_default:
                self.statusbar.showMessage("解密成功，文件默认保存至" + dst, 5000)
            else:
                self.statusbar.showMessage("解密成功，文件已保存至" + dst, 5000)
        except Exception:
            self.statusbar.showMessage("解密失败", 5000)

    # ---------------- 算法适配器：统一调用签名 ----------------
    def _des_encrypt_file(self, src, dst, key):
        cipher = des_cipher.DESCipher()
        cipher.new(key)
        cipher.encrypt_file(src, dst)

    def _des_decrypt_file(self, src, dst, key):
        cipher = des_cipher.DESCipher()
        cipher.new(key)
        cipher.decrypt_file(src, dst)

    def _des_encrypt_string(self, plaintext, key):
        cipher = des_cipher.DESCipher()
        cipher.new(key)
        return cipher.encrypt_string(plaintext)

    def _des_decrypt_string(self, ciphertext, key):
        cipher = des_cipher.DESCipher()
        cipher.new(key)
        return cipher.decrypt_string(ciphertext)

    def _aes_encrypt_file(self, src, dst, key):
        aes_file.encrypt(src, key, dst)

    def _aes_decrypt_file(self, src, dst, key):
        aes_file.decrypt(src, key, dst)

    def _aes_encrypt_string(self, plaintext, key):
        return aes_string.encrypt(plaintext, key)

    def _aes_decrypt_string(self, ciphertext, key):
        return aes_string.decrypt(ciphertext, key)

    def _rc4_encrypt_file(self, src, dst, key):
        cipher = rc4_cipher.RC4()
        cipher.encrypt_file(src, dst, key)

    def _rc4_decrypt_file(self, src, dst, key):
        cipher = rc4_cipher.RC4()
        # RC4 解密函数签名为 (file_plain, file_ciphered, key)
        cipher.decrypt_file(dst, src, key)

    def _rc4_encrypt_string(self, plaintext, key):
        cipher = rc4_cipher.RC4()
        return cipher.encrypt(key, plaintext)

    def _rc4_decrypt_string(self, ciphertext, key):
        cipher = rc4_cipher.RC4()
        return cipher.decrypt(key, ciphertext)

    def _ca_encrypt_file(self, src, dst, key):
        ca_file.encrypt(src, int(key), dst)

    def _ca_decrypt_file(self, src, dst, key):
        ca_file.decrypt(src, int(key), dst)

    def _ca_encrypt_string(self, plaintext, key):
        return ca_string.encrypt(plaintext, int(key))

    def _ca_decrypt_string(self, ciphertext, key):
        return ca_string.decrypt(ciphertext, int(key))

    def _read_lines(self, filename, count=1):
        """
        读取指定数量的文本行，失败时统一提示并返回 None。
        """
        f = None
        try:
            f = open(filename, "r")
            lines = [f.readline() for _ in range(count)]
            return lines
        except (IOError, Exception):
            self.statusbar.showMessage("打开文件" + filename + "失败", 5000)
            return None
        finally:
            if f:
                f.close()

    def send_window_switch_signal(self):
        self._window_switch_signal.emit()

    def import_file_button_clicked(self):
        path = self._select_file("请选择要导入的文件")
        self.file_to_encrypt_name = path
        if not path:
            return
        self._set_import_path(self.file_encrypt_input_path_edit, path, "导入文件")

    def import_file_button_3_clicked(self):
        path = self._select_file("请选择要导入的文件")
        self.file_to_encrypt_name = path
        if not path:
            return
        self._set_import_path(self.public_file_encrypt_input_path_edit, path, "导入文件")

    def path_button_clicked(self):
        path = self._select_file("请选择要保存到的文件")
        self.encrypted_file_to_save_name = path
        self.file_encrypt_output_path_edit.setText(path)
        self.statusbar.showMessage("加密后的文件将保存为" + path, 5000)

    def path_button_5_clicked(self):
        path = self._select_file("请选择要保存到的文件")
        self.encrypted_file_to_save_name = path
        self.public_file_encrypt_output_path_edit.setText(path)
        self.statusbar.showMessage("加密后的文件将保存为" + path, 5000)

    def tool_button_3_clicked(self):
        path = self._select_file("请选择要导入的文件")
        self.file_to_decrypt_name = path
        if not path:
            return
        self._set_import_path(self.file_decrypt_input_path_edit, path, "导入文件")

    def tool_button_5_clicked(self):
        path = self._select_file("请选择要导入的文件")
        self.file_to_decrypt_name = path
        if not path:
            return
        self._set_import_path(self.public_file_decrypt_input_path_edit, path, "导入文件")

    def path_button_2_clicked(self):
        path = self._select_file("请选择要保存到的文件")
        self.decrypted_file_to_save_name = path
        self.file_decrypt_output_path_edit.setText(path)
        self.statusbar.showMessage("解密后的文件将保存为" + path, 5000)

    def path_button_6_clicked(self):
        path = self._select_file("请选择要保存到的文件")
        self.decrypted_file_to_save_name = path
        self.public_file_decrypt_output_path_edit.setText(path)
        self.statusbar.showMessage("解密后的文件将保存为" + path, 5000)

    def import_file_toolbox_clicked(self):
        self.md5_file_name, file_type = QFileDialog.getOpenFileName(
            self,
            "请选择要导入的文件",
            "",
        )
        if not self.md5_file_name:
            return
        else:
            self.lineEdit.setText(self.md5_file_name)

    def md5_clicked(self):
        if self.md5_file_name and self.input_edit.toPlainText():
            self.statusbar.showMessage("同一时刻只能输入字符串或者文件", 5000)
            return
        if self.md5_file_name:
            self.md5_show_text.setText(md5_file.md5(self.md5_file_name))
            self.md5_file_name = ""
            self.lineEdit.setText("")
            self.statusbar.showMessage("成功生成文件MD5", 2000)
        elif self.input_edit.toPlainText():
            self.md5_show_text.setText(md5_string.md5(self.input_edit.toPlainText()))
            self.statusbar.showMessage("成功生成字符串MD5", 2000)
        else:
            return

    def check_key_click(self):
        self._toggle_password_echo(self.check_key, self.input_key)

    def check_key_2_click(self):
        self._toggle_password_echo(self.string_show_key_checkbox, self.string_key_input)

    def check_key_3_click(self):
        self._toggle_password_echo(self.file_show_key_checkbox, self.file_key_input)

    def import_plaintext_button_clicked(self):
        path = self._select_file("请选择要导入的文件")
        if not path:
            return
        f = None
        try:
            f = open(path, "r")
            self.statusbar.showMessage("已成功从" + path + "导入文件", 2000)
            self.plain_text_edit.setPlainText(f.read())
        except (UnicodeDecodeError, IOError):
            self.statusbar.showMessage(
                "打开文件" + path + "失败，可能不是文本文件或非“UTF-8”编码",
                5000,
            )
        finally:
            if f:
                f.close()

    def export_ciphertext_button_clicked(self):
        export_path, _ = QFileDialog.getOpenFileName(self, "导出至", "")
        if not export_path:
            return
        f = None
        try:
            f = open(export_path, "a")
            if not self.cipher_text_edit.toPlainText():
                self.statusbar.showMessage("没有密文可以被写入", 5000)
            else:
                # 待办：导入导出明文密文需处理非ASCII字符问题
                f.write("\n" + self.cipher_text_edit.toPlainText())
                self.statusbar.showMessage(
                    "已成功将密文写入" + export_path,
                    2000,
                )
        except Exception:
            self.statusbar.showMessage(
                "打开或写入" + export_path + "文件失败",
                5000,
            )
        finally:
            if f:
                f.close()

    def import_1(self):
        self._import_key_to(self.input_key)

    def export_1(self):
        self._export_key_from(self.input_key)

    def import_2(self):
        self._import_key_to(self.string_key_input)

    def export_2(self):
        self._export_key_from(self.string_key_input)

    def import_3(self):
        self._import_key_to(self.file_key_input)

    def export_3(self):
        self._export_key_from(self.file_key_input)

    def import_4(self):
        self.import_public_key_button_file_name, import_plaintext_button_file_type = (
            QFileDialog.getOpenFileName(
                self,
                "请选择要导入的公钥",
                "",
            )
        )
        self.import_private_key_button_file_name, type = QFileDialog.getOpenFileName(
            self,
            "请选择要导入的私钥",
            "",
        )
        if (
            not self.import_public_key_button_file_name
            or not self.import_private_key_button_file_name
        ):
            return
        else:
            f = None
            try:
                f = open(self.import_private_key_button_file_name, "r")
                self.public_private_key_display.setText(f.read())
                self.public_file_private_key_display.setText(f.read())
                self.rsa_public_key_file_name = self.import_public_key_button_file_name
                self.ecc_public_key_file_name = self.import_public_key_button_file_name
                self.statusbar.showMessage(
                    "已成功导入公私钥文件，不配对的公私钥或错误格式的公钥会导致加密失败",
                    2000,
                )
            except (UnicodeDecodeError, IOError):
                self.statusbar.showMessage(
                    "打开文件"
                    + self.import_private_key_button_file_name
                    + "失败，可能不是文本文件或非“UTF-8”编码",
                    5000,
                )
            finally:
                if f:
                    f.close()

    def export_4(self):
        self.export_private_key_button_file_name, export_plaintext_button_file_type = (
            QFileDialog.getOpenFileName(
                self,
                "导出私钥至",
                "",
            )
        )
        if not self.export_private_key_button_file_name:
            return
        else:
            f = None
            try:
                f = open(self.export_private_key_button_file_name, "a")
                if (
                    not self.public_private_key_display.toPlainText()
                    or not self.public_file_private_key_display.toPlainText()
                ):
                    self.statusbar.showMessage("没有私钥可以被写入", 5000)
                else:
                    f.write(self.public_private_key_display.toPlainText())
                    self.statusbar.showMessage(
                        "已成功将私钥写入" + self.export_private_key_button_file_name,
                        2000,
                    )
            except Exception:
                self.statusbar.showMessage(
                    "打开或写入"
                    + self.export_private_key_button_file_name
                    + "文件失败",
                    5000,
                )
            finally:
                if f:
                    f.close()

    def caesar_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    caesar_cipher.caesar_encrypt(
                        self.plain_text_edit.toPlainText(), int(self.input_key.text())
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    def keyword_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                keyword_cipher_text, key = keyword_cipher.encrypt(
                    self.plain_text_edit.toPlainText(), self.input_key.text()
                )
                self.cipher_text_edit.setPlainText(keyword_cipher_text)
                self.statusbar.showMessage("加密成功", 2000)

    def affine_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                key = self.input_key.text()
                if key[0] == " " or key[-1] == " " or (" " not in key):
                    self.statusbar.showMessage("密钥格式输入错误", 5000)
                else:
                    index = 0
                    for i in key:
                        if i == " ":
                            index = key.index(i)
                    a = int(key[:index])
                    b = int(key[index + 1 :])
                    if (a % 2 == 0) or (a % 13 == 0):
                        self.statusbar.showMessage("参数a需与26互素（不能为偶数或13的倍数）", 5000)
                        return
                    filtered = affine_cipher.filter_clear(self.plain_text_edit.toPlainText())
                    self.cipher_text_edit.setPlainText(
                        affine_cipher.encrypt(filtered, a, b)
                    )
                    self.statusbar.showMessage("加密成功", 2000)

    def multilateral_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    multilateral_cipher.encrypt(
                        self.plain_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    def vigenere_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    vigenere_cipher.encrypt(
                        self.plain_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    # 待办：Autokey 密文模式要求密钥长度大于明文
    def autokey_ciphertext_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    autokey_plaintext_cipher.encrypt(
                        self.plain_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    def autokey_plaintext_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    autokey_plaintext_cipher.encrypt(
                        self.plain_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    def playfair_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    playfair_cipher.playfair(
                        self.input_key.text(), self.plain_text_edit.toPlainText(), True
                    ).lower()
                )
                self.statusbar.showMessage("加密成功", 2000)

    def permutation_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = permutation_cipher
                self.cipher_text_edit.setPlainText(
                    cipher.encrypt(
                        self.plain_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    def column_permutation_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    column_permutation_cipher.encrypt(
                        self.plain_text_edit.toPlainText().replace(" ", ""),
                        self.input_key.text(),
                    )
                )
                self.statusbar.showMessage("加密成功", 2000)

    def double_transposition_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                key = self.input_key.text()
                if key[0] == " " or key[-1] == " " or (" " not in key):
                    self.statusbar.showMessage("密钥格式输入错误", 5000)
                else:
                    index = 0
                    for i in key:
                        if i == " ":
                            index = key.index(i)
                    a = key[:index]
                    b = key[index + 1 :]
                    self.cipher_text_edit.setPlainText(
                        double_transposition_cipher.encrypt(
                            self.plain_text_edit.toPlainText(), a, b
                        )
                    )
                    self.statusbar.showMessage("加密成功", 2000)

    def caesar_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    caesar_cipher.caesar_decrypt(
                        self.cipher_text_edit.toPlainText(), int(self.input_key.text())
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def keyword_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    keyword_cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def affine_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                index = 0
                for i in self.input_key.text():
                    if i == " ":
                        index = self.input_key.text().index(i)
                a = int(self.input_key.text()[:index])
                b = int(self.input_key.text()[index + 1 :])
                if (a % 2 == 0) or (a % 13 == 0):
                    self.statusbar.showMessage("参数a需与26互素（不能为偶数或13的倍数）", 5000)
                    return
                filtered = affine_cipher.filter_clear(self.cipher_text_edit.toPlainText())
                self.plain_text_edit.setPlainText(
                    affine_cipher.decrypt(filtered, a, b)
                )
                self.statusbar.showMessage("解密成功", 2000)

    def multilateral_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                try:
                    self.plain_text_edit.setPlainText(
                        multilateral_cipher.decrypt(
                            self.cipher_text_edit.toPlainText(), self.input_key.text()
                        )
                    )
                    self.statusbar.showMessage("解密成功", 2000)
                except Exception:
                    self.statusbar.showMessage("解密失败", 5000)

    def vigenere_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    vigenere_cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def autokey_ciphertext_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    autokey_ciphertext_cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def autokey_plaintext_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    autokey_plaintext_cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def playfair_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    playfair_cipher.playfair(
                        self.input_key.text(),
                        self.cipher_text_edit.toPlainText(),
                        False,
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def permutation_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = permutation_cipher
                self.plain_text_edit.setPlainText(
                    cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def column_permutation_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    column_permutation_cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), self.input_key.text()
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def double_transposition_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                index = 0
                for i in self.input_key.text():
                    if i == " ":
                        index = self.input_key.text().index(i)
                a = self.input_key.text()[:index]
                b = self.input_key.text()[index + 1 :]
                self.plain_text_edit.setPlainText(
                    double_transposition_cipher.decrypt(
                        self.cipher_text_edit.toPlainText(), b, a
                    )
                )
                self.statusbar.showMessage("解密成功", 2000)

    def des_encrypt_string_button_clicked(self):
        self._encrypt_string_flow(
            self.string_plain_text_edit,
            self.string_key_input,
            self.string_cipher_text_edit,
            lambda p, k: self._des_encrypt_string(p, k),
            key_check=lambda: self._check_fixed_key_length(self.string_key_input, 8),
            key_hint="请输入正确的密钥",
        )

    def des_encrypt_file_button_clicked(self):
        self._encrypt_file_flow(
            self.file_encrypt_input_path_edit,
            self.file_key_input,
            self.file_encrypt_output_path_edit,
            self._des_encrypt_file,
            default_suffix=".encrypted",
            key_check=lambda: self._check_fixed_key_length(self.file_key_input, 8),
        )

    def aes_encrypt_string_button_clicked(self):
        self._encrypt_string_flow(
            self.string_plain_text_edit,
            self.string_key_input,
            self.string_cipher_text_edit,
            lambda p, k: self._aes_encrypt_string(p, k),
            key_check=lambda: self._check_fixed_key_length(self.string_key_input, 8),
            key_hint="请输入正确的密钥",
        )

    def aes_encrypt_file_button_clicked(self):
        self._encrypt_file_flow(
            self.file_encrypt_input_path_edit,
            self.file_key_input,
            self.file_encrypt_output_path_edit,
            self._aes_encrypt_file,
            default_suffix=".encrypted",
            key_check=lambda: self._check_fixed_key_length(self.file_key_input, 8),
        )

    def rc4_encrypt_string_button_clicked(self):
        self._encrypt_string_flow(
            self.string_plain_text_edit,
            self.string_key_input,
            self.string_cipher_text_edit,
            lambda p, k: self._rc4_encrypt_string(p, k),
        )

    def rc4_encrypt_file_button_clicked(self):
        self._encrypt_file_flow(
            self.file_encrypt_input_path_edit,
            self.file_key_input,
            self.file_encrypt_output_path_edit,
            self._rc4_encrypt_file,
            default_suffix=".encrypted",
        )

    def ca_encrypt_string_button_clicked(self):
        self._encrypt_string_flow(
            self.string_plain_text_edit,
            self.string_key_input,
            self.string_cipher_text_edit,
            lambda p, k: self._ca_encrypt_string(p, k),
            key_check=lambda: self._check_ca_key_range(self.string_key_input),
        )

    def ca_encrypt_file_button_clicked(self):
        self._encrypt_file_flow(
            self.file_encrypt_input_path_edit,
            self.file_key_input,
            self.file_encrypt_output_path_edit,
            self._ca_encrypt_file,
            default_suffix=".encrypted",
            key_check=lambda: self._check_ca_key_range(self.file_key_input),
        )

    def des_decrypt_string_button_clicked(self):
        self._decrypt_string_flow(
            self.string_cipher_text_edit,
            self.string_key_input,
            self.string_plain_text_edit,
            lambda c, k: self._des_decrypt_string(c, k),
            key_check=lambda: self._check_fixed_key_length(self.string_key_input, 8),
        )

    def aes_decrypt_string_button_clicked(self):
        self._decrypt_string_flow(
            self.string_cipher_text_edit,
            self.string_key_input,
            self.string_plain_text_edit,
            lambda c, k: self._aes_decrypt_string(c, k),
            key_check=lambda: self._check_fixed_key_length(self.string_key_input, 8),
        )

    def rc4_decrypt_string_button_clicked(self):
        self._decrypt_string_flow(
            self.string_cipher_text_edit,
            self.string_key_input,
            self.string_plain_text_edit,
            lambda c, k: self._rc4_decrypt_string(c, k),
        )

    def ca_decrypt_string_button_clicked(self):
        self._decrypt_string_flow(
            self.string_cipher_text_edit,
            self.string_key_input,
            self.string_plain_text_edit,
            lambda c, k: self._ca_decrypt_string(c, k),
            key_check=lambda: self._check_ca_key_range(self.string_key_input),
        )

    def des_decrypt_file_button_clicked(self):
        self._decrypt_file_flow(
            self.file_decrypt_input_path_edit,
            self.file_key_input,
            self.file_decrypt_output_path_edit,
            self._des_decrypt_file,
            default_suffix=".decrypted",
            key_check=lambda: self._check_fixed_key_length(self.file_key_input, 8),
        )

    def aes_decrypt_file_button_clicked(self):
        self._decrypt_file_flow(
            self.file_decrypt_input_path_edit,
            self.file_key_input,
            self.file_decrypt_output_path_edit,
            self._aes_decrypt_file,
            default_suffix=".decrypted",
        )

    def rc4_decrypt_file_button_clicked(self):
        self._decrypt_file_flow(
            self.file_decrypt_input_path_edit,
            self.file_key_input,
            self.file_decrypt_output_path_edit,
            self._rc4_decrypt_file,
            default_suffix=".decrypted",
        )

    def ca_decrypt_file_button_clicked(self):
        self._decrypt_file_flow(
            self.file_decrypt_input_path_edit,
            self.file_key_input,
            self.file_decrypt_output_path_edit,
            self._ca_decrypt_file,
            default_suffix=".decrypted",
            key_check=lambda: self._check_ca_key_range(self.file_key_input),
        )

    # 待办：该操作可能导致崩溃风险
    def rsa_generate_keypair_button_clicked(self):
        # private key: d
        # public key: e n
        e, n, d = rsa.RSA()
        self.public_private_key_display.setText(str(d))
        self.public_file_private_key_display.setText(str(d))
        self.rsa_public_key_file_name = "rsa_public_key_" + os.urandom(10).hex()
        f = None
        try:
            f = open(self.rsa_public_key_file_name, "w")
            f.writelines([str(e) + "\n", str(n) + "\n"])
            self.statusbar.showMessage(
                "成功生成RSA公钥和私钥，公钥已保存至" + self.rsa_public_key_file_name,
                5000,
            )
        except Exception:
            self.statusbar.showMessage(
                "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000
            )
        finally:
            if f:
                f.close()

    def rsa_encrypt_string_button_clicked(self):
        if not self.public_plain_text_edit.toPlainText():
            return
        else:
            if not self.public_private_key_display.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                lines = self._read_lines(self.rsa_public_key_file_name, 2)
                if not lines:
                    self.statusbar.showMessage("加密时出错", 5000)
                    return
                e, n = lines
                self.public_cipher_text_edit.setPlainText(
                    rsa.encrypt(int(e), int(n), self.public_plain_text_edit.toPlainText())
                )
                self.statusbar.showMessage("加密成功", 2000)

    def rsa_decrypt_string_button_clicked(self):
        if not self.public_cipher_text_edit.toPlainText():
            return
        else:
            lines = self._read_lines(self.rsa_public_key_file_name, 1)
            if not lines:
                self.statusbar.showMessage("解密时出错", 5000)
                return
            n = lines[0]
            d = self.public_private_key_display.toPlainText()
            self.public_plain_text_edit.setPlainText(
                rsa.decrypt(int(d), int(n), self.public_cipher_text_edit.toPlainText())
            )
            self.statusbar.showMessage("解密成功", 2000)

    def rsa_encrypt_file_button_clicked(self):
        if not self.public_file_encrypt_input_path_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.public_file_private_key_display.toPlainText():
                self.statusbar.showMessage("请先生成或导入密钥对", 5000)
            else:
                if not self.public_file_encrypt_output_path_edit.text():
                    try:
                        default_encrypted_file_save_path = (
                            self.public_file_encrypt_input_path_edit.text() + ".encrypted"
                        )
                        self.public_file_encrypt_output_path_edit.setText(default_encrypted_file_save_path)
                        lines = self._read_lines(self.rsa_public_key_file_name, 2)
                        if not lines:
                            self.statusbar.showMessage("加密时出错", 5000)
                        else:
                            e, n = lines
                            rsa.encode_file(
                                int(e),
                                int(n),
                                self.public_file_encrypt_input_path_edit.text(),
                                default_encrypted_file_save_path,
                            )
                        self.statusbar.showMessage(
                            "加密成功，文件默认保存至"
                            + default_encrypted_file_save_path,
                            5000,
                        )
                    except Exception:
                        self.statusbar.showMessage("加密失败")
                else:
                    try:
                        lines = self._read_lines(self.rsa_public_key_file_name, 2)
                        if not lines:
                            self.statusbar.showMessage("加密时出错", 5000)
                        else:
                            e, n = lines
                            rsa.encode_file(
                                int(e),
                                int(n),
                                self.public_file_encrypt_input_path_edit.text(),
                                self.public_file_encrypt_output_path_edit.text(),
                            )
                        self.statusbar.showMessage(
                            "加密成功，文件已保存至" + self.public_file_encrypt_output_path_edit.text(),
                            5000,
                        )
                    except Exception:
                        self.statusbar.showMessage("加密失败")

    def rsa_decrypt_file_button_clicked(self):
        if not self.public_file_decrypt_input_path_edit.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.public_file_private_key_display.toPlainText():
                self.statusbar.showMessage("请先生成或导入密钥对", 5000)
            else:
                if not self.public_file_decrypt_output_path_edit.text():
                    try:
                        default_decrypted_file_save_path = (
                            self.public_file_decrypt_input_path_edit.text() + ".decrypted"
                        )
                        self.public_file_decrypt_output_path_edit.setText(default_decrypted_file_save_path)
                        d = self.public_file_private_key_display.toPlainText()
                        lines = self._read_lines(self.rsa_public_key_file_name, 1)
                        if not lines:
                            self.statusbar.showMessage("解密时出错", 5000)
                        else:
                            n = lines[0]
                            rsa.decode_file(
                                int(d),
                                int(n),
                                self.public_file_decrypt_input_path_edit.text(),
                                default_decrypted_file_save_path,
                            )
                        self.statusbar.showMessage(
                            "解密成功，文件默认保存至"
                            + default_decrypted_file_save_path,
                            5000,
                        )
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        d = self.public_file_private_key_display.toPlainText()
                        lines = self._read_lines(self.rsa_public_key_file_name, 1)
                        if not lines:
                            self.statusbar.showMessage("解密时出错", 5000)
                        else:
                            n = lines[0]
                            rsa.decode_file(
                                int(d),
                                int(n),
                                self.public_file_decrypt_input_path_edit.text(),
                                self.public_file_decrypt_output_path_edit.text(),
                            )
                        self.statusbar.showMessage(
                            "解密成功，文件已保存至" + self.public_file_decrypt_output_path_edit.text(), 5000
                        )
                    except Exception:
                        self.statusbar.showMessage("解密失败")

    def ecc_generate_keypair_button_clicked(self):
        # private key: d
        # public key: G(x, y)
        cipher = ecc.EccCipher()
        private_key, public_key = cipher.make_key_pair()
        self.show_keypair_text.setText(str(private_key))
        self.show_keypair_text_2.setText(str(private_key))
        self.ecc_public_key_file_name = "ecc_public_key_" + os.urandom(10).hex()
        f = None
        try:
            f = open(self.ecc_public_key_file_name, "w")
            f.writelines([str(public_key[0]) + "\n", str(public_key[1]) + "\n"])
            self.statusbar.showMessage(
                "成功生成ECC公钥和私钥，公钥已保存至" + self.ecc_public_key_file_name,
                5000,
            )
        except Exception:
            self.statusbar.showMessage(
                "打开或写入" + self.ecc_public_key_file_name + "文件失败", 5000
            )
        finally:
            if f:
                f.close()

    def ecc_encrypt_string_button_clicked(self):
        if not self.public_plain_text_edit.toPlainText():
            return
        else:
            if not self.public_private_key_display.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                f = None
                try:
                    f = open(self.ecc_public_key_file_name, "r")
                    cipher = ecc.EccCipher()
                    self.ecc_result = cipher.encrypt(
                        self.public_plain_text_edit.toPlainText().encode("utf-8")
                    )
                    self.public_cipher_text_edit.setPlainText(self.ecc_result.hex())
                    self.statusbar.showMessage("加密成功", 2000)
                except (IOError, Exception):
                    if IOError:
                        self.statusbar.showMessage(
                            "打开文件" + self.ecc_public_key_file_name + "失败", 5000
                        )
                    self.statusbar.showMessage("加密时出错", 5000)
                finally:
                    if f:
                        f.close()

    def ecc_decrypt_string_button_clicked(self):
        if not self.public_cipher_text_edit.toPlainText():
            return
        else:
            f = None
            try:
                f = open(self.ecc_public_key_file_name, "r")
                cipher = ecc.EccCipher()
                self.public_plain_text_edit.setPlainText(
                    cipher.decrypt(self.ecc_result).decode("utf-8")
                )
                self.statusbar.showMessage("解密成功", 2000)
            except Exception:
                self.statusbar.showMessage("解密时出错", 5000)
            finally:
                if f:
                    f.close()

    def ecc_encrypt_file_button_clicked(self):
        if not self.public_file_encrypt_input_path_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.public_file_private_key_display.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                if not self.public_file_encrypt_output_path_edit.text():
                    try:
                        default_encrypted_file_save_path = (
                            self.public_file_encrypt_input_path_edit.text() + ".encrypted"
                        )
                        self.public_file_encrypt_output_path_edit.setText(default_encrypted_file_save_path)
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, "r")
                            with open(
                                self.public_file_encrypt_input_path_edit.text(), "rb"
                            ) as import_file:
                                cipher_text = cipher.encrypt(import_file.read())
                            with open(
                                default_encrypted_file_save_path, "wb"
                            ) as save_file:
                                save_file.write(cipher_text)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入"
                                    + self.ecc_public_key_file_name
                                    + "文件失败",
                                    5000,
                                )
                            self.statusbar.showMessage("加密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage(
                            "加密成功，文件默认保存至"
                            + default_encrypted_file_save_path,
                            5000,
                        )
                    except Exception:
                        self.statusbar.showMessage("加密失败")
                else:
                    try:
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, "r")
                            with open(
                                self.public_file_encrypt_input_path_edit.text(), "rb"
                            ) as import_file:
                                cipher_text = cipher.encrypt(import_file.read())
                            with open(self.public_file_encrypt_output_path_edit.text(), "wb") as save_file:
                                save_file.write(cipher_text)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入"
                                    + self.rsa_public_key_file_name
                                    + "文件失败",
                                    5000,
                                )
                            self.statusbar.showMessage("加密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage(
                            "加密成功，文件已保存至" + self.public_file_encrypt_output_path_edit.text(),
                            5000,
                        )
                    except Exception:
                        self.statusbar.showMessage("加密失败")

    def ecc_decrypt_file_button_clicked(self):
        if not self.public_file_decrypt_input_path_edit.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.public_file_private_key_display.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                if not self.public_file_decrypt_output_path_edit.text():
                    try:
                        default_decrypted_file_save_path = (
                            self.public_file_decrypt_input_path_edit.text() + ".decrypted"
                        )
                        self.public_file_decrypt_output_path_edit.setText(default_decrypted_file_save_path)
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, "r")
                            with open(self.public_file_decrypt_input_path_edit.text(), "rb") as import_file:
                                plaintext = cipher.decrypt(import_file.read())
                            with open(
                                default_decrypted_file_save_path, "wb"
                            ) as save_file:
                                save_file.write(plaintext)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入"
                                    + self.ecc_public_key_file_name
                                    + "文件失败",
                                    5000,
                                )
                            self.statusbar.showMessage("解密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage(
                            "解密成功，文件默认保存至"
                            + default_decrypted_file_save_path,
                            5000,
                        )
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, "r")
                            with open(self.public_file_decrypt_input_path_edit.text(), "rb") as import_file:
                                plaintext = cipher.decrypt(import_file.read())
                            with open(self.public_file_decrypt_output_path_edit.text(), "wb") as save_file:
                                save_file.write(plaintext)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入"
                                    + self.ecc_public_key_file_name
                                    + "文件失败",
                                    5000,
                                )
                            self.statusbar.showMessage("解密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage(
                            "解密成功，文件已保存至" + self.public_file_decrypt_output_path_edit.text(), 5000
                        )
                    except Exception:
                        self.statusbar.showMessage("解密失败")

    # 决定显示4个窗口中的哪一个，并改变相应控件，需在此更新部分连接
    def show_widgets(self, button):
        self.base_frame.setVisible(not self.is_show_widgets)
        # MD5 ——已完成
        if button == 17:
            self.md5_frame.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
        elif button == 15 or button == 16:
            self.switch_mode_without_key_tabwidget.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # RSA ——已完成；已知问题：RSA 字符串解密时会丢掉第一个字符
            if button == 15:
                self.public_generate_keypair_button.clicked.disconnect()
                self.public_file_generate_keypair_button.clicked.disconnect()
                self.public_encrypt_button.clicked.disconnect()
                self.public_decrypt_button.clicked.disconnect()
                self.public_file_encrypt_button.clicked.disconnect()
                self.public_file_decrypt_button.clicked.disconnect()
                self.public_generate_keypair_button.clicked.connect(
                    self.rsa_generate_keypair_button_clicked
                )
                self.public_file_generate_keypair_button.clicked.connect(
                    self.rsa_generate_keypair_button_clicked
                )
                self.public_encrypt_button.clicked.connect(
                    self.rsa_encrypt_string_button_clicked
                )
                self.public_decrypt_button.clicked.connect(
                    self.rsa_decrypt_string_button_clicked
                )
                self.public_file_encrypt_button.clicked.connect(
                    self.rsa_encrypt_file_button_clicked
                )
                self.public_file_decrypt_button.clicked.connect(
                    self.rsa_decrypt_file_button_clicked
                )
                self.public_private_key_display.setText("")
                self.public_file_private_key_display.setText("")
                self.public_plain_text_edit.setPlainText("")
                self.public_cipher_text_edit.setPlainText("")
                self.public_file_encrypt_input_path_edit.setText("")
                self.public_file_encrypt_output_path_edit.setText("")
                self.public_file_decrypt_input_path_edit.setText("")
                self.public_file_decrypt_output_path_edit.setText("")
                self.public_file_algorithm_label.setText("RSA")
                self.public_current_cipher_label.setText("RSA")
            # ECC ——已完成
            elif button == 16:
                self.public_generate_keypair_button.clicked.disconnect()
                self.public_file_generate_keypair_button.clicked.disconnect()
                self.public_encrypt_button.clicked.disconnect()
                self.public_decrypt_button.clicked.disconnect()
                self.public_file_encrypt_button.clicked.disconnect()
                self.public_file_decrypt_button.clicked.disconnect()
                self.public_generate_keypair_button.clicked.connect(
                    self.ecc_generate_keypair_button_clicked
                )
                self.public_file_generate_keypair_button.clicked.connect(
                    self.ecc_generate_keypair_button_clicked
                )
                self.public_encrypt_button.clicked.connect(
                    self.ecc_encrypt_string_button_clicked
                )
                self.public_decrypt_button.clicked.connect(
                    self.ecc_decrypt_string_button_clicked
                )
                self.public_file_encrypt_button.clicked.connect(
                    self.ecc_encrypt_file_button_clicked
                )
                self.public_file_decrypt_button.clicked.connect(
                    self.ecc_decrypt_file_button_clicked
                )
                self.public_private_key_display.setText("")
                self.public_file_private_key_display.setText("")
                self.public_plain_text_edit.setPlainText("")
                self.public_cipher_text_edit.setPlainText("")
                self.public_file_encrypt_input_path_edit.setText("")
                self.public_file_encrypt_output_path_edit.setText("")
                self.public_file_decrypt_input_path_edit.setText("")
                self.public_file_decrypt_output_path_edit.setText("")
                self.public_file_algorithm_label.setText("ECC")
                self.public_current_cipher_label.setText("ECC")
        elif button == 11 or button == 12 or button == 13 or button == 14:
            self.switch_mode_with_key_tabwidget.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # RC4 ——已完成
            if button == 11:
                self.string_encrypt_button.clicked.disconnect()
                self.string_decrypt_button.clicked.disconnect()
                self.file_encrypt_button.clicked.disconnect()
                self.file_decrypt_button.clicked.disconnect()
                self.string_encrypt_button.clicked.connect(
                    self.rc4_encrypt_string_button_clicked
                )
                self.string_decrypt_button.clicked.connect(
                    self.rc4_decrypt_string_button_clicked
                )
                self.file_encrypt_button.clicked.connect(
                    self.rc4_encrypt_file_button_clicked
                )
                self.file_decrypt_button.clicked.connect(
                    self.rc4_decrypt_file_button_clicked
                )
                self.string_key_input.setText("")
                self.file_key_input.setText("")
                self.string_plain_text_edit.setPlainText("")
                self.string_cipher_text_edit.setPlainText("")
                self.file_encrypt_input_path_edit.setText("")
                self.file_encrypt_output_path_edit.setText("")
                self.file_decrypt_input_path_edit.setText("")
                self.file_decrypt_output_path_edit.setText("")
                self.current_cipher_label.setText("RC4")
                self.file_algorithm_label.setText("RC4")
                self.string_key_input.setPlaceholderText(
                    "仅限大小写字母和数字的组合，不限位数"
                )
                self.file_key_input.setMaxLength(65535)
                self.file_key_input.setPlaceholderText(
                    "仅限大小写字母和数字的组合，不限位数"
                )
                self.file_key_input.setMaxLength(65535)
                self.string_key_input.setValidator(self.string_key_validator_alnum)
                self.file_key_input.setValidator(self.file_key_validator_alnum)
            # CA ——已完成
            elif button == 12:
                self.string_encrypt_button.clicked.disconnect()
                self.string_decrypt_button.clicked.disconnect()
                self.file_encrypt_button.clicked.disconnect()
                self.file_decrypt_button.clicked.disconnect()
                self.string_encrypt_button.clicked.connect(
                    self.ca_encrypt_string_button_clicked
                )
                self.string_decrypt_button.clicked.connect(
                    self.ca_decrypt_string_button_clicked
                )
                self.file_encrypt_button.clicked.connect(
                    self.ca_encrypt_file_button_clicked
                )
                self.file_decrypt_button.clicked.connect(
                    self.ca_decrypt_file_button_clicked
                )
                self.string_key_input.setText("")
                self.file_key_input.setText("")
                self.string_plain_text_edit.setPlainText("")
                self.string_cipher_text_edit.setPlainText("")
                self.file_encrypt_input_path_edit.setText("")
                self.file_encrypt_output_path_edit.setText("")
                self.file_decrypt_input_path_edit.setText("")
                self.file_decrypt_output_path_edit.setText("")
                self.current_cipher_label.setText("CA")
                self.file_algorithm_label.setText("CA")
                self.string_key_input.setMaxLength(3)
                self.string_key_input.setPlaceholderText("请输入0-255之间的整数")
                self.file_key_input.setMaxLength(3)
                self.file_key_input.setPlaceholderText("请输入0-255之间的整数")
                self.string_key_input.setValidator(self.string_key_validator_numeric)
                self.file_key_input.setValidator(self.file_key_validator_numeric)
            # DES ——已完成
            elif button == 13:
                self.string_encrypt_button.clicked.disconnect()
                self.string_decrypt_button.clicked.disconnect()
                self.file_encrypt_button.clicked.disconnect()
                self.file_decrypt_button.clicked.disconnect()
                self.string_encrypt_button.clicked.connect(
                    self.des_encrypt_string_button_clicked
                )
                self.string_decrypt_button.clicked.connect(
                    self.des_decrypt_string_button_clicked
                )
                self.file_encrypt_button.clicked.connect(
                    self.des_encrypt_file_button_clicked
                )
                self.file_decrypt_button.clicked.connect(
                    self.des_decrypt_file_button_clicked
                )
                self.string_key_input.setText("")
                self.file_key_input.setText("")
                self.string_plain_text_edit.setPlainText("")
                self.string_cipher_text_edit.setPlainText("")
                self.file_encrypt_input_path_edit.setText("")
                self.file_encrypt_output_path_edit.setText("")
                self.file_decrypt_input_path_edit.setText("")
                self.file_decrypt_output_path_edit.setText("")
                self.current_cipher_label.setText("DES")
                self.file_algorithm_label.setText("DES")
                self.string_key_input.setMaxLength(8)
                self.string_key_input.setPlaceholderText(
                    "8个字符，仅限大小写字母、数字的组合"
                )
                self.file_key_input.setMaxLength(8)
                self.file_key_input.setPlaceholderText(
                    "8个字符，仅限大小写字母、数字的组合"
                )
                self.string_key_input.setValidator(self.string_key_validator_alnum)
                self.file_key_input.setValidator(self.file_key_validator_alnum)
            # AES ——已完成
            elif button == 14:
                self.string_encrypt_button.clicked.disconnect()
                self.string_decrypt_button.clicked.disconnect()
                self.file_encrypt_button.clicked.disconnect()
                self.file_decrypt_button.clicked.disconnect()
                self.string_encrypt_button.clicked.connect(
                    self.aes_encrypt_string_button_clicked
                )
                self.string_decrypt_button.clicked.connect(
                    self.aes_decrypt_string_button_clicked
                )
                self.file_encrypt_button.clicked.connect(
                    self.aes_encrypt_file_button_clicked
                )
                self.file_decrypt_button.clicked.connect(
                    self.aes_decrypt_file_button_clicked
                )
                self.string_key_input.setText("")
                self.file_key_input.setText("")
                self.string_plain_text_edit.setPlainText("")
                self.string_cipher_text_edit.setPlainText("")
                self.file_encrypt_input_path_edit.setText("")
                self.file_encrypt_output_path_edit.setText("")
                self.file_decrypt_input_path_edit.setText("")
                self.file_decrypt_output_path_edit.setText("")
                self.current_cipher_label.setText("AES")
                self.file_algorithm_label.setText("AES")
                self.string_key_input.setMaxLength(8)
                self.string_key_input.setPlaceholderText(
                    "8个字符，仅限大小写字母、数字的组合"
                )
                self.file_key_input.setMaxLength(8)
                self.file_key_input.setPlaceholderText(
                    "8个字符，仅限大小写字母、数字的组合"
                )
                self.string_key_input.setValidator(self.string_key_validator_alnum)
                self.file_key_input.setValidator(self.file_key_validator_alnum)
        # 古典密码
        else:
            self.cipher_with_key_frame.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # 凯撒 ——已完成
            if button == 0:
                # 范式
                # 连接部分
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.caesar_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.caesar_decrypt_button_clicked)
                # 初始化各部件
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                # 密码提示
                self.label.setText("凯撒密码")
                # 输入框提示
                self.input_key.setPlaceholderText(
                    "请输入偏移位数，仅限数字，不能超过26"
                )
                # 输入限制，正则表达式在主界面定义
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_numeric)
            # 关键字 ——已完成
            elif button == 1:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.keyword_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.keyword_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("关键字密码")
                self.input_key.setPlaceholderText("请输入关键字，只能为大小写字母")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # 仿射 ——已完成
            elif button == 2:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.affine_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.affine_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("仿射密码")
                self.input_key.setPlaceholderText(
                    "请输入a和b(仅限数字)，以一个(空格)分隔"
                )
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_numeric_space)
            # 多边 ——已完成
            elif button == 3:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.multilateral_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.multilateral_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("多边密码")
                self.input_key.setPlaceholderText("请输入密钥，仅限5位大小写字母")
                self.input_key.setMaxLength(5)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # 维吉尼亚 ——已完成
            elif button == 4:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.vigenere_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.vigenere_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("维吉尼亚")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # Autokey密 ——已完成
            elif button == 5:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.autokey_ciphertext_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.autokey_ciphertext_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("Autokey密")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # Autokey明 ——已完成
            elif button == 6:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.autokey_plaintext_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.autokey_plaintext_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("Autokey明")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # 波雷费 ——已完成
            elif button == 7:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.playfair_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.playfair_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("波雷费密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # 置换 ——已完成
            elif button == 8:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.permutation_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.permutation_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("置换密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为数字")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_numeric)
            # 列置换 ——已完成
            elif button == 9:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.column_permutation_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.column_permutation_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("列置换密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha)
            # 双重置换 ——已完成
            elif button == 10:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(
                    self.double_transposition_encrypt_button_clicked
                )
                self.decrypt_button.clicked.connect(
                    self.double_transposition_decrypt_button_clicked
                )
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("双重置换")
                self.input_key.setPlaceholderText(
                    "请输入a和b(仅限大小写字母)，以一个空格分隔"
                )
                self.input_key.setMaxLength(65535)
                self.input_key.setValidator(self.classical_key_validator_alpha_space)
