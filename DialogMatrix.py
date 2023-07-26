from PyQt5 import QtCore, QtWidgets
from Translation import tr


class DialogMatrix(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 355)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.line_Total_SMR = QtWidgets.QLineEdit(Dialog)
        self.line_Total_SMR.setReadOnly(True)
        self.line_Total_SMR.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.line_Total_SMR, 4, 0, 1, 1)
        self.pushButtonOK = QtWidgets.QPushButton(Dialog)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.gridLayout.addWidget(self.pushButtonOK, 6, 0, 1, 1)
        self.retranslateUi(Dialog)
        self.pushButtonOK.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", tr("Matrix of distribution of workers")))
        self.pushButtonOK.setText(_translate("Dialog", tr("OK")))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = DialogMatrix()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

