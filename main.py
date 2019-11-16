import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.add_button.clicked.connect(self.add_coffe)
        self.change_button.clicked.connect(self.change_coffe)

        self.update_table()

    def update_table(self):
        cur = self.con.cursor()
        inquiry = """SELECT id, (SELECT variety_name FROM variety_names 
WHERE variety_names.id = Espresso.variety_name_id),
 (SELECT frying_degree FROM degree_of_frying 
 WHERE degree_of_frying.id = Espresso.degree_of_frying_id),
  type, description, price, volume FROM Espresso"""
        result = cur.execute(inquiry).fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта',
                                                    'обжарка', 'тип',
                                                    'описание', 'цена',
                                                    'объём'])
        self.tableWidget.setColumnWidth(0, 15)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 112)
        self.tableWidget.setColumnWidth(4, 290)
        self.tableWidget.setColumnWidth(5, 15)
        self.tableWidget.setColumnWidth(6, 55)

    def add_coffe(self):
        self.ex = EditorWindoe('', '', '', '', '', '', 'add', '')
        self.ex.show()

    def change_coffe(self):
        try:
            x = self.tableWidget.selectedItems()[0].row()
        except:
            return
        data = []
        for i in range(self.tableWidget.columnCount()):
            data.append(self.tableWidget.item(x, i).text())
        self.ex = EditorWindoe(*data[1:], 'change', data[0])
        self.ex.show()


class EditorWindoe(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.variety_name = args[0]
        self.degree_of_frying = args[1]
        self.type = args[2]
        self.description = args[3]
        self.price = args[4]
        self.volume = args[5]
        self.status = args[6]
        self.id = args[7]

        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.cancellation_button.clicked.connect(self.cancel_window)
        self.save_button.clicked.connect(self.create_new_coffe)

        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['название сорта',
                                                    'обжарка', 'тип',
                                                    'описание', 'цена',
                                                    'объём'])
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 112)
        self.tableWidget.setColumnWidth(3, 320)
        self.tableWidget.setColumnWidth(4, 15)
        self.tableWidget.setColumnWidth(5, 55)

        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(
            self.variety_name)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(
            self.degree_of_frying)))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.type)))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(self.description)))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.price)))
        self.tableWidget.setItem(0, 5, QTableWidgetItem(str(self.volume)))

    def cancel_window(self):
        self.con.close()
        self.close()

    def create_new_coffe(self):
        data = []
        for i in range(self.tableWidget.columnCount()):
            try:
                data.append(self.tableWidget.item(0, i).text())
            except:
                data.append('')
        if any(list(map(lambda x: x == '', data))):
            self.error_text.setText('введены не все данные')
            return
        elif not data[4].isdigit():
            self.error_text.setText('цена должна быть числом')
            return

        cur = self.con.cursor()
        inquiry = f"""SELECT id FROM variety_names
        WHERE variety_name = '{data[0]}'"""
        result = cur.execute(inquiry).fetchall()
        if len(result) == 0:
            cur = self.con.cursor()
            inquiry = f"""INSERT INTO variety_names(variety_name) 
                                VALUES('{data[0]}')"""
            cur.execute(inquiry)
            self.con.commit()

            cur = self.con.cursor()
            inquiry = f"""SELECT id FROM variety_names
                    WHERE variety_name = '{data[0]}'"""
            result = cur.execute(inquiry).fetchall()
            variety_name_id = result[0][0]
        else:
            variety_name_id = result[0][0]

        cur = self.con.cursor()
        inquiry = f"""SELECT id FROM degree_of_frying
                WHERE frying_degree = '{data[1]}'"""
        result = cur.execute(inquiry).fetchall()
        if len(result) == 0:
            cur = self.con.cursor()
            inquiry = f"""INSERT INTO degree_of_frying(frying_degree) 
                                        VALUES('{data[1]}')"""
            cur.execute(inquiry)
            self.con.commit()
            cur = self.con.cursor()
            inquiry = f"""SELECT id FROM degree_of_frying
                            WHERE frying_degree = '{data[1]}'"""
            result = cur.execute(inquiry).fetchall()
            degree_of_frying_id = result[0][0]
        else:
            degree_of_frying_id = result[0][0]

        type = data[2]
        description = data[3]
        price = data[4]
        volume = data[5]

        if self.status == 'change':
            inquiry = f"""UPDATE Espresso
SET variety_name_id = {variety_name_id}, type = '{type}',
description = '{description}', price = {price}, volume = '{volume}',
degree_of_frying_id = {degree_of_frying_id}
            WHERE id = {self.id}"""
            cur = self.con.cursor()
            cur.execute(inquiry)
            self.con.commit()

        elif self.status == 'add':
            cur = self.con.cursor()
            inquiry = f"""INSERT INTO Espresso(variety_name_id, 
            degree_of_frying_id, type, description, price, volume) 
                VALUES({variety_name_id}, {degree_of_frying_id}, '{type}', 
                                    '{description}', {price}, '{volume}')"""
            cur.execute(inquiry)
            self.con.commit()

        ex.update_table()
        self.cancel_window()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
