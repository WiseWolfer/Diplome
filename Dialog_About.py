# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\pythonProjectQTDesigner\Dialog_About.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_Dialog_About(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 167)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(132, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(133, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setEnabled(True)
        self.textEdit.setAcceptDrops(True)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", tr("About")))
        self.pushButton.setText(_translate("Dialog", tr("OK")))
        self.label.setText(_translate("Dialog", tr("Program developer:")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_About()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
