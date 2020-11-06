import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog
from add_receipt import add_receipt
from show_recept import show_receipt
from delete_accept import delete_accept
import sqlite3


class Recepts(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('recepts.ui', self)
        self.add_receipt = add_receipt(self)
        self.show_recept = show_receipt(self)
        self.delete_accept = delete_accept(self)
        self.comboBox.addItem('Поиск в названии')
        self.comboBox.addItem('Поиск в описании')
        self.comboBox.addItem('Поиск везде')
        # ----инициальзация баз данных, создание всех нужных таблиц----
        self.db_connection = sqlite3.connect("recepts_db.sqlite")
        self.cursor = self.db_connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS recepts (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        title VARCHAR (100), description TEXT, marks VARCHAR (100))""")
        # ----окончание инициальзации бд----
        # обновление меток и рецептов
        self.update_data()
        # все подключения окна "delete_accept"
        self.delete_accept.buttonBox.accepted.connect(self.delete_receipt_accepted)
        self.delete_accept.buttonBox.rejected.connect(self.delete_receipt_denie)
        # все подключения окна "add_receipt"
        self.add_receipt.buttonBox.accepted.connect(self.update_data)
        self.add_receipt.buttonBox.rejected.connect(self.add_receipt.denie)
        # все подключения окна "show_recept"
        self.show_recept.edit_button.clicked.connect(self.edit_recept)
        self.show_recept.delete_button.clicked.connect(self.call_delete_recept)
        self.show_recept.save.clicked.connect(self.save_recept)
        self.show_recept.lineEdit.textChanged.connect(self.changed)
        self.show_recept.lineEdit_2.textChanged.connect(self.changed)
        self.show_recept.plainTextEdit.textChanged.connect(self.changed)
        # все подключения данного окна
        self.listWidget.itemDoubleClicked.connect(self.open_recept)
        self.sort.textChanged.connect(self.search)
        # пункт меню "добавить рецепт"
        self.action.triggered.connect(self.call_add_receipt)
        self.action.setShortcut('Ctrl+N')
        # пункт меню "редактировать рецепт"
        self.action_3.triggered.connect(self.edit_recept)
        self.action_3.setShortcut('Crtl+R')
        # пункт меню "удалить рецепт"
        #self.action_2.triggered.connect(self.delete_recept)
        self.action_2.setShortcut('Crtl+D')
        self.action_8.triggered.connect(self.change_background_image)
        self.action_7.triggered.connect(self.change_background_color)
        # переменные
        self.name_before = ''

    def update_data(self):
        results = self.cursor.execute("""SELECT DISTINCT marks FROM recepts""").fetchall()
        self.marks.clear()
        if not len(results):
            self.marks.addItem('Нету меток')
        else:
            all_marks = []
            for result in results:
                for mark in result[0].split('-'):
                    all_marks.append(mark.strip())
            for i in sorted(set(all_marks), key=lambda x: x[0]):
                self.marks.addItem(i)
        results = self.cursor.execute("""SELECT title FROM recepts ORDER BY title""").fetchall()
        if not results:
            self.listWidget.clear()
            self.listWidget.addItem('Вы не добавили ещё ни одного рецета, исправим это? \n(Нажмите 2 раза по этому '
                                    'сообщению)')
        else:
            self.listWidget.clear()
            for result in results:
                self.listWidget.addItem(result[0])

    def call_add_receipt(self):
        self.add_receipt.exec_()

    def open_recept(self, item):
        if item.text() == 'Вы не добавили ещё ни одного рецета, исправим это?' \
                          ' \n(Нажмите 2 раза по этому сообщению)':
            self.add_receipt.show()
        else:
            self.show_recept.show()
            result = self.cursor.execute(f"""SELECT title, description, marks FROM recepts WHERE
            title='{item.text()}'""").fetchone()
            self.show_recept.lineEdit.setText(result[0])
            self.name_before = self.show_recept.lineEdit.text()
            self.show_recept.plainTextEdit.setPlainText(result[1])
            self.show_recept.lineEdit_2.setText(result[2].replace('-', ','))
            self.show_recept.save.setEnabled(False)

    def search(self):
        box = self.comboBox.currentText()
        res = self.cursor.execute("""SELECT title FROM recepts""").fetchall()
        if not res:
            self.listWidget.clear()
            self.listWidget.addItem('Вы не добавили ещё ни одного рецета, исправим это? \n(Нажмите 2 раза по этому '
                                    'сообщению)')
        else:
            if box == 'Поиск в названии':
                results = sorted(self.cursor.execute(f"""SELECT title FROM recepts WHERE title LIKE
                '%{self.sort.text()}%'""").fetchall(), key=lambda x: x[0])
                self.listWidget.clear()
                for result in results:
                    self.listWidget.addItem(result[0])
            elif box == 'Поиск в описании':
                results = sorted(self.cursor.execute(f"""SELECT title FROM recepts WHERE description LIKE
                            '%{self.sort.text()}%'""").fetchall(), key=lambda x: x[0])
                self.listWidget.clear()
                for result in results:
                    self.listWidget.addItem(result[0])
            elif box == 'Поиск везде':
                results = sorted(self.cursor.execute(f"""SELECT title FROM recepts WHERE (description LIKE
                                        '%{self.sort.text()}%' OR title LIKE
                                        '%{self.sort.text()}%')""").fetchall(), key=lambda x: x[0])
                self.listWidget.clear()
                for result in results:
                    self.listWidget.addItem(result[0])
            else:
                print('Что-то не так с comboBox с выбором поиска')

    def edit_recept(self):
        if self.show_recept.click_counter % 2 == 0:
            self.show_recept.lineEdit.setStyleSheet('')
            self.show_recept.lineEdit_2.setStyleSheet('')
            self.show_recept.plainTextEdit.setStyleSheet('')
            self.show_recept.lineEdit.setReadOnly(False)
            self.show_recept.lineEdit_2.setReadOnly(False)
            self.show_recept.plainTextEdit.setReadOnly(False)
        else:
            self.show_recept.lineEdit.setStyleSheet('background-color: rgb(217, 217, 217);')
            self.show_recept.lineEdit_2.setStyleSheet('background-color: rgb(217, 217, 217);')
            self.show_recept.plainTextEdit.setStyleSheet('background-color: rgb(217, 217, 217);')
            self.show_recept.lineEdit.setReadOnly(True)
            self.show_recept.lineEdit_2.setReadOnly(True)
            self.show_recept.plainTextEdit.setReadOnly(True)
        self.show_recept.click_counter += 1

    def call_delete_recept(self):
        self.delete_accept.show()

    def save_recept(self):
        result = self.cursor.execute(f"""UPDATE recepts SET 
title='{self.show_recept.lineEdit.text()}', 
description='{self.show_recept.plainTextEdit.toPlainText()}', 
marks='{'-'.join(i.strip() for i in self.show_recept.lineEdit_2.text().split(','))}' 
WHERE title='{self.name_before}'""")
        self.db_connection.commit()
        if result:
            QtWidgets.QMessageBox.information(self, 'Успешно!', 'Рецепт изменён!')
            self.update_data()
        else:
            QtWidgets.QMessageBox.information(self, 'Ошибка!', 'Произошла ошибка при добавлении данных!')
        self.show_recept.close()

    def changed(self):
        result = self.cursor.execute(f"""SELECT title, description, marks FROM recepts WHERE
                    title='{self.show_recept.lineEdit.text()}'""").fetchone()
        try:
            self.sender().text()
        except AttributeError:
            changed_text = self.sender().toPlainText()
        else:
            changed_text = self.sender().text()
        if result is not None:
            if changed_text not in result:
                self.show_recept.save.setEnabled(True)
            else:
                self.show_recept.save.setEnabled(False)
        else:
            self.show_recept.save.setEnabled(True)

    def delete_receipt_accepted(self):
        self.cursor.execute(f"""DELETE FROM recepts WHERE title='{self.show_recept.lineEdit.text()}'
AND description='{self.show_recept.plainTextEdit.toPlainText()}'
AND marks='{self.show_recept.lineEdit_2.text().replace(',', '-')}'""")
        self.db_connection.commit()
        self.update_data()
        self.show_recept.close()
        self.delete_accept.close()

    def delete_receipt_denie(self):
        self.delete_accept.close()

    def change_background_image(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.png);;Картинка (*.jpg)')[0]
        oImage = QImage(fname)
        sImage = oImage.scaled(QSize(509, 470))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(color))
            self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = Recepts()
    s.show()
    sys.exit(app.exec())
