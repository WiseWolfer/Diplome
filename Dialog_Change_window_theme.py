# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\pythonProjectQTDesigner\Dialog_Change_window_theme.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_Dialog_Change_Window_Theme(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(286, 104)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(75, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.radioButtonLigthTheme = QtWidgets.QRadioButton(Dialog)
        self.radioButtonLigthTheme.setObjectName("radioButtonLigthTheme")
        self.gridLayout.addWidget(self.radioButtonLigthTheme, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(76, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        self.radioButtonBlackTheme = QtWidgets.QRadioButton(Dialog)
        self.radioButtonBlackTheme.setObjectName("radioButtonBlackTheme")
        self.gridLayout.addWidget(self.radioButtonBlackTheme, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", tr("Changing window's theme")))
        self.radioButtonLigthTheme.setText(_translate("Dialog", tr("Light theme")))
        self.pushButton.setText(_translate("Dialog", tr("OK")))
        self.radioButtonBlackTheme.setText(_translate("Dialog", tr("Dark theme")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_Change_Window_Theme()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
