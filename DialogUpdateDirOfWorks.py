# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\Diplome\DialogUpdateDirOfWorks.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_DialogUpdateDirOfWorks(object):
    def setupUi(self, DialogUpdateDirOfWorks):
        DialogUpdateDirOfWorks.setObjectName("DialogUpdateDirOfWorks")
        DialogUpdateDirOfWorks.resize(452, 159)
        self.gridLayout = QtWidgets.QGridLayout(DialogUpdateDirOfWorks)
        self.gridLayout.setObjectName("gridLayout")
        self.lWork_name = QtWidgets.QLabel(DialogUpdateDirOfWorks)
        self.lWork_name.setObjectName("lWork_name")
        self.gridLayout.addWidget(self.lWork_name, 0, 0, 1, 1)
        self.lGesn_id = QtWidgets.QLabel(DialogUpdateDirOfWorks)
        self.lGesn_id.setObjectName("lGesn_id")
        self.gridLayout.addWidget(self.lGesn_id, 1, 0, 1, 1)
        self.lUnit = QtWidgets.QLabel(DialogUpdateDirOfWorks)
        self.lUnit.setObjectName("lUnit")
        self.gridLayout.addWidget(self.lUnit, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(149, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.pushUpdateData = QtWidgets.QPushButton(DialogUpdateDirOfWorks)
        self.pushUpdateData.setObjectName("pushUpdateData")
        self.gridLayout.addWidget(self.pushUpdateData, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(148, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.lineUnit = QtWidgets.QLineEdit(DialogUpdateDirOfWorks)
        self.lineUnit.setObjectName("lineUnit")
        self.gridLayout.addWidget(self.lineUnit, 2, 1, 1, 2)
        self.lineGesn_id = QtWidgets.QLineEdit(DialogUpdateDirOfWorks)
        self.lineGesn_id.setObjectName("lineGesn_id")
        self.gridLayout.addWidget(self.lineGesn_id, 1, 1, 1, 2)
        self.lineWork_name = QtWidgets.QLineEdit(DialogUpdateDirOfWorks)
        self.lineWork_name.setObjectName("lineWork_name")
        self.gridLayout.addWidget(self.lineWork_name, 0, 1, 1, 2)

        self.retranslateUi(DialogUpdateDirOfWorks)
        QtCore.QMetaObject.connectSlotsByName(DialogUpdateDirOfWorks)

    def retranslateUi(self, DialogUpdateDirOfWorks):
        _translate = QtCore.QCoreApplication.translate
        DialogUpdateDirOfWorks.setWindowTitle(_translate("DialogUpdateDirOfWorks",
                                                         tr("DialogUpdateDirOfWorks")))
        self.lWork_name.setText(_translate("DialogUpdateDirOfWorks", tr("Work name")))
        self.lGesn_id.setText(_translate("DialogUpdateDirOfWorks", tr("GESN ID")))
        self.lUnit.setText(_translate("DialogUpdateDirOfWorks", tr("Unit")))
        self.pushUpdateData.setText(_translate("DialogUpdateDirOfWorks", tr("Update Data")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogUpdateDirOfWorks = QtWidgets.QDialog()
    ui = Ui_DialogUpdateDirOfWorks()
    ui.setupUi(DialogUpdateDirOfWorks)
    DialogUpdateDirOfWorks.show()
    sys.exit(app.exec_())
