#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import QSignalMapper, QObject, Qt
from PyQt5.QtWidgets import QFileDialog, QLineEdit
from PyQt5 import QtWidgets
from algorithm.hash_algorithm import md5_file, md5_string

from demo import UiMainWindow


class Event(UiMainWindow, QObject):

    def __init__(self, main_window):
        super().__init__(main_window)

        self.md5_file_name = ""

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

        # MD5
        self.import_file_toolbox.clicked.connect(self.import_file_toolbox_clicked)
        self.pushButton.clicked.connect(self.md5_clicked)

        # 流密码+分组密码
        self.check_key_2.stateChanged.connect(self.check_key_2_click)

        # 公钥密码

        # 古典密码
        self.import_plaintext_button.clicked.connect(self.import_plaintext_button_clicked)

    def default_page_set(self):
        self.switch_sd.setCurrentIndex(0)
        self.cipher_switch_toolbox.setCurrentIndex(0)
        self.classical_cipher_switch.setCurrentIndex(0)
        self.switch_mode_with_key_tabwidget.setCurrentIndex(0)
        self.switch_mode_without_key_tabwidget.setCurrentIndex(0)

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
            self.statusbar.showMessage("同一时刻只能输入字符串或者文件", 2000)
            return
        if self.md5_file_name:
            self.md5_show_text.setText(md5_file.md5(self.md5_file_name))
            self.md5_file_name = ""
            self.lineEdit.setText("")
            self.statusbar.showMessage("成功生成文件MD5", 800)
        elif self.input_edit.toPlainText():
            self.md5_show_text.setText(md5_string.md5(self.input_edit.toPlainText()))
            self.statusbar.showMessage("成功生成字符串MD5", 800)
        else:
            return

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
            self.statusbar.showMessage(
                "已成功从"+self.import_plaintext_button_file_name+"导入文件", 800)
            try:
                f = open(self.import_plaintext_button_file_name,"r")
                self.statusbar.showMessage(
                    "已成功从" + self.import_plaintext_button_file_name + "导入文件", 800)
                self.plain_text_edit.setPlainText(f.read())
            except IOError:
                self.statusbar.showMessage(
                    "打开文件" + self.import_plaintext_button_file_name + "失败，可能不是文本文件或编码非“UTF-8”", 2000)
            finally:
                f.close()



    # 决定显示4个窗口中的哪一个
    def show_widgets(self, button):
        print(button)
        self.base_frame.setVisible(not self.is_show_widgets)

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
                self.current_cipher_label.setText("RC4")
                self.what_algorithm.setText("RC4")
            # CA
            elif button == 12:
                self.current_cipher_label.setText("CA")
                self.what_algorithm.setText("CA")
            # DES
            elif button == 13:
                self.current_cipher_label.setText("DES")
                self.what_algorithm.setText("DES")
                self.input_key_2.setMaxLength(8)
                self.input_key_2.setPlaceholderText("8个字符，仅限字母、数字的组合")
            # AES
            elif button == 14:
                self.current_cipher_label.setText("AES")
                self.what_algorithm.setText("AES")
                self.input_key_2.setMaxLength(8)
                self.input_key_2.setPlaceholderText("8个字符，仅限字母、数字的组合")
        # 古典密码
        else:
            self.cipher_with_key_frame.setVisible(self.is_show_widgets)
            self.show_base_frame = not self.show_base_frame
            self.is_show_widgets = not self.is_show_widgets
            if button == 0:
                self.label.setText("凯撒密码")
            elif button == 1:
                self.label.setText("关键字密码")
            elif button == 2:
                self.label.setText("仿射密码")
            elif button == 3:
                self.label.setText("多边密码")
            elif button == 4:
                self.label.setText("维吉尼亚")
            elif button == 5:
                self.label.setText("Autokey密")
            elif button == 6:
                self.label.setText("Autokey明")
            elif button == 7:
                self.label.setText("波雷费密码")
            elif button == 8:
                self.label.setText("置换密码")
            elif button == 9:
                self.label.setText("列置换密码")
            elif button == 10:
                self.label.setText("双重置换")



