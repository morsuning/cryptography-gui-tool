# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore
from PyQt5.QtCore import QSignalMapper, QObject, Qt
from PyQt5.QtWidgets import QFileDialog, QLineEdit
from algorithm.hash_algorithm import md5_file, md5_string
from algorithm.classical_cipher import caesar_cipher, keyword_cipher, \
    affine_cipher, multilateral_cipher, vigenere_cipher, permutation_cipher, \
    column_permutation_cipher, autokey_plaintext_cipher, autokey_ciphertext_cipher, \
    double_transposition_cipher, playfair_cipher
from algorithm.block_cipher import des_cipher
from algorithm.block_cipher.aes import aes_string, aes_file
from algorithm.stream_cipher import rc4_cipher
from algorithm.stream_cipher.ca import ca_string, ca_file
from algorithm.public_cipher.rsa import rsa
from algorithm.public_cipher.ecc import ecc

from ui.demo import UiMainWindow


class Event(UiMainWindow, QObject):

    def __init__(self, main_window):
        super().__init__(main_window)
        self.about.setText("算法：\n陈星辰 郭明磊\n杨晨 杨雨铮\n薛晨阳\n界面：\n薛晨阳\n美化：\n杨晨")
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
        # 连接的另一种写法
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
        self.generate_keypair_button.clicked.connect(self.default_clicked)
        self.generate_keypair_button_2.clicked.connect(self.default_clicked)

        # 各界面通用部件

        # MD5
        self.import_file_toolbox.clicked.connect(self.import_file_toolbox_clicked)
        self.pushButton.clicked.connect(self.md5_clicked)

        # 流密码+分组密码
        self.check_key_2.stateChanged.connect(self.check_key_2_click)
        self.check_key_3.stateChanged.connect(self.check_key_3_click)
        self.import_plaintext_button_2.clicked.connect(self.import_plaintext_button_clicked)
        self.export_ciphertext_button_2.clicked.connect(self.export_ciphertext_button_clicked)
        self.import_file_button.clicked.connect(self.import_file_button_clicked)
        self.path_button.clicked.connect(self.path_button_clicked)
        self.toolButton_3.clicked.connect(self.tool_button_3_clicked)
        self.path_button_2.clicked.connect(self.path_button_2_clicked)

        # 公钥密码
        self.import_plaintext_button_4.clicked.connect(self.import_plaintext_button_clicked)
        self.export_ciphertext_button_4.clicked.connect(self.export_ciphertext_button_clicked)
        self.import_file_button_3.clicked.connect(self.import_file_button_3_clicked)
        self.path_button_5.clicked.connect(self.path_button_5_clicked)
        self.toolButton_5.clicked.connect(self.tool_button_5_clicked)
        self.path_button_6.clicked.connect(self.path_button_6_clicked)

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

    def import_file_button_clicked(self):
        self.file_to_encrypt_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要导入的文件", '', )
        f = None
        try:
            f = open(self.file_to_encrypt_name, 'r')
            self.import_file_path_edit.setText(self.file_to_encrypt_name)
            self.statusbar.showMessage("导入文件" + self.file_to_encrypt_name + "成功", 2000)
        except Exception:
            self.statusbar.showMessage("文件导入失败", 5000)
        finally:
            if f:
                f.close()

    def import_file_button_3_clicked(self):
        self.file_to_encrypt_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要导入的文件", '', )
        f = None
        try:
            f = open(self.file_to_encrypt_name, 'r')
            self.import_file_path_edit_3.setText(self.file_to_encrypt_name)
            self.statusbar.showMessage("导入文件" + self.file_to_encrypt_name + "成功", 2000)
        except Exception:
            self.statusbar.showMessage("文件导入失败", 5000)
        finally:
            if f:
                f.close()

    def path_button_clicked(self):
        self.encrypted_file_to_save_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要保存到的文件", '', )
        self.save_path_label.setText(self.encrypted_file_to_save_name)
        self.statusbar.showMessage("加密后的文件将保存为" + self.encrypted_file_to_save_name, 5000)

    def path_button_5_clicked(self):
        self.encrypted_file_to_save_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要保存到的文件", '', )
        self.save_path_label_3.setText(self.encrypted_file_to_save_name)
        self.statusbar.showMessage("加密后的文件将保存为" + self.encrypted_file_to_save_name, 5000)

    def tool_button_3_clicked(self):
        self.file_to_decrypt_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要导入的文件", '', )
        f = None
        try:
            f = open(self.file_to_decrypt_name, 'r')
            self.lineEdit_3.setText(self.file_to_decrypt_name)
            self.statusbar.showMessage("导入文件" + self.file_to_decrypt_name + "成功", 2000)
        except Exception:
            self.statusbar.showMessage("文件导入失败", 5000)
        finally:
            if f:
                f.close()

    def tool_button_5_clicked(self):
        self.file_to_decrypt_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要导入的文件", '', )
        f = None
        try:
            f = open(self.file_to_decrypt_name, 'r')
            self.lineEdit_7.setText(self.file_to_decrypt_name)
            self.statusbar.showMessage("导入文件" + self.file_to_decrypt_name + "成功", 2000)
        except Exception:
            self.statusbar.showMessage("文件导入失败", 5000)
        finally:
            if f:
                f.close()

    def path_button_2_clicked(self):
        self.decrypted_file_to_save_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要保存到的文件", '', )
        self.lineEdit_4.setText(self.decrypted_file_to_save_name)
        self.statusbar.showMessage("解密后的文件将保存为" + self.decrypted_file_to_save_name, 5000)

    def path_button_6_clicked(self):
        self.decrypted_file_to_save_name, file_to_encrypt_type = QFileDialog. \
            getOpenFileName(self, "请选择要保存到的文件", '', )
        self.lineEdit_8.setText(self.decrypted_file_to_save_name)
        self.statusbar.showMessage("解密后的文件将保存为" + self.decrypted_file_to_save_name, 5000)

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

    def check_key_3_click(self):
        if self.check_key_3.checkState() == Qt.Checked:
            self.input_key_3.setEchoMode(QLineEdit.Normal)
        if self.check_key_3.checkState() == Qt.Unchecked:
            self.input_key_3.setEchoMode(QLineEdit.Password)

    def import_plaintext_button_clicked(self):
        self.import_plaintext_button_file_name, import_plaintext_button_file_type = QFileDialog.\
            getOpenFileName(self, "请选择要导入的文件", '', )
        if not self.import_plaintext_button_file_name:
            return
        else:
            f = None
            try:
                f = open(self.import_plaintext_button_file_name, "r")
                self.statusbar.showMessage(
                    "已成功从" + self.import_plaintext_button_file_name + "导入文件", 2000)
                self.plain_text_edit.setPlainText(f.read())
            except (UnicodeDecodeError, IOError):
                self.statusbar.showMessage(
                    "打开文件" + self.import_plaintext_button_file_name + "失败，可能不是文本文件或非“UTF-8”编码", 5000)
            finally:
                if f:
                    f.close()

    def export_ciphertext_button_clicked(self):
        self.export_ciphertext_button_file_name, export_plaintext_button_file_type = QFileDialog. \
            getOpenFileName(self, "导出至", '', )
        if not self.export_ciphertext_button_file_name:
            return
        else:
            f = None
            try:
                f = open(self.export_ciphertext_button_file_name, "a")
                if not self.cipher_text_edit.toPlainText():
                    self.statusbar.showMessage("没有密文可以被写入", 5000)
                else:
                    # TODO 导入导出明文密文 解决非ascii字符问题
                    f.write("\n" + self.cipher_text_edit.toPlainText())
                    self.statusbar.showMessage(
                        "已成功将密文写入" + self.export_ciphertext_button_file_name, 2000)
            except Exception:
                self.statusbar.showMessage(
                    "打开或写入" + self.export_ciphertext_button_file_name + "文件失败", 5000)
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

    def affine_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
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
                b = int(self.input_key.text()[index+1:])
                self.cipher_text_edit.setPlainText(
                    affine_cipher.encrypt(self.plain_text_edit.toPlainText(), a, b))
                self.statusbar.showMessage("加密成功", 2000)

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

    # TODO autokey ciphertext 密钥必须比明文长
    def autokey_ciphertext_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    autokey_plaintext_cipher.encrypt(self.plain_text_edit.toPlainText(), self.input_key.text()))
                self.statusbar.showMessage("加密成功", 2000)

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

    def playfair_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.cipher_text_edit.setPlainText(
                    playfair_cipher.playfair(self.input_key.text(), self.plain_text_edit.toPlainText(), True).lower()
                )
                self.statusbar.showMessage("加密成功", 2000)

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
                self.cipher_text_edit.setPlainText(
                    column_permutation_cipher.encrypt(self.plain_text_edit.toPlainText().replace(" ", ""),
                                                      self.input_key.text())
                    )
                self.statusbar.showMessage("加密成功", 2000)

    def double_transposition_encrypt_button_clicked(self):
        if not self.plain_text_edit.toPlainText():
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
                b = self.input_key.text()[index+1:]
                self.cipher_text_edit.setPlainText(
                    double_transposition_cipher.encrypt(self.plain_text_edit.toPlainText(), a, b))
                self.statusbar.showMessage("加密成功", 2000)

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
                b = self.input_key.text()[index+1:]
                # TODO affine cipher 密码内部缺陷，a,b不能为模26余0的数
                self.plain_text_edit.setPlainText(
                    affine_cipher.decrypt(self.cipher_text_edit.toPlainText(), a, b))
                self.statusbar.showMessage("解密成功", 2000)

    def multilateral_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                # TODO multilateral算法缺陷 ！！无法解密 多边密码
                try:
                    self.plain_text_edit.setPlainText(
                        multilateral_cipher.decrypt(self.cipher_text_edit.toPlainText(),
                                                self.input_key.text()))
                except Exception:
                    self.statusbar.showMessage("解密失败", 5000)
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

    def autokey_ciphertext_decrypt_button_clicked(self):
        if not self.cipher_text_edit.toPlainText():
            return
        else:
            if not self.input_key.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                self.plain_text_edit.setPlainText(
                    autokey_ciphertext_cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
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
                    autokey_plaintext_cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
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
                    playfair_cipher.playfair(self.input_key.text(), self.cipher_text_edit.toPlainText(), False)
                )
                self.statusbar.showMessage("解密成功", 2000)

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
                self.plain_text_edit.setPlainText(
                    column_permutation_cipher.decrypt(self.cipher_text_edit.toPlainText(), self.input_key.text())
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
                b = self.input_key.text()[index+1:]
                self.plain_text_edit.setPlainText(
                    double_transposition_cipher.decrypt(self.cipher_text_edit.toPlainText(), b, a))
                self.statusbar.showMessage("解密成功", 2000)

    def des_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入正确的密钥", 5000)
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
        if not self.import_file_path_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_3.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    cipher = des_cipher.DESCipher()
                    cipher.new(self.input_key_3.text())
                    if not self.save_path_label.text():
                        try:
                            default_encrypted_file_save_path = self.import_file_path_edit.text() + ".encrypted"
                            self.save_path_label.setText(default_encrypted_file_save_path)
                            cipher.encrypt_file(self.import_file_path_edit.text(), default_encrypted_file_save_path)
                            self.statusbar.showMessage("加密成功，文件默认保存至" + default_encrypted_file_save_path, 5000)
                        except Exception:
                            self.statusbar.showMessage("加密失败")
                    else:
                        try:
                            cipher.encrypt_file(self.import_file_path_edit.text(), self.save_path_label.text())
                            self.statusbar.showMessage("加密成功，文件已保存至" + self.save_path_label.text(), 5000)
                        except Exception:
                            self.statusbar.showMessage("加密失败")

    def aes_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入正确的密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    self.cipher_text_edit_2.setPlainText(
                        aes_string.encrypt(self.plain_text_edit_2.toPlainText(), self.input_key_2.text())
                        )
                    self.statusbar.showMessage("加密成功", 2000)

    def aes_encrypt_file_button_clicked(self):
        if not self.import_file_path_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_2.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    if not self.save_path_label.text():
                        try:
                            default_encrypted_file_save_path = self.import_file_path_edit.text() + ".encrypted"
                            self.save_path_label.setText(default_encrypted_file_save_path)
                            aes_file.encrypt(self.import_file_path_edit.text(),
                                             self.input_key_3.text(), default_encrypted_file_save_path)
                            self.statusbar.showMessage("加密成功，文件默认保存至" + default_encrypted_file_save_path, 5000)
                        except Exception:
                            self.statusbar.showMessage("加密失败")
                    else:
                        try:
                            aes_file.encrypt(self.import_file_path_edit.text(),
                                             self.input_key_3.text(), self.save_path_label.text())
                            self.statusbar.showMessage("加密成功，文件已保存至" + self.save_path_label.text(), 5000)
                        except Exception:
                            self.statusbar.showMessage("加密失败")

    def rc4_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = rc4_cipher.RC4()
                self.cipher_text_edit_2.setPlainText(
                    cipher.encrypt(self.input_key_2.text(), self.plain_text_edit_2.toPlainText())
                    )
                self.statusbar.showMessage("加密成功", 2000)

    def rc4_encrypt_file_button_clicked(self):
        if not self.import_file_path_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = rc4_cipher.RC4()
                if not self.save_path_label.text():
                    try:
                        default_encrypted_file_save_path = self.import_file_path_edit.text() + ".encrypted"
                        self.save_path_label.setText(default_encrypted_file_save_path)
                        cipher.encrypt_file(self.import_file_path_edit.text(),
                                            default_encrypted_file_save_path, self.input_key_3.text())
                        self.statusbar.showMessage("加密成功，文件默认保存至" + default_encrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")
                else:
                    try:
                        cipher.encrypt_file(self.import_file_path_edit.text(),
                                            self.save_path_label.text(), self.input_key_3.text())
                        self.statusbar.showMessage("加密成功，文件已保存至" + self.save_path_label.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")

    def ca_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if int(self.input_key_2.text()) > 255 or int(self.input_key_2.text()) < 0:
                    self.statusbar.showMessage("密钥只能为0-255之间的整数", 5000)
                else:
                    self.cipher_text_edit_2.setPlainText(
                        ca_string.encrypt(self.plain_text_edit_2.toPlainText(), int(self.input_key_2.text()))
                        )
                    self.statusbar.showMessage("加密成功", 2000)

    def ca_encrypt_file_button_clicked(self):
        if not self.import_file_path_edit.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if not self.save_path_label.text():
                    try:
                        default_encrypted_file_save_path = self.import_file_path_edit.text() + ".encrypted"
                        self.save_path_label.setText(default_encrypted_file_save_path)
                        ca_file.encrypt(self.import_file_path_edit.text(),
                                        int(self.input_key_3.text()), default_encrypted_file_save_path)
                        self.statusbar.showMessage("加密成功，文件默认保存至" + default_encrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")
                else:
                    try:
                        ca_file.encrypt(self.import_file_path_edit.text(),
                                        int(self.input_key_3.text()), self.save_path_label.text())
                        self.statusbar.showMessage("加密成功，文件已保存至" + self.save_path_label.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")

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
                    cipher.decrypt(self.input_key_2.text(), self.cipher_text_edit_2.toPlainText())
                    )
                self.statusbar.showMessage("解密成功", 2000)

    def ca_decrypt_string_button_clicked(self):
        if not self.cipher_text_edit_2.toPlainText():
            return
        else:
            if not self.input_key_2.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if int(self.input_key_2.text()) > 255 or int(self.input_key_2.text()) < 0:
                    self.statusbar.showMessage("密钥只能为0-255之间的整数", 5000)
                else:
                    self.plain_text_edit_2.setPlainText(
                        ca_string.decrypt(self.cipher_text_edit_2.toPlainText(), int(self.input_key_2.text()))
                        )
                    self.statusbar.showMessage("解密成功", 2000)

    def des_decrypt_file_button_clicked(self):
        if not self.lineEdit_3.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if len(self.input_key_3.text()) != 8:
                    self.statusbar.showMessage("请输入8位密钥", 5000)
                else:
                    cipher = des_cipher.DESCipher()
                    print(self.input_key_3.text())
                    cipher.new(self.input_key_3.text())
                    if not self.lineEdit_4.text():
                        try:
                            default_decrypted_file_save_path = self.lineEdit_3.text() + ".decrypted"
                            self.lineEdit_4.setText(default_decrypted_file_save_path)
                            cipher.decrypt_file(self.lineEdit_3.text(), default_decrypted_file_save_path)
                            self.statusbar.showMessage("解密成功，文件默认保存至" + default_decrypted_file_save_path, 5000)
                        except Exception:
                            self.statusbar.showMessage("解密失败")
                    else:
                        try:
                            cipher.decrypt_file(self.lineEdit_3.text(), self.lineEdit_4.text())
                            self.statusbar.showMessage("解密成功，文件已保存至" + self.lineEdit_4.text(), 5000)
                        except Exception:
                            self.statusbar.showMessage("解密失败")

    def aes_decrypt_file_button_clicked(self):
        if not self.lineEdit_3.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if not self.lineEdit_4.text():
                    try:
                        default_decrypted_file_save_path = self.lineEdit_3.text() + ".decrypted"
                        self.lineEdit_4.setText(default_decrypted_file_save_path)
                        aes_file.decrypt(self.lineEdit_3.text(),
                                         self.input_key_3.text(), default_decrypted_file_save_path)
                        self.statusbar.showMessage("解密成功，文件默认保存至" + default_decrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        aes_file.decrypt(self.lineEdit_3.text(), self.input_key_3.text(), self.lineEdit_4.text())
                        self.statusbar.showMessage("解密成功，文件已保存至" + self.lineEdit_4.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")

    def rc4_decrypt_file_button_clicked(self):
        if not self.lineEdit_3.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                cipher = rc4_cipher.RC4()
                if not self.lineEdit_4.text():
                    try:
                        default_decrypted_file_save_path = self.lineEdit_3.text() + ".decrypted"
                        self.lineEdit_4.setText(default_decrypted_file_save_path)
                        cipher.decrypt_file(default_decrypted_file_save_path,
                                            self.lineEdit_3.text(), self.input_key_3.text())
                        self.statusbar.showMessage("解密成功，文件默认保存至" + default_decrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        cipher.decrypt_file(self.lineEdit_4.text(),
                                            self.lineEdit_3.text(), self.input_key_3.text())
                        self.statusbar.showMessage("解密成功，文件已保存至" + self.lineEdit_4.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")

    def ca_decrypt_file_button_clicked(self):
        if not self.lineEdit_3.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.input_key_3.text():
                self.statusbar.showMessage("请输入密钥", 5000)
            else:
                if not self.lineEdit_4.text():
                    try:
                        default_decrypted_file_save_path = self.lineEdit_3.text() + ".decrypted"
                        self.lineEdit_4.setText(default_decrypted_file_save_path)
                        ca_file.decrypt(self.lineEdit_3.text(),
                                        int(self.input_key_3.text()), default_decrypted_file_save_path)
                        self.statusbar.showMessage("解密成功，文件默认保存至" + default_decrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        ca_file.decrypt(self.lineEdit_3.text(),
                                        int(self.input_key_3.text()), self.lineEdit_4.text())
                        self.statusbar.showMessage("解密成功，文件已保存至" + self.lineEdit_4.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")

    def rsa_generate_keypair_button_clicked(self):
        # private key: d
        # public key: e n
        e, n, d = rsa.RSA()
        self.show_keypair_text.setText(str(d))
        self.show_keypair_text_2.setText(str(d))
        self.rsa_public_key_file_name = "rsa_public_key_" + os.urandom(10).hex()
        f = None
        try:
            f = open(self.rsa_public_key_file_name, 'w')
            f.writelines([str(e)+'\n', str(n)+'\n'])
            self.statusbar.showMessage(
                "成功生成RSA公钥和私钥，公钥已保存至" + self.rsa_public_key_file_name, 5000)
        except Exception:
            self.statusbar.showMessage(
                "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
        finally:
            if f:
                f.close()

    def rsa_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_4.toPlainText():
            return
        else:
            if not self.show_keypair_text.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                f = None
                try:
                    f = open(self.rsa_public_key_file_name, 'r')
                    e = f.readline()
                    n = f.readline()
                    self.cipher_text_edit_4.setPlainText(
                        rsa.encrypt(int(e), int(n), self.plain_text_edit_4.toPlainText())
                    )
                    self.statusbar.showMessage("加密成功", 2000)
                except (IOError, Exception):
                    if IOError:
                        self.statusbar.showMessage(
                            "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
                    self.statusbar.showMessage("加密时出错", 5000)
                finally:
                    if f:
                        f.close()

    def rsa_decrypt_string_button_clicked(self):
        if not self.cipher_text_edit_4.toPlainText():
            return
        else:
            f = None
            try:
                f = open(self.rsa_public_key_file_name, 'r')
                e = f.readline()
                n = f.readline()
                d = self.show_keypair_text.toPlainText()
                self.plain_text_edit_4.setPlainText(
                    rsa.decrypt(int(d), int(n), self.cipher_text_edit_4.toPlainText())
                )
                self.statusbar.showMessage("解密成功", 2000)
            except Exception:
                self.statusbar.showMessage("解密时出错", 5000)
            finally:
                if f:
                    f.close()

    def rsa_encrypt_file_button_clicked(self):
        if not self.import_file_path_edit_3.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.show_keypair_text_2.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                if not self.save_path_label_3.text():
                    try:
                        default_encrypted_file_save_path = self.import_file_path_edit_3.text() + ".encrypted"
                        self.save_path_label_3.setText(default_encrypted_file_save_path)
                        f = None
                        try:
                            f = open(self.rsa_public_key_file_name, 'r')
                            e = f.readline()
                            n = f.readline()
                            rsa.encode_file(int(e), int(n),
                                            self.import_file_path_edit_3.text(), default_encrypted_file_save_path)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("加密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("加密成功，文件默认保存至" + default_encrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")
                else:
                    try:
                        f = None
                        try:
                            f = open(self.rsa_public_key_file_name, 'r')
                            e = f.readline()
                            n = f.readline()
                            rsa.encode_file(int(e), int(n),
                                            self.import_file_path_edit_3.text(), self.save_path_label_3.text())
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("加密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("加密成功，文件已保存至" + self.save_path_label_3.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")

    def rsa_decrypt_file_button_clicked(self):
        if not self.lineEdit_7.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.show_keypair_text_2.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                if not self.lineEdit_8.text():
                    try:
                        default_decrypted_file_save_path = self.lineEdit_7.text() + ".decrypted"
                        self.lineEdit_8.setText(default_decrypted_file_save_path)
                        d = self.show_keypair_text_2.toPlainText()
                        f = None
                        try:
                            f = open(self.rsa_public_key_file_name, 'r')
                            e = f.readline()
                            n = f.readline()
                            rsa.decode_file(int(d), int(n), self.lineEdit_7.text(), default_decrypted_file_save_path)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("解密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("解密成功，文件默认保存至" + default_decrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        d = self.show_keypair_text_2.toPlainText()
                        f = None
                        try:
                            f = open(self.rsa_public_key_file_name, 'r')
                            e = f.readline()
                            n = f.readline()
                            rsa.decode_file(int(d), int(n), self.lineEdit_7.text(), self.lineEdit_8.text())
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("解密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("解密成功，文件已保存至" + self.lineEdit_8.text(), 5000)
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
            f = open(self.ecc_public_key_file_name, 'w')
            f.writelines([str(public_key[0]) + '\n', str(public_key[1]) + '\n'])
            self.statusbar.showMessage(
                "成功生成ECC公钥和私钥，公钥已保存至" + self.ecc_public_key_file_name, 5000)
        except Exception:
            self.statusbar.showMessage(
                "打开或写入" + self.ecc_public_key_file_name + "文件失败", 5000)
        finally:
            if f:
                f.close()

    def ecc_encrypt_string_button_clicked(self):
        if not self.plain_text_edit_4.toPlainText():
            return
        else:
            if not self.show_keypair_text.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                f = None
                try:
                    f = open(self.ecc_public_key_file_name, 'r')
                    x = f.readline()
                    y = f.readline()
                    cipher = ecc.EccCipher()
                    self.ecc_result = cipher.encrypt(self.plain_text_edit_4.toPlainText().encode('utf-8'))
                    self.cipher_text_edit_4.setPlainText(
                        self.ecc_result.hex()
                    )
                    self.statusbar.showMessage("加密成功", 2000)
                except (IOError, Exception):
                    if IOError:
                        self.statusbar.showMessage(
                            "打开文件" + self.ecc_public_key_file_name + "失败", 5000)
                    self.statusbar.showMessage("加密时出错", 5000)
                finally:
                    if f :
                        f.close()

    def ecc_decrypt_string_button_clicked(self):
        if not self.cipher_text_edit_4.toPlainText():
            return
        else:
            f = None
            try:
                f = open(self.ecc_public_key_file_name, 'r')
                x = f.readline()
                y = f.readline()
                private_key = self.show_keypair_text.toPlainText()
                cipher = ecc.EccCipher()
                self.plain_text_edit_4.setPlainText(
                    cipher.decrypt(self.ecc_result).decode('utf-8')
                )
                self.statusbar.showMessage("解密成功", 2000)
            except Exception:
                self.statusbar.showMessage("解密时出错", 5000)
            finally:
                if f:
                    f.close()

    def ecc_encrypt_file_button_clicked(self):
        if not self.import_file_path_edit_3.text():
            self.statusbar.showMessage("请选择要加密的文件！", 5000)
            return
        else:
            if not self.show_keypair_text_2.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                if not self.save_path_label_3.text():
                    try:
                        default_encrypted_file_save_path = self.import_file_path_edit_3.text() + ".encrypted"
                        self.save_path_label_3.setText(default_encrypted_file_save_path)
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, 'r')
                            x = f.readline()
                            y = f.readline()
                            with open(self.import_file_path_edit_3.text(), 'rb') as import_file:
                                cipher_text = cipher.encrypt(import_file.read())
                            with open(default_encrypted_file_save_path, 'wb') as save_file:
                                save_file.write(cipher_text)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.ecc_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("加密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("加密成功，文件默认保存至" + default_encrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")
                else:
                    try:
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, 'r')
                            x = f.readline()
                            y = f.readline()
                            with open(self.import_file_path_edit_3.text(), 'rb') as import_file:
                                cipher_text = cipher.encrypt(import_file.read())
                            with open(self.save_path_label_3.text(), 'wb') as save_file:
                                save_file.write(cipher_text)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.rsa_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("加密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("加密成功，文件已保存至" + self.save_path_label_3.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("加密失败")

    def ecc_decrypt_file_button_clicked(self):
        if not self.lineEdit_7.text():
            self.statusbar.showMessage("请选择要解密的文件！", 5000)
            return
        else:
            if not self.show_keypair_text_2.toPlainText():
                self.statusbar.showMessage("请先生成密钥对", 5000)
            else:
                if not self.lineEdit_8.text():
                    try:
                        default_decrypted_file_save_path = self.lineEdit_7.text() + ".decrypted"
                        self.lineEdit_8.setText(default_decrypted_file_save_path)
                        d = self.show_keypair_text_2.toPlainText()
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, 'r')
                            x = f.readline()
                            y = f.readline()
                            with open(self.lineEdit_7.text(), 'rb') as import_file:
                                plaintext = cipher.decrypt(import_file.read())
                            with open(default_decrypted_file_save_path, 'wb') as save_file:
                                save_file.write(plaintext)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.ecc_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("解密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("解密成功，文件默认保存至" + default_decrypted_file_save_path, 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")
                else:
                    try:
                        d = self.show_keypair_text_2.toPlainText()
                        f = None
                        cipher = ecc.EccCipher()
                        try:
                            f = open(self.ecc_public_key_file_name, 'r')
                            x = f.readline()
                            y = f.readline()
                            with open(self.lineEdit_7.text(), 'rb') as import_file:
                                plaintext = cipher.decrypt(import_file.read())
                            with open(self.lineEdit_8.text(), 'wb') as save_file:
                                save_file.write(plaintext)
                        except (IOError, Exception):
                            if IOError:
                                self.statusbar.showMessage(
                                    "打开或写入" + self.ecc_public_key_file_name + "文件失败", 5000)
                            self.statusbar.showMessage("解密时出错", 5000)
                        finally:
                            if f:
                                f.close()
                        self.statusbar.showMessage("解密成功，文件已保存至" + self.lineEdit_8.text(), 5000)
                    except Exception:
                        self.statusbar.showMessage("解密失败")

    # 决定显示4个窗口中的哪一个，并改变相应控件，需在此更新部分连接
    def show_widgets(self, button):
        self.base_frame.setVisible(not self.is_show_widgets)
        # MD5 --done
        if button == 17:
            self.md5_frame.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
        elif button == 15 or button == 16:
            self.switch_mode_without_key_tabwidget.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # RSA --done TODO 已知问题：RSA 字符串解密时会丢掉第一个字符
            if button == 15:
                self.generate_keypair_button.clicked.disconnect()
                self.generate_keypair_button_2.clicked.disconnect()
                self.encrypt_button_6.clicked.disconnect()
                self.decrypt_button_6.clicked.disconnect()
                self.encrypt_button_7.clicked.disconnect()
                self.decrypt_button_7.clicked.disconnect()
                self.generate_keypair_button.clicked.connect(self.rsa_generate_keypair_button_clicked)
                self.generate_keypair_button_2.clicked.connect(self.rsa_generate_keypair_button_clicked)
                self.encrypt_button_6.clicked.connect(self.rsa_encrypt_string_button_clicked)
                self.decrypt_button_6.clicked.connect(self.rsa_decrypt_string_button_clicked)
                self.encrypt_button_7.clicked.connect(self.rsa_encrypt_file_button_clicked)
                self.decrypt_button_7.clicked.connect(self.rsa_decrypt_file_button_clicked)
                self.show_keypair_text.setText("")
                self.show_keypair_text_2.setText("")
                self.plain_text_edit_4.setPlainText("")
                self.cipher_text_edit_4.setPlainText("")
                self.import_file_path_edit_3.setText("")
                self.save_path_label_3.setText("")
                self.lineEdit_7.setText("")
                self.lineEdit_8.setText("")
                self.what_algorithm_2.setText("RSA")
                self.current_cipher_label_3.setText("RSA")
            # ECC --done
            elif button == 16:
                self.generate_keypair_button.clicked.disconnect()
                self.generate_keypair_button_2.clicked.disconnect()
                self.encrypt_button_6.clicked.disconnect()
                self.decrypt_button_6.clicked.disconnect()
                self.encrypt_button_7.clicked.disconnect()
                self.decrypt_button_7.clicked.disconnect()
                self.generate_keypair_button.clicked.connect(self.ecc_generate_keypair_button_clicked)
                self.generate_keypair_button_2.clicked.connect(self.ecc_generate_keypair_button_clicked)
                self.encrypt_button_6.clicked.connect(self.ecc_encrypt_string_button_clicked)
                self.decrypt_button_6.clicked.connect(self.ecc_decrypt_string_button_clicked)
                self.encrypt_button_7.clicked.connect(self.ecc_encrypt_file_button_clicked)
                self.decrypt_button_7.clicked.connect(self.ecc_decrypt_file_button_clicked)
                self.show_keypair_text.setText("")
                self.show_keypair_text_2.setText("")
                self.plain_text_edit_4.setPlainText("")
                self.cipher_text_edit_4.setPlainText("")
                self.import_file_path_edit_3.setText("")
                self.save_path_label_3.setText("")
                self.lineEdit_7.setText("")
                self.lineEdit_8.setText("")
                self.what_algorithm_2.setText("ECC")
                self.current_cipher_label_3.setText("ECC")
        elif button == 11 or button == 12 \
                or button == 13 or button == 14:
            self.switch_mode_with_key_tabwidget.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            # RC4 --done
            if button == 11:
                self.encrypt_button_2.clicked.disconnect()
                self.decrypt_button_2.clicked.disconnect()
                self.encrypt_button_3.clicked.disconnect()
                self.decrypt_button_3.clicked.disconnect()
                self.encrypt_button_2.clicked.connect(self.rc4_encrypt_string_button_clicked)
                self.decrypt_button_2.clicked.connect(self.rc4_decrypt_string_button_clicked)
                self.encrypt_button_3.clicked.connect(self.rc4_encrypt_file_button_clicked)
                self.decrypt_button_3.clicked.connect(self.rc4_decrypt_file_button_clicked)
                self.input_key_2.setText("")
                self.input_key_3.setText("")
                self.plain_text_edit_2.setPlainText("")
                self.cipher_text_edit_2.setPlainText("")
                self.import_file_path_edit.setText("")
                self.save_path_label.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
                self.current_cipher_label.setText("RC4")
                self.what_algorithm.setText("RC4")
                self.input_key_2.setPlaceholderText("仅限大小写字母和数字的组合，不限位数")
                self.input_key_3.setMaxLength(65535)
                self.input_key_3.setPlaceholderText("仅限大小写字母和数字的组合，不限位数")
                self.input_key_3.setMaxLength(65535)
                self.input_key_2.setValidator(self.block_validator_1)
                self.input_key_3.setValidator(self.block_validator_2)
            # CA --done
            elif button == 12:
                self.encrypt_button_2.clicked.disconnect()
                self.decrypt_button_2.clicked.disconnect()
                self.encrypt_button_3.clicked.disconnect()
                self.decrypt_button_3.clicked.disconnect()
                self.encrypt_button_2.clicked.connect(self.ca_encrypt_string_button_clicked)
                self.decrypt_button_2.clicked.connect(self.ca_decrypt_string_button_clicked)
                self.encrypt_button_3.clicked.connect(self.ca_encrypt_file_button_clicked)
                self.decrypt_button_3.clicked.connect(self.ca_decrypt_file_button_clicked)
                self.input_key_2.setText("")
                self.input_key_3.setText("")
                self.plain_text_edit_2.setPlainText("")
                self.cipher_text_edit_2.setPlainText("")
                self.import_file_path_edit.setText("")
                self.save_path_label.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
                self.current_cipher_label.setText("CA")
                self.what_algorithm.setText("CA")
                self.input_key_2.setMaxLength(3)
                self.input_key_2.setPlaceholderText("请输入0-255之间的整数")
                self.input_key_3.setMaxLength(3)
                self.input_key_3.setPlaceholderText("请输入0-255之间的整数")
                self.input_key_2.setValidator(self.block_validator_3)
                self.input_key_3.setValidator(self.block_validator_4)
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
                self.input_key_2.setText("")
                self.input_key_3.setText("")
                self.plain_text_edit_2.setPlainText("")
                self.cipher_text_edit_2.setPlainText("")
                self.import_file_path_edit.setText("")
                self.save_path_label.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
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
                self.input_key_2.setText("")
                self.input_key_3.setText("")
                self.plain_text_edit_2.setPlainText("")
                self.cipher_text_edit_2.setPlainText("")
                self.import_file_path_edit.setText("")
                self.save_path_label.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")
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
            # 凯撒 --done
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
            # 关键字 --done
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
                self.input_key.setValidator(self.classical_validator_3)
            # 仿射 --done
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
            # 多边 --done
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
                self.input_key.setPlaceholderText("请输入密钥，仅限5位大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 维吉尼亚 --done
            elif button == 4:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.vigenere_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.vigenere_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("维吉尼亚")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # Autokey密 --done
            elif button == 5:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.autokey_ciphertext_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.autokey_ciphertext_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("Autokey密")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # Autokey明 --done
            elif button == 6:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.autokey_plaintext_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.autokey_plaintext_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("Autokey明")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 波雷费 --done
            elif button == 7:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.playfair_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.playfair_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("波雷费密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 置换 --done
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
            # 列置换 --done
            elif button == 9:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.column_permutation_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.column_permutation_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("列置换密码")
                self.input_key.setPlaceholderText("请输入密钥，只能为大小写字母")
                self.input_key.setValidator(self.classical_validator_3)
            # 双重置换 --done
            elif button == 10:
                self.encrypt_button.clicked.disconnect()
                self.decrypt_button.clicked.disconnect()
                self.encrypt_button.clicked.connect(self.double_transposition_encrypt_button_clicked)
                self.decrypt_button.clicked.connect(self.double_transposition_decrypt_button_clicked)
                self.input_key.setText("")
                self.plain_text_edit.setPlainText("")
                self.cipher_text_edit.setPlainText("")
                self.label.setText("双重置换")
                self.input_key.setPlaceholderText("请输入a和b(仅限大小写字母)，以一个" "(空格)分隔")
                self.input_key.setValidator(self.classical_validator_5)
