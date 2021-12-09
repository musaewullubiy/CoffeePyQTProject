import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog
from PyQt5 import QtWidgets, QtCore
import traceback


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(r"data\coffee.sqlite3")
        self.set_table()
        self.add_btn.clicked.connect(self.add_coffee)
        self.change_btn.clicked.connect(self.change_coffee)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(768, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_btn.setObjectName("add_btn")
        self.gridLayout.addWidget(self.add_btn, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.change_btn = QtWidgets.QPushButton(self.centralwidget)
        self.change_btn.setObjectName("change_btn")
        self.gridLayout.addWidget(self.change_btn, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_btn.setText(_translate("MainWindow", "Добавить"))
        self.change_btn.setText(_translate("MainWindow", "Редактировать"))

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
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        if red_arrs:
            self.name_edit.setText(red_arrs[0].text())
            self.degree_edit.setText(red_arrs[1].text())
            self.mol_edit.setText(str(red_arrs[2].text()))
            self.desc_edit.setText(red_arrs[3].text())
            self.price_edit.setText(str(red_arrs[4].text()))
            self.volume_edit.setText(str(red_arrs[5].text()))

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 216)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.name_edit = QtWidgets.QLineEdit(Dialog)
        self.name_edit.setObjectName("name_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_edit)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.degree_edit = QtWidgets.QLineEdit(Dialog)
        self.degree_edit.setObjectName("degree_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.degree_edit)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.mol_edit = QtWidgets.QLineEdit(Dialog)
        self.mol_edit.setObjectName("mol_edit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.mol_edit)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.desc_edit = QtWidgets.QLineEdit(Dialog)
        self.desc_edit.setObjectName("desc_edit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.desc_edit)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.price_edit = QtWidgets.QLineEdit(Dialog)
        self.price_edit.setObjectName("price_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.price_edit)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.volume_edit = QtWidgets.QLineEdit(Dialog)
        self.volume_edit.setObjectName("volume_edit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.volume_edit)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.status_bar = QtWidgets.QLabel(Dialog)
        self.status_bar.setText("")
        self.status_bar.setObjectName("status_bar")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.status_bar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Название"))
        self.label_3.setText(_translate("Dialog", "Степень обжарки"))
        self.label_4.setText(_translate("Dialog", "Молотый/в зернах"))
        self.label_5.setText(_translate("Dialog", "Описание вкуса"))
        self.label_6.setText(_translate("Dialog", "Цена"))
        self.label_7.setText(_translate("Dialog", "Объем упаковки"))
        self.pushButton.setText(_translate("Dialog", "Ок"))

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