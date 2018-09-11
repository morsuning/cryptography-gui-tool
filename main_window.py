# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ui import single_ui


class Ui_main_window(QtWidgets.QMainWindow):

    def __init__(self, main_window):
        super().__init__()
        self.sietup_u(main_window)
        # 连接专用 TODO 在这里建立各种连接
        self.trigger = QtCore.pyqtSignal()
        self.trigger.connect()

    def setup_ui(self, main_window):
        """设置主界面，主界面只包含一个状态栏一个QStackedWidget和一个QFrame"""
        main_window.setObjectName("main_window")
        main_window.resize(812, 602)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        main_window.setFont(font)
        main_window.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        main_window.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # 设置QStackWidget用来切换单/双机加密
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(40, 20, 131, 21))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.currentChanged['int'].connect(main_window.update)

        # 创建切换按钮
        self.change_button = QtWidgets.QPushButton("切换单/双机模式", self)
        # 或者self.button.move(20,20)也能设置
        self.change_button.setGeometry(0, 0, 0, 0)
        self.change_button.clicked.connect(self.switch_page())

        # 分别配置单双机界面
        # self.page_s = QtWidgets.QWidget()
        # self.page_s.setObjectName("page_s")
        self.page_s = single_ui.SingleMode()
        self.page_s.setObjectName("page_s")
        # 前面应该是写好类中创建的page_s对象，像单机加密就是sigle_ui.py中的SingleMode类对象
        self.stackedWidget.addWidget(self.page_s)

        self.page_d = QtWidgets.QWidget()
        self.page_d.setObjectName("page_d")
        # TODO
        self.stackedWidget.addWidget(self.page_d)

        # 设置QFrame，用来勾勒右侧显示框架 - 一直存在
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(210, 50, 561, 491))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")

        # 创建转态栏
        main_window.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(main_window)
        self.statusBar.setObjectName("statusBar")
        # 设置状态栏
        main_window.setStatusBar(self.statusBar)

        self.retranslateUi(main_window)

        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate  # 国际化支持
        main_window.setWindowTitle(_translate("main_window", "单/双机加解密"))
        # self.page_1.setToolTip(_translate("main_window", "<html><head/><body><p><br/></p></body></html>"))

    # 设置换页逻辑
    def switch_page(self):
        n_count = self.stackedWidget.count()
        n_index = self.stackedWidget.currentIndex()
        n_index += 1
        if n_index >= n_count:
            n_index = 0
        self.stackedWidget.setCurrentIndex(n_index)

    def display(self):
        pass

    # 移到dual_ui.py
    def page_t_ui(self):
        pass