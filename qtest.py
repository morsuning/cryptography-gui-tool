import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QToolBox, QGroupBox, QVBoxLayout, QApplication, QMainWindow


class Example(QToolBox):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(280, 500)
        self.setWindowTitle('微信公众号：学点编程吧--QToolBox')
        self.setWindowFlags(Qt.Dialog)
        groupbox = QGroupBox()
        vlayout = QVBoxLayout(groupbox)
        vlayout.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Example()
    ui.show()
    sys.exit(app.exec_())
