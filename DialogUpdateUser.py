# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\Diplome\DialogUpdateUser.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_DialogUpdateUser(object):
    def setupUi(self, DialogUpdateUser):
        DialogUpdateUser.setObjectName("DialogUpdateUser")
        DialogUpdateUser.resize(411, 267)
        self.gridLayout = QtWidgets.QGridLayout(DialogUpdateUser)
        self.gridLayout.setObjectName("gridLayout")
        self.lUserLogin = QtWidgets.QLabel(DialogUpdateUser)
        self.lUserLogin.setObjectName("lUserLogin")
        self.gridLayout.addWidget(self.lUserLogin, 0, 0, 1, 1)
        self.lineUserLogin = QtWidgets.QLineEdit(DialogUpdateUser)
        self.lineUserLogin.setObjectName("lineUserLogin")
        self.gridLayout.addWidget(self.lineUserLogin, 0, 1, 1, 1)
        self.lUserPassword = QtWidgets.QLabel(DialogUpdateUser)
        self.lUserPassword.setObjectName("lUserPassword")
        self.gridLayout.addWidget(self.lUserPassword, 1, 0, 1, 1)
        self.lineUserPassword = QtWidgets.QLineEdit(DialogUpdateUser)
        self.lineUserPassword.setObjectName("lineUserPassword")
        self.gridLayout.addWidget(self.lineUserPassword, 1, 1, 1, 1)
        self.lPosition = QtWidgets.QLabel(DialogUpdateUser)
        self.lPosition.setObjectName("lPosition")
        self.gridLayout.addWidget(self.lPosition, 2, 0, 1, 1)
        self.linePosition = QtWidgets.QLineEdit(DialogUpdateUser)
        self.linePosition.setObjectName("linePosition")
        self.gridLayout.addWidget(self.linePosition, 2, 1, 1, 1)
        self.pushUpdateUser = QtWidgets.QPushButton(DialogUpdateUser)
        self.pushUpdateUser.setObjectName("pushUpdateUser")
        self.gridLayout.addWidget(self.pushUpdateUser, 3, 1, 1, 1)

        self.retranslateUi(DialogUpdateUser)
        QtCore.QMetaObject.connectSlotsByName(DialogUpdateUser)

    def retranslateUi(self, DialogUpdateUser):
        _translate = QtCore.QCoreApplication.translate
        DialogUpdateUser.setWindowTitle(_translate("DialogUpdateUser", tr("DialogUpdateUser")))
        self.lUserLogin.setText(_translate("DialogUpdateUser", tr("User login")))
        self.lUserPassword.setText(_translate("DialogUpdateUser", tr("User password")))
        self.lPosition.setText(_translate("DialogUpdateUser", tr("User role")))
        self.pushUpdateUser.setText(_translate("DialogUpdateUser", tr("Update a user")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogUpdateUser = QtWidgets.QDialog()
    ui = Ui_DialogUpdateUser()
    ui.setupUi(DialogUpdateUser)
    DialogUpdateUser.show()
    sys.exit(app.exec_())
