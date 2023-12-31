# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\Diplome\Dialog_AddToRegBuildingsInDistrictTable.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_AddToRegBuildingsInDistrictTable(object):
    def __init__(self):
        self.data3 = 0
        self.data2 = 0
        self.data1 = 0

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(397, 239)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.labelFloors = QtWidgets.QLabel(Dialog)
        self.labelFloors.setObjectName("labelFloors")
        self.gridLayout.addWidget(self.labelFloors, 0, 0, 1, 1)
        self.label_Entrances = QtWidgets.QLabel(Dialog)
        self.label_Entrances.setObjectName("label_Entrances")
        self.gridLayout.addWidget(self.label_Entrances, 1, 0, 1, 1)
        self.label_TotalNumberOfFloors = QtWidgets.QLabel(Dialog)
        self.label_TotalNumberOfFloors.setObjectName("label_TotalNumberOfFloors")
        self.gridLayout.addWidget(self.label_TotalNumberOfFloors, 2, 0, 1, 1)
        self.label_Buildings_name_reg = QtWidgets.QLabel(Dialog)
        self.label_Buildings_name_reg.setObjectName("label_Buildings_name_reg")
        self.gridLayout.addWidget(self.label_Buildings_name_reg, 3, 0, 1, 1)
        self.lineBuildings_name_reg = QtWidgets.QLineEdit(Dialog)
        self.lineBuildings_name_reg.setObjectName("lineBuildings_name_reg")
        self.gridLayout.addWidget(self.lineBuildings_name_reg, 3, 1, 1, 2)
        self.label_NumberOfBuilding = QtWidgets.QLabel(Dialog)
        self.label_NumberOfBuilding.setObjectName("label_NumberOfBuilding")
        self.gridLayout.addWidget(self.label_NumberOfBuilding, 4, 0, 1, 1)
        self.pushAddData = QtWidgets.QPushButton(Dialog)
        self.pushAddData.setObjectName("pushAddData")
        self.gridLayout.addWidget(self.pushAddData, 5, 1, 1, 1)
        self.spinBox_TotalNumberOfFloors = QtWidgets.QSpinBox(Dialog)
        self.spinBox_TotalNumberOfFloors.setReadOnly(True)
        self.spinBox_TotalNumberOfFloors.setObjectName("spinBox_TotalNumberOfFloors")
        self.gridLayout.addWidget(self.spinBox_TotalNumberOfFloors, 2, 1, 1, 2)
        self.spinBox_Entrances = QtWidgets.QSpinBox(Dialog)
        self.spinBox_Entrances.setObjectName("spinBox_Entrances")
        self.gridLayout.addWidget(self.spinBox_Entrances, 1, 1, 1, 2)
        self.spinFloors = QtWidgets.QSpinBox(Dialog)
        self.spinFloors.setObjectName("spinFloors")
        self.gridLayout.addWidget(self.spinFloors, 0, 1, 1, 2)
        self.spinBox_NumberOfBuilding = QtWidgets.QSpinBox(Dialog)
        self.spinBox_NumberOfBuilding.setReadOnly(True)
        self.spinBox_NumberOfBuilding.setObjectName("spinBox_NumberOfBuilding")
        self.gridLayout.addWidget(self.spinBox_NumberOfBuilding, 4, 1, 1, 2)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        # calling method
        self.spinFloors.valueChanged.connect(self.action_spin1)
        self.spinBox_Entrances.valueChanged.connect(self.action_spin2)

    def action_spin1(self):
        self.data1 = self.spinFloors.value()
        self.spinBox_TotalNumberOfFloors.setValue(self.data1 * self.data2)

    def action_spin2(self):
        self.data2 = self.spinBox_Entrances.value()
        self.spinBox_TotalNumberOfFloors.setValue(self.data1 * self.data2)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", tr("DialogAddToRegBuildingInDistrictTable")))
        self.labelFloors.setText(_translate("Dialog", tr("Amount of floors")))
        self.label_Entrances.setText(_translate("Dialog", tr("Amount of entrances")))
        self.label_TotalNumberOfFloors.setText(_translate("Dialog", tr("Total amount of floors")))
        self.label_Buildings_name_reg.setText(_translate("Dialog", tr("Building name")))
        self.label_NumberOfBuilding.setText(_translate("Dialog", tr("Number of building")))
        self.pushAddData.setText(_translate("Dialog", tr("Add Data")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_AddToRegBuildingsInDistrictTable()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
