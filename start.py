import sys

import main_window
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = main_window.Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
