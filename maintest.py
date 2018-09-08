import sys

import main_window
from PyQt5.QtWidgets import QApplication, QMainWindow


class Test():
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        pass


# 仅用做启动入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = main_window.Ui_main_window(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())