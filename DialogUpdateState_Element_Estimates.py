# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\Diplome\DialogUpdateState_Element_Estimates.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_DialogUpdateState_Element_Estimates(object):
    def setupUi(self, DialogUpdateState_Element_Estimates):
        DialogUpdateState_Element_Estimates.setObjectName("DialogUpdateState_Element_Estimates")
        DialogUpdateState_Element_Estimates.resize(407, 174)
        self.gridLayout = QtWidgets.QGridLayout(DialogUpdateState_Element_Estimates)
        self.gridLayout.setObjectName("gridLayout")
        self.lGESN_id = QtWidgets.QLabel(DialogUpdateState_Element_Estimates)
        self.lGESN_id.setObjectName("lGESN_id")
        self.gridLayout.addWidget(self.lGESN_id, 0, 0, 1, 1)
        self.lUnit = QtWidgets.QLabel(DialogUpdateState_Element_Estimates)
        self.lUnit.setObjectName("lUnit")
        self.gridLayout.addWidget(self.lUnit, 1, 0, 1, 1)
        self.lGESN_name = QtWidgets.QLabel(DialogUpdateState_Element_Estimates)
        self.lGESN_name.setObjectName("lGESN_name")
        self.gridLayout.addWidget(self.lGESN_name, 2, 0, 1, 1)
        self.lineGesn_name = QtWidgets.QLineEdit(DialogUpdateState_Element_Estimates)
        self.lineGesn_name.setObjectName("lineGesn_name")
        self.gridLayout.addWidget(self.lineGesn_name, 2, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(126, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.pushUpdateData = QtWidgets.QPushButton(DialogUpdateState_Element_Estimates)
        self.pushUpdateData.setObjectName("pushUpdateData")
        self.gridLayout.addWidget(self.pushUpdateData, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(126, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.lineUnit = QtWidgets.QLineEdit(DialogUpdateState_Element_Estimates)
        self.lineUnit.setObjectName("lineUnit")
        self.gridLayout.addWidget(self.lineUnit, 1, 1, 1, 2)
        self.lineGesn_id = QtWidgets.QLineEdit(DialogUpdateState_Element_Estimates)
        self.lineGesn_id.setObjectName("lineGesn_id")
        self.gridLayout.addWidget(self.lineGesn_id, 0, 1, 1, 2)

        self.retranslateUi(DialogUpdateState_Element_Estimates)
        QtCore.QMetaObject.connectSlotsByName(DialogUpdateState_Element_Estimates)

    def retranslateUi(self, DialogUpdateState_Element_Estimates):
        _translate = QtCore.QCoreApplication.translate
        DialogUpdateState_Element_Estimates.setWindowTitle(_translate("DialogUpdateState_Element_Estimates",
                                                                      tr("DialogUpdateState_Element_Estimates")))
        self.lGESN_id.setText(_translate("DialogUpdateState_Element_Estimates", tr("GESN ID")))
        self.lUnit.setText(_translate("DialogUpdateState_Element_Estimates", tr("Unit")))
        self.lGESN_name.setText(_translate("DialogUpdateState_Element_Estimates", tr("GESN name")))
        self.pushUpdateData.setText(_translate("DialogUpdateState_Element_Estimates", tr("Update Data")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogUpdateState_Element_Estimates = QtWidgets.QDialog()
    ui = Ui_DialogUpdateState_Element_Estimates()
    ui.setupUi(DialogUpdateState_Element_Estimates)
    DialogUpdateState_Element_Estimates.show()
    sys.exit(app.exec_())
