from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
import sys


class show_receipt(QtWidgets.QDialog):
    def __init__(self):
        super(show_receipt, self).__init__()
        uic.loadUi('show_recept.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = show_receipt()
    calc.show()
    sys.exit(app.exec())