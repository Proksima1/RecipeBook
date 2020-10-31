import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from add_receipt import add_receipt
from show_recept import show_receipt
import sqlite3


class Recepts(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('recepts.ui', self)
        self.add_receipt = add_receipt()
        self.show_recept = show_receipt()
        self.comboBox.addItem('Поиск в название')
        self.comboBox.addItem('Поиск в описании')
        self.comboBox.addItem('Поиск везде')
        """"----инициальзация баз данных, создание всех нужных таблиц----"""
        db_connection = sqlite3.connect("recepts_db.sqlite")
        self.cursor = db_connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS recepts (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        title VARCHAR (100), description TEXT, marks VARCHAR (100))""")
        """"----окончание инициальзации бд----"""
        results = self.cursor.execute("""SELECT DISTINCT marks FROM recepts""").fetchall()
        if not len(results):
            self.marks.addItem('Нету меток')
        else:
            all_marks = []
            for result in results:
                for mark in result[0].split('-'):
                    all_marks.append(mark)
            for i in sorted(set(all_marks), key=lambda x: x[0]):
                self.marks.addItem(i)
        results = self.cursor.execute("""SELECT title FROM recepts ORDER BY title""").fetchall()
        if not results:
            self.listWidget.addItem('Вы не добавили ещё не одного рецета, исправим это? \n(Нажмите 2 раза по этому '
                                    'сообщению)')
        else:
            for result in results:
                self.listWidget.addItem(result[0])

        """Привязка кнопок и т.д"""
        # пункт меню "добавить рецепт"
        self.action.triggered.connect(self.call_add_receipt)
        self.action.setShortcut('Ctrl+N')

        self.add_receipt.buttonBox.accepted.connect(self.add_receipt_accepted)
        self.add_receipt.buttonBox.rejected.connect(self.add_receipt.reject)
        self.listWidget.itemDoubleClicked.connect(self.open_recept)

    def call_add_receipt(self):
        self.add_receipt.exec_()

    def add_receipt_accepted(self):
        self.add_receipt.lineEdit_2.clear()
        self.add_receipt.lineEdit.clear()
        self.add_receipt.plainTextEdit.clear()
        results = self.cursor.execute("""SELECT DISTINCT marks FROM recepts""").fetchall()
        self.marks.clear()
        if not len(results):
            self.comboBox.addItem('Нету меток')
        else:
            all_marks = []
            for result in results:
                for mark in result[0].split('-'):
                    all_marks.append(mark)
            for i in sorted(set(all_marks), key=lambda x: x[0]):
                self.marks.addItem(i)
        results = self.cursor.execute("""SELECT title FROM recepts ORDER BY title""").fetchall()
        if not results:
            self.listWidget.addItem('Вы не добавили ещё не одного рецета, исправим это? \n(Нажмите 2 раза по этому '
                                    'сообщению)')
        else:
            self.listWidget.clear()
            for result in results:
                self.listWidget.addItem(result[0])
        self.add_receipt.hide()

    def open_recept(self, item):
        if item.text() == 'Вы не добавили ещё не одного рецета, исправим это?' \
                          ' \n(Нажмите 2 раза по этому сообщению)':
            self.add_receipt.show()
        else:
            self.show_recept.show()
            print(item.text())
            result = self.cursor.execute(f"""SELECT title, description, marks FROM recepts WHERE
            title={item.text()}""").fetchone()
            print(result)
            self.show_recept.lineEdit.setText(result[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Recepts()
    s.show()
    sys.exit(app.exec())