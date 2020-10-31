from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QApplication
import sys
import sqlite3


class add_receipt(QtWidgets.QDialog):
    def __init__(self):
        super(add_receipt, self).__init__()
        uic.loadUi('new_recept.ui', self)
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.denie)
        self.plainTextEdit.textChanged.connect(self.unred)
        self.lineEdit.textChanged.connect(self.unred)
        self.lineEdit_2.textChanged.connect(self.unred)
        """инициализация базы данных"""
        self.db_connection = sqlite3.connect("recepts_db.sqlite")
        self.cursor = self.db_connection.cursor()
        """окончание инициализация базы данных"""

    def denie(self):
        self.lineEdit_2.clear()
        self.lineEdit.clear()
        self.plainTextEdit.clear()
        self.close()

    def accepted(self):
        if self.lineEdit.text().strip() == '':
            self.lineEdit.setStyleSheet('border: 1px solid red')
        elif self.plainTextEdit.toPlainText().strip() == '':
            self.plainTextEdit.setStyleSheet('border: 1px solid red')
        elif self.lineEdit_2.text().strip() == '':
            self.lineEdit_2.setStyleSheet('border: 1px solid red')
        else:
            self.cursor.execute(f"""INSERT INTO 
            recepts(title, description, marks) VALUES('{self.lineEdit.text()}',
            '{self.plainTextEdit.toPlainText()}',
            '{' '.join(self.lineEdit_2.text().split())}')""")
            self.db_connection.commit()
            self.close()
        QtWidgets.QMessageBox.information(self, 'Успешно!',
                                                'Новый рецепт успешно добавлен')
        return

    def unred(self):
        self.sender().setStyleSheet('border: 1px solid gray')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = add_receipt()
    calc.show()
    sys.exit(app.exec())