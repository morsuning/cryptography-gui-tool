import sys
# import main_window
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget
from PyQt5 import QtCore
import PyQt5.QtGui
from qtpy import QtGui


class mainwindow(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("这是标题")
        self.initUI()
        # self.show()

    def initUI(self):
        self.statusBar().showMessage("你好")
        btn = QPushButton("Quit", self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = mainwindow()
    # QMainWindow = main_window.Ui_MainWindow()
    # ui = main_window.Ui_MainWindow()
    # ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
