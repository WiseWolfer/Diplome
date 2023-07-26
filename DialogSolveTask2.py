# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Dmitriy\PycharmProjects\Diplome\DialogSolveTask2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Translation import tr


class Ui_DialogSolveTask2(object):
    def setupUi(self, DialogSolveTask2):
        DialogSolveTask2.setObjectName("DialogSolveTask2")
        DialogSolveTask2.resize(860, 293)
        self.gridLayout = QtWidgets.QGridLayout(DialogSolveTask2)
        self.gridLayout.setObjectName("gridLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(DialogSolveTask2)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 0, 2, 1, 2)
        self.label = QtWidgets.QLabel(DialogSolveTask2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushActDoc = QtWidgets.QPushButton(DialogSolveTask2)
        self.pushActDoc.setEnabled(False)
        self.pushActDoc.setObjectName("pushActDoc")
        self.gridLayout.addWidget(self.pushActDoc, 1, 0, 1, 1)
        self.pushSolveTask = QtWidgets.QPushButton(DialogSolveTask2)
        self.pushSolveTask.setEnabled(False)
        self.pushSolveTask.setObjectName("pushSolveTask")
        self.gridLayout.addWidget(self.pushSolveTask, 1, 2, 1, 1)
        self.pushGetData = QtWidgets.QPushButton(DialogSolveTask2)
        self.pushGetData.setObjectName("pushGetData")
        self.gridLayout.addWidget(self.pushGetData, 1, 3, 1, 1)
        self.pushShowCalSMR = QtWidgets.QPushButton(DialogSolveTask2)
        self.pushShowCalSMR.setEnabled(False)
        self.pushShowCalSMR.setObjectName("pushShowCalSMR")
        self.gridLayout.addWidget(self.pushShowCalSMR, 1, 1, 1, 1)

        self.retranslateUi(DialogSolveTask2)
        QtCore.QMetaObject.connectSlotsByName(DialogSolveTask2)

    def retranslateUi(self, DialogSolveTask2):
        _translate = QtCore.QCoreApplication.translate
        DialogSolveTask2.setWindowTitle(_translate("DialogSolveTask2",
                                                   tr("Entering the start date of the GPM works at the facilities")))
        self.label.setText(_translate("DialogSolveTask2", tr("Start date of GPM works at the facilities")))
        self.pushActDoc.setText(_translate("DialogSolveTask2", tr("Interactions with the document")))
        self.pushSolveTask.setText(_translate("DialogSolveTask2", tr("Solve Task")))
        self.pushGetData.setText(_translate("DialogSolveTask2", tr("Get Data")))
        self.pushShowCalSMR.setText(_translate("DialogSolveTask2", tr("Display the calendar schedule of the SMR")))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogSolveTask2 = QtWidgets.QDialog()
    ui = Ui_DialogSolveTask2()
    ui.setupUi(DialogSolveTask2)
    DialogSolveTask2.show()
    sys.exit(app.exec_())