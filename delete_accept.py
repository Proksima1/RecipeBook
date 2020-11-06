from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
import sys


class delete_accept(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(delete_accept, self).__init__(parent, QtCore.Qt.Window)
        uic.loadUi('delete_accept.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = delete_accept()
    calc.show()
    sys.exit(app.exec())