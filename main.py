import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog
import traceback


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite3")
        self.set_table()
        self.add_btn.clicked.connect(self.add_coffee)
        self.change_btn.clicked.connect(self.change_coffee)

    def set_table(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_coffee(self):
        self.dialog = AddEditCoffeeForm()
        self.dialog.show()
        try:
            if self.dialog.exec():
                data = self.dialog.data
                cur = self.con.cursor()
                cur.execute(f"""INSERT INTO coffee(sort_title, degree_of_roasting, ground_or_grains,
                 flavor_description, price, volume_of_packaging) VALUES{self.dialog.data}""")
                self.con.commit()
                self.set_table()
        except Exception:
            self.statusBar().showMessage('Выберите запись', msecs=5000)

    def change_coffee(self):
        try:
            current_item = self.tableWidget.currentItem().row()
            current_id = self.tableWidget.takeItem(current_item, 0)
            current_title = self.tableWidget.takeItem(current_item, 1)
            current_degree = self.tableWidget.takeItem(current_item, 2)
            current_mol = self.tableWidget.takeItem(current_item, 3)
            current_desc = self.tableWidget.takeItem(current_item, 4)
            current_price = self.tableWidget.takeItem(current_item, 5)
            current_volume = self.tableWidget.takeItem(current_item, 6)
            self.tableWidget.setItem(current_item, 0, current_id)
            self.tableWidget.setItem(current_item, 1, current_title)
            self.tableWidget.setItem(current_item, 2, current_degree)
            self.tableWidget.setItem(current_item, 3, current_mol)
            self.tableWidget.setItem(current_item, 4, current_desc)
            self.tableWidget.setItem(current_item, 5, current_price)
            self.tableWidget.setItem(current_item, 6, current_volume)
            self.dialog = AddEditCoffeeForm([current_title, current_degree, current_mol,
                                             current_desc, current_price, current_volume])
            self.dialog.show()
            if self.dialog.exec():
                cur = self.con.cursor()
                que = f"""UPDATE coffee SET 
                sort_title = '{self.dialog.data[0]}',
                degree_of_roasting = '{self.dialog.data[1]}',
                ground_or_grains = {self.dialog.data[2]},
                flavor_description = '{self.dialog.data[3]}',
                price = {self.dialog.data[4]},
                volume_of_packaging = {self.dialog.data[5]} 
                WHERE id = {current_id.text()}"""
                print(que)
                cur.execute(que)
                self.con.commit()
                self.set_table()
        except Exception:
            self.statusBar().showMessage('Выберите запись', msecs=5000)


class AddEditCoffeeForm(QDialog):
    def __init__(self, red_arrs=[]):
        super(AddEditCoffeeForm, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.run)
        if red_arrs:
            self.name_edit.setText(red_arrs[0].text())
            self.degree_edit.setText(red_arrs[1].text())
            self.mol_edit.setText(str(red_arrs[2].text()))
            self.desc_edit.setText(red_arrs[3].text())
            self.price_edit.setText(str(red_arrs[4].text()))
            self.volume_edit.setText(str(red_arrs[5].text()))

    def run(self):
        try:
            data = (self.name_edit.text(), self.degree_edit.text(), self.mol_edit.text(),
                    self.desc_edit.text(), float(self.price_edit.text()), float(self.volume_edit.text()))
            if all(data):
                self.data = data
                self.accept()
            else:
                self.status_bar.setText('Ошибочка')
        except Exception:
            self.status_bar.setText('Ошибочка')


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


sys.excepthook = excepthook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())