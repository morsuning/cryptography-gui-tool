import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from event import event

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = event.Event(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
