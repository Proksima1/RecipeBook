from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
import sys


class show_receipt(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(show_receipt, self).__init__(parent, QtCore.Qt.Window)
        uic.loadUi('show_recept.ui', self)
        self.click_counter = 0
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.denied)

    def closeEvent(self, event):
        self.lineEdit.setStyleSheet('background-color: rgb(217, 217, 217);')
        self.lineEdit_2.setStyleSheet('background-color: rgb(217, 217, 217);')
        self.plainTextEdit.setStyleSheet('background-color: rgb(217, 217, 217);')
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.plainTextEdit.setReadOnly(True)
        self.click_counter = 0

    def ok(self):
        pass

    def denied(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = show_receipt()
    calc.show()
    sys.exit(app.exec())