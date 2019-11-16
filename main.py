import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
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


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
