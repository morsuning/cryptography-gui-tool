# -*- coding: utf-8 -*-
from copy import copy
from PyQt5 import QtCore
from PyQt5.QtCore import QSignalMapper, QObject, Qt
from PyQt5.QtWidgets import QFileDialog, QLineEdit
from algorithm.hash_algorithm import md5_file, md5_string
from algorithm.classical_cipher import caesar_cipher, keyword_cipher, \
    affine_cipher, multilateral_cipher, vigenere_cipher, permutation_cipher, \
    column_permutation_cipher, autokey_plaintext_cipher
from algorithm.block_cipher import des_cipher
from algorithm.block_cipher.AES import aes_string, aes_file
from algorithm.stream_cipher import rc4_cipher

from demo import UiMainWindow


class Event(UiMainWindow, QObject):

    def __init__(self, main_window):
        super().__init__(main_window)

        self.md5_file_name = ""
        self.import_plaintext_button_file_name = ""
        self.export_ciphertext_button_file_name = ""

        self._window_switch_signal = QtCore.pyqtSignal(str)
        self.button_mapper = QSignalMapper(self)
        self.show_base_frame = True
        self.is_show_widgets = True
        self.default_page_set()
        self.setup_mapper()
        self.setup_mapper()
        self.setup_connect()

    def setup_mapper(self):
        self.button_mapper.setMapping(self.kaisa, 0)
        self.button_mapper.setMapping(self.guanjianzi, 1)
        self.button_mapper.setMapping(self.fangshe, 2)
        self.button_mapper.setMapping(self.duobian, 3)
        self.button_mapper.setMapping(self.weijiniya, 4)
        self.button_mapper.setMapping(self.autokeymi, 5)
        self.button_mapper.setMapping(self.autokeyming, 6)
        self.button_mapper.setMapping(self.boleifei, 7)
        self.button_mapper.setMapping(self.zhihuan, 8)
        self.button_mapper.setMapping(self.liezhihuan, 9)
        self.button_mapper.setMapping(self.shuangchongzhihuan, 10)

        self.button_mapper.setMapping(self.RC4, 11)
        self.button_mapper.setMapping(self.CA, 12)

        self.button_mapper.setMapping(self.DES, 13)
        self.button_mapper.setMapping(self.AES, 14)

        self.button_mapper.setMapping(self.RSA, 15)
        self.button_mapper.setMapping(self.ECC, 16)

        self.button_mapper.setMapping(self.MD5, 17)

    def setup_connect(self):

        # self.connect(self.button_mapper, self.SIGNAL("mapped(int)"), self.show_widgets)
        # self.connect(self.kaisa, self.SIGNAL("clicked()"), self.button_mapper, self.SLOT("map()"))

        self.button_mapper.mapped.connect(self.show_widgets)

        self.kaisa.toggled['bool'].connect(self.button_mapper.map)
        self.guanjianzi.toggled['bool'].connect(self.button_mapper.map)
        self.fangshe.toggled['bool'].connect(self.button_mapper.map)
        self.duobian.toggled['bool'].connect(self.button_mapper.map)
        self.weijiniya.toggled['bool'].connect(self.button_mapper.map)
        self.autokeymi.toggled['bool'].connect(self.button_mapper.map)
        self.autokeyming.toggled['bool'].connect(self.button_mapper.map)
        self.boleifei.toggled['bool'].connect(self.button_mapper.map)
        self.zhihuan.toggled['bool'].connect(self.button_mapper.map)
        self.liezhihuan.toggled['bool'].connect(self.button_mapper.map)
        self.shuangchongzhihuan.toggled['bool'].connect(self.button_mapper.map)
        self.RC4.toggled['bool'].connect(self.button_mapper.map)
        self.CA.toggled['bool'].connect(self.button_mapper.map)
        self.DES.toggled['bool'].connect(self.button_mapper.map)
        self.AES.toggled['bool'].connect(self.button_mapper.map)
        self.RSA.toggled['bool'].connect(self.button_mapper.map)
        self.ECC.toggled['bool'].connect(self.button_mapper.map)
        self.MD5.toggled['bool'].connect(self.button_mapper.map)

        # Default
        self.encrypt_button.clicked.connect(self.default_clicked)
        self.decrypt_button.clicked.connect(self.default_clicked)
        self.encrypt_button_2.clicked.connect(self.default_clicked)
        self.decrypt_button_2.clicked.connect(self.default_clicked)
        self.encrypt_button_3.clicked.connect(self.default_clicked)
        self.decrypt_button_3.clicked.connect(self.default_clicked)
        self.encrypt_button_6.clicked.connect(self.default_clicked)
        self.decrypt_button_6.clicked.connect(self.default_clicked)
        self.encrypt_button_7.clicked.connect(self.default_clicked)
        self.decrypt_button_7.clicked.connect(self.default_clicked)



        # MD5
        self.import_file_toolbox.clicked.connect(self.import_file_toolbox_clicked)
        self.pushButton.clicked.connect(self.md5_clicked)

        # 流密码+分组密码
        self.check_key_2.stateChanged.connect(self.check_key_2_click)


        # 公钥密码

        # 古典密码
        self.import_plaintext_button.clicked.connect(self.import_plaintext_button_clicked)
        self.export_ciphertext_button.clicked.connect(self.export_ciphertext_button_clicked)
        self.check_key.stateChanged.connect(self.check_key_click)

    def default_page_set(self):
        self.switch_sd.setCurrentIndex(0)
        self.cipher_switch_toolbox.setCurrentIndex(0)
        self.classical_cipher_switch.setCurrentIndex(0)
        self.switch_mode_with_key_tabwidget.setCurrentIndex(0)
        self.switch_mode_without_key_tabwidget.setCurrentIndex(0)

    def default_clicked(self):
        pass

    def send_window_switch_signal(self):
        self._window_switch_signal.emit()

    def import_file_toolbox_clicked(self):
        self.md5_file_name, file_type = QFileDialog.\
            getOpenFileName(self, '请选择要加密的文件', '',)
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
        if self.check_key.checkState() == Qt.Checked:
            self.input_key.setEchoMode(QLineEdit.Normal)
        if self.check_key.checkState() == Qt.Unchecked:
            self.input_key.setEchoMode(QLineEdit.Password)

    def check_key_2_click(self):
        if self.check_key_2.checkState() == Qt.Checked:
            self.input_key_2.setEchoMode(QLineEdit.Normal)
        if self.check_key_2.checkState() == Qt.Unchecked:
            self.input_key_2.setEchoMode(QLineEdit.Password)

    def import_plaintext_button_clicked(self):
        self.import_plaintext_button_file_name, import_plaintext_button_file_type = QFileDialog.\
            getOpenFileName(self, "请选择要导入的文件", '', )
        if not self.import_plaintext_button_file_name:
            return
        else:
            try:
                f = open(self.import_plaintext_button_file_name, "r")
                self.statusbar.showMessage(
                    "已成功从" + self.import_plaintext_button_file_name + "导入文件", 2000)
                self.plain_text_edit.setPlainText(f.read())
            except (UnicodeDecodeError, IOError):
                self.statusbar.showMessage(
                    "打开文件" + self.import_plaintext_button_file_name + "失败，可能不是文本文件或非“UTF-8”编码", 5000)
            finally:
                f.close()

    def export_ciphertext_button_clicked(self):
        self.export_ciphertext_button_file_name, export_plaintext_button_file_type = QFileDialog. \
            getOpenFileName(self, "导出至", '', )
        if not self.export_ciphertext_button_file_name:
            return
        else:
            try:
                f = open(self.export_ciphertext_button_file_name, "a")
                if not self.cipher_text_edit.toPlainText():
                    self.statusbar.showMessage("没有密文可以被写入", 5000)
                else:
                    # TODO 解决非ascii字符问题
                    f.write("\n" + self.cipher_text_edit.toPlainText())
                    self.statusbar.showMessage(
                        "已成功将密文写入" + self.export_ciphertext_button_file_name, 2000)
            except Exception:
                self.statusbar.showMessage(
                    "打开或写入" + self.export_ciphertext_button_file_name + "文件失败", 5000)
            finally:
                f.close()

    def caesar_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    caesar_cipher.caesar_encrypt(self.plain_text_edit.toPlainText(),
                                                 int(self.input_key.text()))
                )
                self.statusbar.showMessage("加密成功", 2000)

    def keyword_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                keyword_cipher_text, key = keyword_cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text())
                self.cipher_text_edit.setPlainText(keyword_cipher_text)
                self.statusbar.showMessage("加密成功", 2000)

    # TODO
    def affine_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                for i in self.input_key.text():
                    if i == " ":
                        index = self.input_key.text().index(i)
                a = int(self.input_key.text()[:index])
                b = int(self.input_key.text()[index+1:])
                self.cipher_text_edit.setPlainText(
                    affine_cipher.affine_encrypt(self.plain_text_edit.toPlainText(), a, b))
                self.statusbar.showMessage("加密成功", 2000)

    # TODO
    def multilateral_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    multilateral_cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text()))
                self.statusbar.showMessage("加密成功", 2000)

    def vigenere_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    vigenere_cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text()))
                self.statusbar.showMessage("加密成功", 2000)

    # TODO Autokeymi

    def autokey_plaintext_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    autokey_plaintext_cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text()))
                self.statusbar.showMessage("加密成功", 2000)

    # TODO
    def playfair_encrypt_button_clicked(self):
        pass

    def permutation_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = permutation_cipher.PermutationCipher()
                self.cipher_text_edit.setPlainText(
                    cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text())
                    )
                self.statusbar.showMessage("加密成功", 2000)

    def column_permutation_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = column_permutation_cipher.ColumnPermutationCipher()
                self.cipher_text_edit.setPlainText(
                    cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text())
                    )
                self.statusbar.showMessage("加密成功", 2000)

    # TODO 双重置换

    def caesar_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    caesar_cipher.caesar_decrypt(self.cipher_text_edit.toPlainText(),
                                                 int(self.input_key.text()))
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
                    keyword_cipher.decrypt(self.cipher_text_edit.toPlainText(),
                                            self.input_key.text()))
                self.statusbar.showMessage("解密成功", 2000)

    def affine_decrypt_button_clicked(self):
        pass

    def multilateral_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                # TODO try...catch...finally
                self.plain_text_edit.setPlainText(
                    multilateral_cipher.decrypt(self.cipher_text_edit.toPlainText(),
                                            self.input_key.text()))
                self.statusbar.showMessage("解密成功", 2000)

    def vigenere_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    vigenere_cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
                )
                self.statusbar.showMessage("解密成功", 2000)

    # TODO 两个Autokey
    def autokey_plaintext_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    autokey_plaintext_cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
                )
                self.statusbar.showMessage("解密成功", 2000)

    def playfair_decrypt_button_clicked(self):
        pass

    def permutation_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = permutation_cipher.PermutationCipher()
                self.plain_text_edit.setPlainText(
                    cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
                )
                self.statusbar.showMessage("解密成功", 2000)

    def column_permutation_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = column_permutation_cipher.ColumnPermutationCipher()
                self.plain_text_edit.setPlainText(
                    cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
                )
                self.statusbar.showMessage("解密成功", 2000)

    # TODO 双重置换

    def des_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    cipher = des_cipher.DESCipher()
                    cipher.new(self.input_key_2.text())
                    self.cipher_text_edit_2.setPlainText(
                        cipher.encrypt_string(self.plain_text_edit_2.toPlainText())
                        )
                    self.statusbar.showMessage("加密成功", 2000)

    def des_encrypt_file_button_clicked(self):
        pass

    def aes_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    self.cipher_text_edit_2.setPlainText(
                        aes_string.encrypt(self.plain_text_edit_2.toPlainText(), self.input_key_2.text())
                        )
                    self.statusbar.showMessage("加密成功", 2000)

    def aes_encrypt_file_button_clicked(self):
        pass

    def rc4_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    cipher = rc4_cipher.RC4()
                    self.cipher_text_edit_2.setPlainText(
                        cipher.encrypt(self.input_key_2.text(), self.plain_text_edit_2.toPlainText())
                        )
                    self.statusbar.showMessage("加密成功", 2000)

    def rc4_encrypt_file_button_clicked(self):
        pass

    def ca_encrypt_string_button_clicked(self):
        pass

    def ca_encrypt_file_button_clicked(self):
        pass

    def des_decrypt_string_button_clicked(self):
        if not self.cipher_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    cipher = des_cipher.DESCipher()
                    cipher.new(self.input_key_2.text())
                    self.plain_text_edit_2.setPlainText(
                        cipher.decrypt_string(self.cipher_text_edit_2.toPlainText())
                        )
                    self.statusbar.showMessage("解密成功", 2000)

    def aes_decrypt_string_button_clicked(self):
        if not self.cipher_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    self.plain_text_edit_2.setPlainText(
                        aes_string.decrypt(self.cipher_text_edit_2.toPlainText(), self.input_key_2.text())
                        )
                    self.statusbar.showMessage("解密成功", 2000)

    def rc4_decrypt_string_button_clicked(self):
        if not self.cipher_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = rc4_cipher.RC4()
                self.plain_text_edit_2.setPlainText(
                    cipher.decrypt()
                    )
                self.statusbar.showMessage("解密成功", 2000)

    def ca_decrypt_string_button_clicked(self):
        pass

    def des_decrypt_file_button_clicked(self):
        pass

    def aes_decrypt_file_button_clicked(self):
        pass

    def rc4_decrypt_file_button_clicked(self):
        pass

    def ca_decrypt_file_button_clicked(self):
        pass

    # 决定显示4个窗口中的哪一个，并改变相应控件，需在此更新部分连接
    def show_widgets(self, button):
        print(button)
        self.base_frame.setVisible(not self.is_show_widgets)
        # MD5
        if button == 17:
            self.md5_frame.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets

        elif button == 15 or button == 16:
            self.switch_mode_without_key_tabwidget.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # RSA
            if button == 15:
                self.what_algorithm_2.setText("RSA")
                self.current_cipher_label_3.setText("RSA")
            # ECC
            elif button == 16:
                self.what_algorithm_2.setText("ECC")
                self.current_cipher_label_3.setText("ECC")
        elif button == 11 or button == 12 \
                or button == 13 or button == 14:
            self.switch_mode_with_key_tabwidget.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # RC4
            if button == 11:
                self.encrypt_button_2.clicked.disconnect()
                self.decrypt_button_2.clicked.disconnect()
                self.encrypt_button_3.clicked.disconnect()
                self.decrypt_button_3.clicked.disconnect()
                self.encrypt_button_2.clicked.connect(self.rc4_encrypt_string_button_clicked)
                self.decrypt_button_2.clicked.connect(self.rc4_decrypt_string_button_clicked)
                self.encrypt_button_3.clicked.connect(self.rc4_encrypt_file_button_clicked)
                self.decrypt_button_3.clicked.connect(self.rc4_decrypt_file_button_clicked)
                self.current_cipher_label.setText("RC4")
                self.what_algorithm.setText("RC4")
            # CA
            elif button == 12:
                self.encrypt_button_2.clicked.disconnect()
                self.decrypt_button_2.clicked.disconnect()
                self.encrypt_button_3.clicked.disconnect()
                self.decrypt_button_3.clicked.disconnect()
                self.encrypt_button_2.clicked.connect(self.ca_encrypt_string_button_clicked)
                self.decrypt_button_2.clicked.connect(self.ca_decrypt_string_button_clicked)
                self.encrypt_button_3.clicked.connect(self.ca_encrypt_file_button_clicked)
                self.decrypt_button_3.clicked.connect(self.ca_decrypt_file_button_clicked)
                self.current_cipher_label.setText("CA")
                self.what_algorithm.setText("CA")
            # DES --done
            elif button == 13:
                self.encrypt_button_2.clicked.disconnect()
                self.decrypt_button_2.clicked.disconnect()
                self.encrypt_button_3.clicked.disconnect()
                self.decrypt_button_3.clicked.disconnect()
                self.encrypt_button_2.clicked.connect(self.des_encrypt_string_button_clicked)
                self.decrypt_button_2.clicked.connect(self.des_decrypt_string_button_clicked)
                self.encrypt_button_3.clicked.connect(self.des_encrypt_file_button_clicked)
                self.decrypt_button_3.clicked.connect(self.des_decrypt_file_button_clicked)
                self.current_cipher_label.setText("DES")
                self.what_algorithm.setText("DES")
                self.input_key_2.setMaxLength(8)
                self.input_key_2.setPlaceholderText("8个字符，仅限大小写字母、数字的组合")
                self.input_key_3.setMaxLength(8)
                self.input_key_3.setPlaceholderText("8个字符，仅限大小写字母、数字的组合")
                self.input_key_2.setValidator(self.block_validator_1)
                self.input_key_3.setValidator(self.block_validator_2)
            # AES  --done
            elif button == 14:
                self.encrypt_button_2.clicked.disconnect()
                self.decrypt_button_2.clicked.disconnect()
                self.encrypt_button_3.clicked.disconnect()
                self.decrypt_button_3.clicked.disconnect()
                self.encrypt_button_2.clicked.connect(self.aes_encrypt_string_button_clicked)
                self.decrypt_button_2.clicked.connect(self.aes_decrypt_string_button_clicked)
                self.encrypt_button_3.clicked.connect(self.aes_encrypt_file_button_clicked)
                self.decrypt_button_3.clicked.connect(self.aes_decrypt_file_button_clicked)
                self.current_cipher_label.setText("AES")
                self.what_algorithm.setText("AES")
                self.input_key_2.setMaxLength(8)
                self.input_key_2.setPlaceholderText("8个字符，仅限大小写字母、数字的组合")
                self.input_key_3.setMaxLength(8)
                self.input_key_3.setPlaceholderText("8个字符，仅限大小写字母、数字的组合")
                self.input_key_2.setValidator(self.block_validator_1)
                self.input_key_3.setValidator(self.block_validator_2)
        # 古典密码
        else:
            self.cipher_with_key_frame.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # 凯撒
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
                self.input_key.setPlaceholderText("请输入偏移位数，仅限数字，不能超过26")
                # 输入限制，正则表达式在主界面定义
                self.input_key.setValidator(self.classical_validator_2)
            # 关键字
            elif button == 1:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.keyword_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.keyword_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("关键字密码")
                self.input_key.setPlaceholderText("请输入关键字，只能为大小写英文字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 仿射
            elif button == 2:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.affine_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.affine_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("仿射密码")
                self.input_key.setPlaceholderText("请输入a和b(仅限数字)，以一个" "(空格)分隔")
                self.input_key.setValidator(self.classical_validator_4)
            # 多边
            elif button == 3:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.multilateral_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.multilateral_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("多边密码")
                self.input_key.setMaxLength(5)
                self.input_key.setPlaceholderText("请输入密钥，仅限5位英文大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 维吉尼亚
            elif button == 4:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.vigenere_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.vigenere_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("维吉尼亚")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写英文字母")
                self.input_key.setValidator(self.classical_validator_3)
            # Autokey密
            elif button == 5:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.default_clicked)
                self.decrypt_button.clicked.connect(self.default_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                # TODO
                self.label.setText("Autokey密")
            # Autokey明
            elif button == 6:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.autokey_plaintext_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.autokey_plaintext_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("Autokey明")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写英文字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 波雷费
            elif button == 7:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.playfair_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.playfair_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("波雷费密码")
            # 置换
            elif button == 8:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.permutation_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.permutation_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("置换密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为数字")
                self.input_key.setValidator(self.classical_validator_2)
            # 列置换
            elif button == 9:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.column_permutation_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.column_permutation_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("列置换密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写英文字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 双重置换
            elif button == 10:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.default_clicked)
                self.decrypt_button.clicked.connect(self.default_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                # TODO
                self.label.setText("双重置换")



