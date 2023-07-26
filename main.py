# from PyQt5 import uic
import datetime
import calendar
# библиотеки для решения задач и интерфейса
import numpy as np
import pandas as pd
import plotly.express as px
from pulp import *
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox, QMainWindow, QDialog, QHeaderView
from PyQt5.QtGui import QPalette, QBrush, QFont, QColor
from PyQt5.QtCore import Qt, QTranslator, QDate
from PyQt5.QtGui import QTextTableFormat, QTextCursor
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from Translation import tr

# библиотека для работы с БД
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import closing

# подключаемые классы из файлов
from mainwindow import Ui_MainWindow
from DialogMatrix import DialogMatrix
from Dialog_authorization import Ui_Dialog
from Dialog_Size import Ui_Dialog_Size
from Dialog_About import Ui_Dialog_About
from Dialog_Change_window_theme import Ui_Dialog_Change_Window_Theme
from DialogSolveTask1 import Ui_DialogSolveTask1
from DialogActions import Ui_DialogActions
from Dialog_Add_Search_Delete_Data import Ui_DialogDelADDSearch
from Dialog_AddToDirectoryOfWorksTable import Ui_AddToDirectoryOfWorksTable
from Dialog_AddToRegBuildingsInDistrictTable import Ui_AddToRegBuildingsInDistrictTable
from Dialog_AddToStateElementEstimatesTable import Ui_AddToStateElementEstimatesTable
from DialogUpdateState_Element_Estimates import Ui_DialogUpdateState_Element_Estimates
from DialogUpdateDirOfWorks import Ui_DialogUpdateDirOfWorks
from DialogUpdateRegBuildingsInDistrict import Ui_DialogUpdateRegBuildingsInDistrict
from Dialog_Administration import Ui_DialogAdministration
from DialogUpdateUser import Ui_DialogUpdateUser
from DialogAddUser import Ui_DialogAddUser
from DialogSolveTask2 import Ui_DialogSolveTask2
from DialogCalendarPlanSMR import DialogCalendarPlanSMR
from DialogSelectWeek_Task4 import DialogWeeklyPlanELWorks
from DialogADDL_vol_works import Ui_DialogADDL_vol_works
from DialogUpdateL_vol_works import Ui_DialogUpdateL_vol_works
from DialogAddDataToAM_works_per_build_GPM import Ui_DialogAddDataToAM_works_per_build_GPM
from DialogUpdateDataToAM_works_per_build_GPM import Ui_DialogUpdateDataToAM_works_per_build_GPM
from DialogAddToReport_on_compl_works import Ui_DialogAddToReport_on_compl_works
from DialogUpdateInReport_on_compl_works import Ui_DialogUpdateInReport_on_compl_works


class Dialog_Change_Window_theme(QDialog, Ui_Dialog_Change_Window_Theme):
    def __init__(self, parent=None):
        super(Dialog_Change_Window_theme, self).__init__(parent)
        self.setupUi(self)
        self.radioButtonLigthTheme.setChecked(True)
        self.pushButton.clicked.connect(self.checkRadioButton)

    def checkRadioButton(self):
        if self.radioButtonLigthTheme.isChecked():
            onClickedLightTheme()
        if self.radioButtonBlackTheme.isChecked():
            onClickedBlackTheme()

    def ChangeWindowColor(self):
        self.show()
        if self.radioButtonLigthTheme.isChecked():
            self.radioButtonLigthTheme.setChecked(True)
        if self.radioButtonBlackTheme.isChecked():
            self.radioButtonBlackTheme.setChecked(True)


class Dialog_About(QDialog, Ui_Dialog_About):
    def __init__(self, parent=None):
        super(Dialog_About, self).__init__(parent)
        self.setupUi(self)

    def About(self):
        self.label.setFont(QFont("Times", 12))
        self.textEdit.setFont(QFont("Times", 12))
        self.textEdit.setText(tr("Sbrodov Dmitrii ITSTMS 4-4"))
        self.show()


class Dialog_Size(QDialog, Ui_Dialog_Size):
    def __init__(self, parent=None):
        super(Dialog_Size, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.addItems(["640 x 480",
                                "720 x 576",
                                "1280 x 720",
                                "1920 x 1080"])
        self.comboBox.setCurrentIndex(1)


class DialogAuth(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(DialogAuth, self).__init__(parent)
        self.setupUi(self)
        self.trans = QTranslator()
        self.radioButton.setCheckable(True)
        self.radioButton_2.setCheckable(True)
        self.radioButton_2.setChecked(True)
        self.pushButtonLogIn.clicked.connect(self.checkAuth)
        self.radioButton.clicked.connect(self.trigger_russian)
        self.radioButton_2.clicked.connect(self.trigger_english)

    def trigger_russian(self):
        if not self.radioButton_2.setChecked(False):
            self.radioButton_2.setChecked(False)
        self.radioButton.setChecked(True)
        self.trans.load('main.en.qm')
        _app = QApplication.instance()  # получить экземпляр приложения
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        MainWindow.action_4.setChecked(True)
        MainWindow.trigger_russian()

    def trigger_english(self):
        if not self.radioButton.setChecked(False):
            self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(True)
        self.trans.load('main.ru.qm')
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        MainWindow.action_5.setChecked(True)
        MainWindow.trigger_english()

    def checkAuth(self):
        # курсор для работы с бд открываю
        # делаю запрос для авторизации
        # и автоматически закрываю
        with closing(connect_to_DB()) as conn:
            # запускаю курсор с запросом и делаю результат списком
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select user_login, user_password, position FROM users')
                Found = False
                for row in cursor:
                    if self.lineEdit.text() == row[0] and self.lineEdit_2.text() == row[1] \
                            and row[2] != "Администратор":
                        MainWindow.current_user.setText(MainWindow.getLabel() + row[2])
                        self.close()
                        MainWindow.show()
                        Found = True
                        break
                    elif self.lineEdit.text() == row[0] and self.lineEdit_2.text() == row[1] \
                            and row[2] == "Администратор":
                        MainWindow.current_user.setText(MainWindow.getLabel() + row[2])
                        MainWindow.Administration.setEnabled(True)
                        self.close()
                        MainWindow.show()
                        Found = True
                        break
                if not Found:
                    msgBoxError = QMessageBox()
                    msgBoxError.setWindowTitle(tr("Authorization Error"))
                    msgBoxError.setText(tr("Incorrect login or password!\n"
                                           "Please, authorization again."))
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                    self.show()
                    msgBoxError.exec()


def createPaletteDark():
    paletteDark = QPalette()
    paletteDark.setColor(QPalette.Window, QColor(53, 53, 53))
    paletteDark.setColor(QPalette.WindowText, Qt.white)
    paletteDark.setColor(QPalette.Base, QColor(25, 25, 25))
    paletteDark.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    paletteDark.setColor(QPalette.ToolTipBase, Qt.black)
    paletteDark.setColor(QPalette.ToolTipText, Qt.white)
    paletteDark.setColor(QPalette.Text, Qt.white)
    paletteDark.setColor(QPalette.Button, QColor(53, 53, 53))
    paletteDark.setColor(QPalette.ButtonText, Qt.white)
    paletteDark.setColor(QPalette.BrightText, Qt.red)
    paletteDark.setColor(QPalette.Link, QColor(42, 130, 218))
    paletteDark.setColor(QPalette.Highlight, QColor(42, 130, 218))
    paletteDark.setColor(QPalette.HighlightedText, Qt.white)
    return paletteDark


def createPaletteLight():
    paletteLight = QPalette()
    paletteLight.setBrush(QPalette.Highlight, QBrush(Qt.white))
    paletteLight.setBrush(QPalette.HighlightedText, QBrush(Qt.red))
    paletteLight.setColor(QPalette.Window, Qt.white)
    return paletteLight


def onClickedLightTheme():
    palette = createPaletteLight()
    app.setStyle("Fusion")
    app.setPalette(palette)


def onClickedBlackTheme():
    palette = createPaletteDark()
    app.setStyle("Windows")
    app.setPalette(palette)


def connect_to_DB():
    return psycopg2.connect(dbname='Diplome', user='Dimacik',
                            password='************', host='127.0.0.1')


class DialogAddUser(QDialog, Ui_DialogAddUser):
    def __init__(self, parent=None):
        super(DialogAddUser, self).__init__(parent)
        self.setupUi(self)
        self.pushAddUser.clicked.connect(self.addUserData)

    @staticmethod
    def showAddDataNotice():
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data adding!"))
        msgBoxFileLoaded.setText(tr('The data has been successfully pressed into the table "users" !'))
        msgBoxFileLoaded.exec_()

    def addUserData(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""INSERT INTO users("user_login", "user_password", "position") 
                                VALUES(%s, %s, %s)""",
                               (self.lineUserLogin.text().strip('"'),
                                self.lineUserPassword.text().strip('"'),
                                self.linePosition.text().strip('"')))
                conn.commit()
                self.showAddDataNotice()
                self.close()


class DialogUpdateUser(QDialog, Ui_DialogUpdateUser):
    def __init__(self, data_old, parent=None):
        super(DialogUpdateUser, self).__init__(parent)
        self.setupUi(self)
        self.old_user = data_old
        self.pushUpdateUser.clicked.connect(self.UpdateUser)

    @staticmethod
    def showUpdatedDataNotice():
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data modification!"))
        msgBoxFileLoaded.setText(tr('The data has been successfully changed in the table "users"!'))
        msgBoxFileLoaded.exec_()

    def UpdateUser(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Update users 
                set "user_login" = %s, "user_password" = %s, "position" = %s
                where user_login = %s""",
                               (self.lineUserLogin.text().strip('"'),
                                self.lineUserPassword.text().strip('"'),
                                self.linePosition.text().strip('"'),
                                self.old_user))
                conn.commit()
                self.showUpdatedDataNotice()
                self.close()


class DialogAdministration(QDialog, Ui_DialogAdministration):
    def __init__(self, parent=None):
        super(DialogAdministration, self).__init__(parent)
        self.setupUi(self)
        # массив с данными из таблицы БД users
        self.data = []
        # данные конкретной ячейки
        self.CellData = ""
        # выбранный индекс таблицы
        self.index_column_table = 0
        # данные для поиска в БД
        self.search_data = ""

    def showAdministration(self):
        Dialog = QtWidgets.QDialog()
        self.setupUi(Dialog)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.showUsers()
        self.pushAddData.clicked.connect(self.addUserData)
        self.pushUpdateData.clicked.connect(self.updateUserData)
        self.pushDeleteData.clicked.connect(self.deleteUserData)
        self.pushSearch.clicked.connect(self.searchUserData)
        self.tableView.clicked.connect(self.clickedCell)
        self.lineSearch.textChanged.connect(self.lineEditCheck)
        Dialog.exec_()

    def lineEditCheck(self):
        if self.lineSearch.text() == "":
            self.showUsers()
        else:
            return

    def clickedCell(self):
        self.CellData = self.tableView.model().data(self.tableView.currentIndex(), role=0)
        self.lineSearch.setText(self.CellData)
        self.index_column_table = self.tableView.selectedIndexes()[0].column() + 1

    def addUserData(self):
        DialogAdd = DialogAddUser()
        DialogAdd.exec_()
        self.showUsers()

    @staticmethod
    def showSuccessfullDeletion():
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data deletion!"))
        msgBoxFileLoaded.setText(tr("User's data has been successfully deleted"
                                    '  from the table "users"!'))
        msgBoxFileLoaded.exec_()

    def deleteUserData(self):
        if self.index_column_table == 1:
            delete_data = self.CellData.strip('"')
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("Delete from users where user_login = %s",
                                   (delete_data,))
                    conn.commit()
            self.showUsers()
            self.showSuccessfullDeletion()

    def updateUserData(self):
        if self.index_column_table == 1:
            update_data = self.CellData.strip('"')
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Select "user_login", "user_password",
                     "position" from users where user_login = %s""",
                                   (update_data,))
                    Update_user_data = cursor.fetchall()
                    DialogUpdate = DialogUpdateUser(update_data)
                    DialogUpdate.lineUserLogin.setText(Update_user_data[0][0])
                    DialogUpdate.lineUserPassword.setText(Update_user_data[0][1])
                    DialogUpdate.linePosition.setText(Update_user_data[0][2])
                    DialogUpdate.exec_()
            self.showUsers()

    def searchUserData(self):
        self.search_data = self.lineSearch.text().strip('"')
        if self.index_column_table == 1:
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Select "user_login", "user_password", "position" 
                                    from users where user_login = %s""",
                                   (self.search_data,))
                    data_user = cursor.fetchall()
                    model = TableModel(pd.DataFrame(data_user,
                                                    columns=["user_login",
                                                             "user_password",
                                                             "position"],
                                                    index=[i + 1 for i in range(len(data_user))]))
                    self.tableView.setModel(model)
        else:
            return

    def showUsers(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "user_login", "user_password", "position" from users""")
                self.data = cursor.fetchall()
        self.tableView.setModel(TableModel(pd.DataFrame(self.data,
                                                        columns=["user_login",
                                                                 "user_password",
                                                                 "position"],
                                                        index=[i + 1 for i in range(len(self.data))])))


# класс для решения задачи Ведомость потребности в кадрах
class DialogSolveTask3:
    def __init__(self):
        self.Dataframe = pd.DataFrame()
        self.DataframeTotal = pd.DataFrame()
        # Данные из БД
        # даннные по рабочим (из справочника рабочих)
        self.rec_data_workers_info = []
        # данные из ведомости объёмов работ
        self.rec_data_list_of_vol_works = []
        # данные по объектам
        self.records_buildings = []
        # данные из календарного плана эл.монтаж. работ
        self.dataCalPlanELWorks = []
        # данные из штатного расписания и справочника работ (связанных по номеру ГЭСН)
        self.dataStaff = []
        # этажность домов
        self.house_properties = []
        # Трудозатраты СМР в чел.ч => Трудозатраты СМР итог
        self.time_of_work_dict_total = []
        # Трудозатраты СМР в чел.ч
        self.time_of_work = []
        # все массивы с данными DataFrame в одном массиве
        self.allInOne = []

    def getData(self):
        self.dataClear()
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select * from calendar_plan_el_works""")
                self.dataCalPlanELWorks = cursor.fetchall()
                for j, item in enumerate(self.dataCalPlanELWorks):
                    for kj, ktem in enumerate(item):
                        if kj == 3:
                            cursor.execute("""Select "brigade_id", "amount_of_workers"
                                            from dir_prof_workers_brig
                                            where "brigade_id" = %s""", (ktem,))
                            self.rec_data_workers_info += cursor.fetchall()
                cursor.execute("""Select Distinct "Position", "sp_category" from staffing_arrangements""")
                self.dataStaff = cursor.fetchall()
                cursor.execute('Select work_name, "Scope_of_SMR_in_thousand_rub_per_floor",'
                               'duration_of_work from list_of_volume_of_works')
                self.rec_data_list_of_vol_works = cursor.fetchall()
                for i, item in enumerate(self.dataCalPlanELWorks):
                    for k, ktem in enumerate(item):
                        if k == 2:
                            cursor.execute("""Select "Total_number_of_floors" from reg_buildings_in_district 
                                                          where "Building_name_reg" = %s
                                                          Order by "Number_of_building" ASC""",
                                           (ktem,))
                            self.records_buildings += cursor.fetchall()
            msgBoxError = QMessageBox()
            msgBoxError.setWindowTitle(tr("The task is solved"))
            msgBoxError.setText(tr('The task "Statement of personnel requirements" has been successfully solved!'))
            msgBoxError.exec_()

    def dataClear(self):
        self.time_of_work = []
        self.house_properties = []
        self.time_of_work_dict_total = np.array([])
        self.rec_data_list_of_vol_works = []
        self.rec_data_workers_info = []
        self.allInOne = []
        self.Dataframe = pd.DataFrame()
        self.DataframeTotal = pd.DataFrame()
        self.records_buildings = []
        self.dataStaff = []

    def solveTask(self):
        self.getData()
        for val in self.records_buildings:
            for jx, val2 in enumerate(val):
                self.house_properties.append(val2)
        for item in self.rec_data_list_of_vol_works:
            for j, val in enumerate(item):
                if j == 2:
                    self.time_of_work.append(val)
        # Трудозатраты СМР в чел.ч => Трудозатраты СМР итог
        self.time_of_work_dict_total = np.sum([[i * j for i in self.time_of_work]
                                               for j in self.house_properties], axis=1)
        # Трудозатраты СМР в чел.ч
        self.time_of_work = [[i * j for i in self.time_of_work] for j in self.house_properties]
        summa = []
        s = 0
        for k, ktem in enumerate(self.time_of_work):
            compare = max(ktem)
            for lo, ltem in enumerate(ktem):
                if ltem != compare:
                    s += ltem
            summa.append(s)
        am_w_per_brig, massive_help = [], []
        for item1, item2 in zip(summa, self.time_of_work_dict_total):
            am_w_per_brig.append(item2 / item1)
        am_w_per_brig_total = []
        brigade = []
        for d, data in enumerate(self.rec_data_workers_info):
            for da, dat in enumerate(data):
                if da == 1:
                    for am, item in enumerate(am_w_per_brig):
                        if am == 0:
                            massive_help.append(data[0])
                            massive_help.append(dat - round(dat / item))
                            massive_help.append(round(dat / item))
                            massive_help.append(dat)
                            am_w_per_brig_total.append(massive_help)
                            massive_help = []
        indexesBrig = []
        specialty = []
        sp_category = []
        am_of_workers = []
        for i, item in enumerate(am_w_per_brig_total):
            for j, jtem in enumerate(item):
                if j == 1:
                    indexesBrig.append(item[0])
                    specialty.append(self.dataStaff[0][0])
                    am_of_workers.append(jtem)
                    sp_category.append(self.dataStaff[0][1])
                    brigade.append("Бригада №" + str(item[0]) + " -> " + str(jtem) + " чел-к -> "
                                   + str(self.dataStaff[0][1]) + " разряд")
                elif j == 2:
                    brigade.append("Бригада №" + str(item[0]) + " -> " + str(jtem) + " чел-к -> "
                                   + str(self.dataStaff[1][1]) + " разряд")
                    indexesBrig.append(item[0])
                    specialty.append(self.dataStaff[0][0])
                    am_of_workers.append(jtem)
                    sp_category.append(self.dataStaff[1][1])
        dduration0 = []
        dduration = []
        for d, duration in enumerate(self.dataCalPlanELWorks):
            for k, dur in enumerate(duration):
                if k == 6:
                    dduration0.append(dur)
        for am, amount in enumerate(am_w_per_brig_total):
            for d, dur in enumerate(dduration0):
                if am == 0:
                    dduration.append(round(dur * amount[1] / amount[3]))
                    dduration.append(round(dur * amount[2] / amount[3]))
        start_dates = [self.dataCalPlanELWorks[0][4] +
                       datetime.timedelta(days=i) for i in range(len(dduration))]
        end_dates = [self.dataCalPlanELWorks[0][4] +
                     datetime.timedelta(days=num + 3)
                     for n, num in enumerate(dduration)]
        days_start_to_end = [(self.dataCalPlanELWorks[0][4] +
                              datetime.timedelta(days=num) -
                              self.dataCalPlanELWorks[0][4]).days for n, num in enumerate(dduration)]
        self.Dataframe = pd.DataFrame(
            {
                'Brigade': brigade,
                'start_num': start_dates,
                'end_num': end_dates,
                'days_start_to_end': days_start_to_end
            })
        self.DataframeTotal = pd.DataFrame(
            {
                'Номер бригады': indexesBrig,
                'Специальность кадра': specialty,
                'Разряд специалиста': sp_category,
                'Кол-во работников': am_of_workers,
                'Дата начала выполнения работ согласно календарному плану, дн., месяц.': start_dates,
                'Продолжительность выполнения работ, согласно календарному плану, дн.': days_start_to_end
            }, index=[i + 1 for i in range(len(indexesBrig))]
        )
        df_copy = pd.DataFrame(
            {
                'Номер бригады': indexesBrig,
                'Специальность кадра': specialty,
                'Разряд специалиста': sp_category,
                'Кол-во работников': am_of_workers,
                'Дата начала выполнения работ согласно календарному плану, дн., месяц.': start_dates,
                'Продолжительность выполнения работ, согласно календарному плану, дн.': days_start_to_end
            }, index=[i + 1 for i in range(len(indexesBrig))]
        )
        for k in range(len(indexesBrig)):
            MainWindow.tableView.setSpan(k, 0, 1, 1)
            MainWindow.tableView.setSpan(k, 1, 1, 1)
            MainWindow.tableView.setSpan(k, 2, 1, 1)
            MainWindow.tableView.setSpan(k, 4, 1, 1)
        MainWindow.tableView.setModel(TableModel(df_copy))
        # пример диаграммы ГАНТА через plotly
        fig = px.timeline(self.Dataframe, x_start="start_num",
                          x_end="end_num", y="Brigade", title="Время выполнения работ"
                                                              " электромонтажниками")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            title_font_size=42,
            font_size=18,
            title_font_family="Times New Romance"
        )
        fig.show()
        self.ActionScreen()
        self.CreateViewAndInsertData()
        MainWindow.Task5.setEnabled(True)

    def ConstructDataFrame(self):
        columns = []
        for col in range(self.DataframeTotal.columns.size):
            columns.append(col)
        Data = pd.DataFrame([], index=[], columns=columns)
        Data.at[1, 0] = "Согласовываю"
        Data.at[2, 0] = "Подрядчик:"
        Data.at[3, 0] = "____________(__________)"
        Data.at[1, self.DataframeTotal.columns.size - 1] = "Утверждаю"
        Data.at[2, self.DataframeTotal.columns.size - 1] = "Заказчик:"
        Data.at[3, self.DataframeTotal.columns.size - 1] = "____________(__________)"
        self.DataframeTotal.loc[self.DataframeTotal.index.size + 1] = ""
        self.DataframeTotal.at[self.DataframeTotal.index.size + 2,
                               self.DataframeTotal.columns[
                                   self.DataframeTotal.columns.size - 1]] = "Составил Начальник ПТО"
        self.DataframeTotal.at[self.DataframeTotal.index.size + 3,
                               self.DataframeTotal.columns[
                                   self.DataframeTotal.columns.size - 1]] = "____________(__________)"
        self.DataframeTotal.at[self.DataframeTotal.index.size + 4,
                               self.DataframeTotal.columns[
                                   self.DataframeTotal.columns.size - 1]] = "«___» __________ _________г"
        return Data

    def ActionScreen(self):
        pr = DialogActions(self.DataframeTotal, self.ConstructDataFrame(), "Ведомость потребности в кадрах")
        pr.cursor.movePosition(QTextCursor.Start)
        pr.cursor.insertText("Согласовываю" + " " * 226 + "Утверждаю" + "\n")
        pr.cursor.insertText("Подрядчик:" + " " * 230 + "Заказчик:" + "\n")
        pr.cursor.insertText("____________(__________)" + " " * 208 + "____________(__________)" + "\n")
        pr.cursor.insertBlock()
        # вычитаю добавленные строки с печатью
        table = pr.cursor.insertTable(self.DataframeTotal.index.size - 3, self.DataframeTotal.columns.size + 1)
        for i, item in enumerate(self.DataframeTotal.columns):
            headerCell = table.cellAt(0, i)
            headerCellCursor = headerCell.firstCursorPosition()
            headerCellCursor.insertText(item)
        for j, r in enumerate(self.DataframeTotal.values):
            if not r.any():
                break
            self.allInOne.append(r)
        for j, r in enumerate(self.allInOne):
            for k, rok in enumerate(r):
                cell = table.cellAt(j + 1, k)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(str(rok))
        massive_trapdoor = ["Составил Начальник ПТО",
                            "____________(__________)",
                            "«___»___________________г"]
        pr.cursor.movePosition(QTextCursor.End)
        pr.cursor.insertBlock()
        for i, item in enumerate(massive_trapdoor, start=1):
            if i != 0:
                pr.cursor.insertText("\n")
            pr.cursor.insertText(" " * 248 + item)
        pr.exec_()

    def CreateViewAndInsertData(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("Select EXISTS (Select * FROM pg_tables WHERE tablename = "
                               "'tlist_of_dem_in_workers')")
                element = cursor.fetchone()
                if element:
                    cursor.execute("Drop Table tlist_of_dem_in_workers CASCADE")
                    cursor.execute("Create Table tlist_of_dem_in_workers"
                                   "(Brigade_id smallint, Position character varying(50),"
                                   "sp_category smallint, Amount_of_workers smallint,"
                                   "St_date_brig_work date, Duration_brig_work smallint)")
                for r in self.allInOne:
                    cursor.execute("INSERT INTO tlist_of_dem_in_workers "
                                   "Values(%s, %s, %s, %s, %s, %s)",
                                   (r[0], r[1], r[2], r[3], r[4], r[5]))

                cursor.execute("Create or replace view List_of_dem_in_workers"
                               " as select Brigade_id, Position, sp_category,"
                               " Amount_of_workers, St_date_brig_work, Duration_brig_work"
                               " from tlist_of_dem_in_workers")
                conn.commit()


class DialogSelectWeekTask4(QDialog, DialogWeeklyPlanELWorks):
    def __init__(self, parent=None):
        super(DialogSelectWeekTask4, self).__init__(parent)
        self.setupUi(self)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.CellData = ''
        self.column_index = 0
        self.row_index = 0
        self.tableView.clicked.connect(self.SelectedData)
        self.resize(1920, 900)
        # данные из БД
        self.DataCalendarPlan = []
        self.Data2022 = []
        self.Data2023 = []
        self.DataYearTotal = []
        # данные для датафрейма
        self.resultQuery = []
        # выбранный объект из строки с датой
        self.chose_obj = ''
        self.date = ''
        # колонки датафрейма с календарным графиком
        self.columns = ["Наименование объекта",
                        "Ст-ть СМР в тыс. руб",
                        "Затраты труда в чел.ч",
                        "Численность бригады, чел.",
                        "Продолжительность в дн."]
        self.cols_doc = []
        # Датафрейм для выходного документа и календарного плана
        self.DataFrameCalPlan = pd.DataFrame()
        self.DataFrameDoc = pd.DataFrame()
        self.lineEditRule.setFont(QFont("Times", 12))

    def SelectedData(self):
        # данные конкретной ячейки
        self.CellData = self.tableView.model().data(self.tableView.currentIndex(), role=0)
        # выбранный индекс таблицы
        self.column_index = self.tableView.selectedIndexes()[0].column() + 1
        self.row_index = self.tableView.selectedIndexes()[0].row() + 1
        self.chose_obj = self.tableView.model().index(self.row_index - 1, 0).data()
        if self.column_index > 5:
            week_dates = []
            dates = []
            counter_week = 0
            for i, ind in enumerate(self.columns):
                if i >= self.column_index - 1 and counter_week != 5:
                    date = datetime.datetime.strptime(ind, "%d-%m-%Y").weekday()
                    dates.append(ind)
                    if calendar.day_name[date] == 'Monday':
                        week_dates.append("Понедельник (" + ind + ")")
                    elif calendar.day_name[date] == 'Tuesday':
                        week_dates.append("Вторник (" + ind + ")")
                    elif calendar.day_name[date] == 'Wednesday':
                        week_dates.append("Среда (" + ind + ")")
                    elif calendar.day_name[date] == 'Thursday':
                        week_dates.append("Четверг (" + ind + ")")
                    elif calendar.day_name[date] == 'Friday':
                        week_dates.append("Пятница (" + ind + ")")
                    counter_week += 1
            self.date = dates[0]
            self.setresultQuery(dates[0], self.chose_obj)
            count_obj_with_Plan_for_w = 0
            for ltem in self.resultQuery:
                if ltem[9] is not None and ltem[10] is not None:
                    # or (ltem[9] > 0 and ltem[10] > 0):
                    count_obj_with_Plan_for_w += 1
            for i, item in enumerate(self.resultQuery):
                if item[9] is not None and item[10] is not None:  # or (item[9] > 0 and item[10] > 0):
                    item[10] = round(8 * item[4] / item[7]) * 5
                    for k in range(len(week_dates)):
                        item.append(str(round(8 * item[4] / item[7])) + " " +
                                    str(item[6]) + " / " + str(round(8 * item[4] / count_obj_with_Plan_for_w))
                                    + " чел.ч")
                for j, jtem in enumerate(item):
                    if jtem is None:
                        item[j] = 0
            # будущая настройка tableview и формирования dataframe для отображения
            self.cols_doc = ["Наименование объекта",
                             "Номер бригады",
                             "Специальность рабочего",
                             "Разряд специалиста",
                             "Количество рабочих в бригаде, чел.",
                             "Наименование работы", "Ед. изм",
                             "К-во чел.час на ед-цу изм., чел.ч",
                             "Объём на объект",
                             "Выполненный объём работ на {0}".format(dates[0]),
                             "Плановый объём работ на неделю"]
            for wd in week_dates:
                self.cols_doc.append(wd)
            self.DataFrameDoc = pd.DataFrame(self.resultQuery,
                                             index=[i + 1 for i in range(len(self.resultQuery))],
                                             columns=self.cols_doc)
            df_copy = pd.DataFrame(self.resultQuery,
                                   index=[i + 1 for i in range(len(self.resultQuery))],
                                   columns=self.cols_doc)
            for i in range(len(self.resultQuery)):
                MainWindow.tableView.setSpan(i, 0, len(self.resultQuery), 1)
                MainWindow.tableView.setSpan(i, 1, len(self.resultQuery), 1)
                MainWindow.tableView.setSpan(i, 2, len(self.resultQuery), 1)
                MainWindow.tableView.setSpan(i, 4, len(self.resultQuery), 1)
            MainWindow.tableView.setModel(TableModel(df_copy))
            if len(self.resultQuery) > 0:
                self.ActionScreen()

    def ConstructDataFrame(self):
        columns = []
        for col in range(self.DataFrameDoc.columns.size):
            columns.append(col)
        Data = pd.DataFrame([], index=[], columns=columns)
        Data.at[1, 0] = "Согласовываю"
        Data.at[2, 0] = "Подрядчик:"
        Data.at[3, 0] = "____________(__________)"
        Data.at[1, self.DataFrameDoc.columns.size - 1] = "Утверждаю"
        Data.at[2, self.DataFrameDoc.columns.size - 1] = "Заказчик:"
        Data.at[3, self.DataFrameDoc.columns.size - 1] = "____________(__________)"
        Data.at[4, self.DataFrameDoc.columns.size - 10] = "Недельно-суточный график электромонтажных работ" \
                                                          " на объекте _________"
        Data.at[5, self.DataFrameDoc.columns.size - 10] = "на одну неделю с_____________"
        self.DataFrameDoc.loc[self.DataFrameDoc.index.size + 1] = ""
        self.DataFrameDoc.at[self.DataFrameDoc.index.size + 2,
                             self.DataFrameDoc.columns[self.DataFrameDoc.columns.size - 1]] = "Составил Начальник ПТО"
        self.DataFrameDoc.at[self.DataFrameDoc.index.size + 3,
                             self.DataFrameDoc.columns[self.DataFrameDoc.columns.size - 1]] = "____________(__________)"
        self.DataFrameDoc.at[self.DataFrameDoc.index.size + 4,
                             self.DataFrameDoc.columns[self.DataFrameDoc.columns.size - 1]] = \
            "«___» __________ _________г "
        return Data

    def ActionScreen(self):
        pr = DialogActions(self.DataFrameDoc, self.ConstructDataFrame(), "Нед-сут. граф. эл.монтаж.работ", True)
        pr.cursor.movePosition(QTextCursor.Start)
        pr.cursor.insertText("Согласовываю" + " " * 226 + "Утверждаю" + "\n")
        pr.cursor.insertText("Подрядчик:" + " " * 230 + "Заказчик:" + "\n")
        pr.cursor.insertText("____________(__________)" + " " * 208 + "____________(__________)" + "\n")
        pr.cursor.insertText(" " * 104 +
                             "Недельно-суточный график электромонтажных работ на объекте:"
                             + "\n" + " " * 104 + self.chose_obj + "\n")
        pr.cursor.insertText(" " * 135 + "на одну неделю с {0}".format(self.date) + "\n")
        pr.cursor.insertBlock()
        table = pr.cursor.insertTable(self.DataFrameDoc.index.size - 3, self.DataFrameDoc.columns.size + 1)

        for lo in range(self.DataFrameDoc.columns.size):
            table.mergeCells(lo + 1, 0, len(self.resultQuery), 1)
            table.mergeCells(lo + 1, 1, len(self.resultQuery), 1)
            table.mergeCells(lo + 1, 2, len(self.resultQuery), 1)
            table.mergeCells(lo + 1, 4, len(self.resultQuery), 1)

        for i, item in enumerate(self.DataFrameDoc.columns):
            headerCell = table.cellAt(0, i)
            headerCellCursor = headerCell.firstCursorPosition()
            headerCellCursor.insertText(item)
        pred_Obj = self.resultQuery[0][0]
        pred_brigate = self.resultQuery[0][1]
        pred_pos = self.resultQuery[0][2]
        pred_am_of_workers = self.resultQuery[0][4]
        for j, r in enumerate(self.resultQuery):
            for k, rok in enumerate(r):
                cell = table.cellAt(j + 1, k)
                cellCursor = cell.firstCursorPosition()
                if rok == pred_Obj:
                    cellCursor.insertText(str(rok))
                    pred_Obj = ""
                if rok == pred_brigate:
                    cellCursor.insertText(str(rok))
                    pred_brigate = ""
                if rok == pred_pos:
                    cellCursor.insertText(str(rok))
                    pred_pos = ""
                if rok == pred_am_of_workers:
                    cellCursor.insertText(str(rok))
                    pred_am_of_workers = ""
                elif k >= 3 and k != 4:
                    cellCursor.insertText(str(rok))

        massive_trapdoor = ["Составил Начальник ПТО",
                            "____________(__________)",
                            "«___»___________________г"]
        pr.cursor.movePosition(QTextCursor.End)
        pr.cursor.insertBlock()
        for i, item in enumerate(massive_trapdoor, start=1):
            if i != 0:
                pr.cursor.insertText("\n")
            pr.cursor.insertText(" " * 248 + item)
        pr.exec_()

    def setresultQuery(self, date, obj):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""select cal."building_name", cal."brigade_id", staff."Position",
                               staff."sp_category", brig."amount_of_workers",
                               rep."work_name_report", rep."unit", st."labor_cost",
                               rep."volume_per_object", rep."act_am_work_performed", 
                               Case 
                                   When rep."act_am_work_performed" is not NuLL 
                                   then round(5*8*brig."amount_of_workers" / st."labor_cost")
                               END "Plan_vol_per_week"
                               
                               from  calendar_plan_el_works cal, report_on_compl_works rep,
                               state_element_estimates st, directory_of_works dir,
                               staffing_arrangements staff, dir_prof_workers_brig brig
                               
                               where rep."building_name" =  cal."building_name" and dir."work_name" = 
                               rep."work_name_report" and brig."brigade_id" = cal."brigade_id" and
                                st."gesn_id" = dir."gesn_id" and st."gesn_id" = staff."gesn_id" and
                                dir."gesn_id" = staff.gesn_id and rep."end_date_act_am_work_perf" = %s 
                                and  cal."building_name" = %s
                               order by cal."building_name" """, (date, obj.strip('"')))
                self.resultQuery = cursor.fetchall()
                if len(self.resultQuery) > 0:
                    msgBoxError = QMessageBox()
                    msgBoxError.setWindowTitle(tr("Data status"))
                    msgBoxError.setText(tr("The data was successfully received from the database"
                                           " and the task was solved!"))
                    msgBoxError.exec_()
                else:
                    msgBoxError = QMessageBox()
                    msgBoxError.setWindowTitle(tr("Data status"))
                    msgBoxError.setText(tr("In the report of the foreman there are"
                                           " no works completed for the chosen date!"))
                    msgBoxError.exec_()

    def getData(self):
        self.clearData()
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""select Distinct  cal."building_name",
                 "Cost_of_SMR", "Labor_per_obj", d."amount_of_workers", cal."duration_of_works_in_days"
                            from calendar_plan_el_works cal, dir_prof_workers_brig d
                            where d."brigade_id" = cal."brigade_id" """)
                self.DataCalendarPlan = cursor.fetchall()
                cursor.execute("""select Distinct
                        pr."working_days_in_2022"
                        from production_calendar pr, calendar_plan_el_works cal
                        where 
                        pr."working_days_in_2022" between cal."st_date_electr_iworks"
                        and cal."end_date_electr_iworks"
                        order by pr."working_days_in_2022" """)
                self.Data2022 = cursor.fetchall()
                if len(self.Data2022) > 0:
                    for row in self.Data2022:
                        for item in row:
                            self.DataYearTotal.append(item)
                cursor.execute("""select Distinct
                        pr."working_days_in_2023"
                        from production_calendar pr, calendar_plan_el_works cal
                        where 
                        pr."working_days_in_2023" between cal."st_date_electr_iworks" and
                        cal."end_date_electr_iworks"
                        order by pr."working_days_in_2023" """)
                self.Data2023 = cursor.fetchall()
                if len(self.Data2023) > 0:
                    for row in self.Data2023:
                        for item in row:
                            self.DataYearTotal.append(item)

    def clearData(self):
        self.columns = ["Наименование объекта",
                        "Ст-ть СМР в тыс. руб",
                        "Затраты труда в чел.ч",
                        "Численность бригады, чел.",
                        "Продолжительность в дн."]
        self.DataCalendarPlan.clear()
        self.Data2022.clear()
        self.Data2023.clear()
        self.DataYearTotal.clear()
        self.DataFrameCalPlan = pd.DataFrame()

    def solveTask(self):
        self.getData()
        self.lineEditRule.setText(tr("Select the start date of the week from the calendar plan..."))
        for d, dat in enumerate(self.DataCalendarPlan):
            for pr in range(len(self.DataYearTotal)):
                dat.append("_" * 8)
        for i, item in enumerate(self.DataYearTotal):
            self.columns.append(item.strftime("%d-%m-%Y"))
        self.DataFrameCalPlan = pd.DataFrame(self.DataCalendarPlan,
                                             index=[i + 1 for i in range(len(self.DataCalendarPlan))],
                                             columns=self.columns)
        self.tableView.setModel(TableModel(self.DataFrameCalPlan))
        self.retranslateUi(self)
        self.show()


class DialogSolveTask2(QDialog, Ui_DialogSolveTask2):
    def __init__(self, parent=None):
        super(DialogSolveTask2, self).__init__(parent)
        self.setupUi(self)
        # Данные из БД
        self.data_from_production_calendar = []
        self.data_from_db_l_costs = []
        self.data_machines_mechanisms = []
        # Выбранная дата из календаря
        self.date_field = QDate()
        # массив с днями и затратами
        self.labor_days = []
        # колонки и строчки tableview
        self.columns = ["Продолжительность, в дн.",
                        "Затраты ГПМ, в маш.ч",
                        "Продолжительность, в дн."]
        self.columns2 = ["Название грузоподъемных машин и механизмов",
                         "Грузоподъёмность максимальная, т",
                         "Максимальная высота крюка, м",
                         "Максимальный вылет с основной стрелой, м",
                         "Виды монтажных работ", "Наименование объекта",
                         "Дата начала работ", "Продолжительность работ, раб.дн",
                         "Дата окончания работ"]
        self.rows = []
        self.total_massive = []
        self.model = TableModel(pd.DataFrame())
        # Датефрейм с календарным планом работ ГПМ на объектах
        self.DataFrame = pd.DataFrame()
        self.DataFrameTotal = pd.DataFrame()
        # флаг на сохранение решения
        self.checkSolved = False

    def ShowSolveWindow(self):
        Dialog = QtWidgets.QDialog()
        self.setupUi(Dialog)
        # настройка календаря
        self.calendarWidget.setMinimumDate(QDate(2022, 1, 1))
        self.calendarWidget.setMaximumDate(QDate(2022, 6, 30))
        # настройка шрифта lebel
        self.label.setFont(QFont("Times", 12))
        # подключение кнопок
        self.pushGetData.clicked.connect(self.GetData)
        self.pushSolveTask.clicked.connect(self.SolveTask)
        self.pushShowCalSMR.clicked.connect(self.ShowCalPlanSMR)
        self.pushActDoc.clicked.connect(self.ActionScreen)
        if self.checkSolved:
            self.calendarWidget.setSelectedDate(QDate(self.date_field.year,
                                                      self.date_field.month, self.date_field.day))
            self.pushShowCalSMR.setEnabled(True)
            self.pushActDoc.setEnabled(True)
        Dialog.exec_()

    def GetData(self):
        self.clear_lists()
        self.date_field = self.calendarWidget.selectedDate().toPyDate()
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""SELECT Distinct a."work_name", a."building_ID", a."unit", e."gesn_id",
                            a."volume_of_works", a."name_of_GPM", e."amount_of_gpm",
                            case
                                when a."unit" = 'м3' THEN  e."amount_of_gpm" * a."volume_of_works"
                                else Round(CAST(e."amount_of_gpm" * a."volume_of_works" as Numeric) / 100, 1)
                            End "Labor_per_volume", a."building_name"
                            FROM "am_works_per_building_GPM" a, "exploition of GPM" e
                            where e."work_name_GPM" = a."work_name"
                            order by a."building_name", a."building_ID" ASC""")
                self.data_from_db_l_costs = cursor.fetchall()
                massive, massive_2 = [], []
                for i, item in enumerate(self.data_from_db_l_costs):
                    for j, jtem in enumerate(item):
                        if j != 1:
                            massive.append(jtem)
                    massive_2.append(massive)
                    massive = []
                self.data_from_db_l_costs = massive_2
                cursor.execute("""SELECT Distinct d."name_of_gpm", d."max_load_capacity",
                 d."max_height_of_hook", d."max_crane_arm_dep" 
                 from directory_nomenclature_gpm d, reg_pres_cond_mach_mech r, list_avai_gpm_in_comp l
                 where l."renter" = 'Не требуется' and r."gpm_availability" = 'есть'
                 and r."gpm_condition" = 'Не требует ремонта'""")
                self.data_machines_mechanisms = cursor.fetchall()
                if self.date_field.year.__str__() == "2023":
                    cursor.execute("""Select working_days_in_2023"
                                                  "from production_calendar where working_days_in_2023 >= %s""",
                                   (self.date_field,))
                    for row in cursor:
                        for item in row:
                            self.data_from_production_calendar.append(item)
                else:
                    cursor.execute("""Select working_days_in_2022, working_days_in_2023"
                                                  "from production_calendar where working_days_in_2022 >= %s
                                                  and working_days_in_2023 >= %s""",
                                   (self.date_field, self.date_field))
                    for row in cursor:
                        for item in row:
                            self.data_from_production_calendar.append(item)
                self.data_from_production_calendar.sort()
                self.pushSolveTask.setEnabled(True)
        msgBoxError = QMessageBox()
        msgBoxError.setWindowTitle(tr("Data status"))
        msgBoxError.setText(tr("The data was successfully received from the database!"))
        msgBoxError.exec_()

    def clear_lists(self):
        self.data_from_db_l_costs.clear()
        self.data_from_production_calendar.clear()
        self.labor_days.clear()
        self.total_massive.clear()
        self.columns = ["Продолжительность, в дн.",
                        "Затраты ГПМ, в маш.ч",
                        "Продолжительность, в дн."]

    def SolveTask(self):
        massive_help, massive_help2 = [], []
        summa = 0
        duration = []
        prev_crane = self.data_from_db_l_costs[0][4]
        f_obj = self.data_from_db_l_costs[0][7]
        for i, item in enumerate(self.data_from_db_l_costs):
            for j, j_item in enumerate(item):
                if j == 0:
                    massive_help2.append(item[4])
                    massive_help2.append(item[0])
                    massive_help2.append(item[7])
                    massive_help2.append(self.date_field.strftime("%Y-%m-%d"))
                    massive_help2.append(round(item[6] / 8))
                    massive_help2.append(datetime.datetime.strptime(self.date_field.strftime("%Y-%m-%d"),
                                                                    "%Y-%m-%d").date() +
                                         datetime.timedelta(days=round(item[6] / 8)))
                    self.total_massive.append(massive_help2)
                    massive_help2 = []
                if j == 7:
                    if prev_crane == item[4]:
                        summa += item[6]
                        if i == len(self.data_from_db_l_costs) - 1:
                            duration.append(round(summa / 8))
                            massive_help.append(item[7])
                            massive_help.append(summa)
                            massive_help.append(round(summa / 8))
                            for k in range(round(summa / 8)):
                                massive_help.append("_" * 8)
                            self.labor_days.append(massive_help)
                    else:
                        duration.append(round(summa / 8))
                        prev_crane = item[4]
                        massive_help.append(f_obj)
                        massive_help.append(summa)
                        massive_help.append(round(summa / 8))
                        for k in range(round(summa / 8)):
                            massive_help.append("_" * 8)
                        self.labor_days.append(massive_help)
                        massive_help = []
                        summa = item[6]
                        f_obj = item[7]
        max_duration = max(duration)
        for t, total in enumerate(self.total_massive):
            for tt, to in enumerate(total):
                if tt == 0:
                    for machines in self.data_machines_mechanisms:
                        if to == machines[0]:
                            total.insert(1, machines[1])
                            total.insert(2, machines[2])
                            total.insert(3, machines[3])
        self.DataFrameTotal = pd.DataFrame(self.total_massive,
                                           index=[idx + 1 for idx in range(len(self.total_massive))],
                                           columns=self.columns2)
        self.rows = self.labor_days
        for idx, dat in enumerate(self.data_from_production_calendar):
            if max_duration == idx:
                break
            if self.date_field.strftime("%Y-%m-%d") <= dat.strftime("%Y-%m-%d"):
                self.columns.append(dat.strftime("%d-%m-%Y"))
        self.DataFrame = pd.DataFrame(self.rows,
                                      columns=[col for col in self.columns],
                                      index=[i + 1 for i in range(len(self.rows))])
        self.model = TableModel(self.DataFrame)
        for k in range(len(self.rows)):
            MainWindow.tableView.setSpan(k, 0, 1, 1)
            MainWindow.tableView.setSpan(k, 1, 1, 1)
            MainWindow.tableView.setSpan(k, 2, 1, 1)
            MainWindow.tableView.setSpan(k, 4, 1, 1)
        MainWindow.tableView.setModel(TableModel(self.DataFrameTotal))
        self.pushShowCalSMR.setEnabled(True)
        self.pushSolveTask.setEnabled(False)
        self.pushActDoc.setEnabled(True)
        self.checkSolved = True

    def ShowCalPlanSMR(self):
        Dialog = QtWidgets.QDialog()
        DialogCalPlanSMR = DialogCalendarPlanSMR()
        DialogCalPlanSMR.setupUi(Dialog)
        DialogCalPlanSMR.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        Dialog.resize(1550, 355)
        DialogCalPlanSMR.tableView.setModel(self.model)
        Dialog.exec_()

    def ConstructDataFrame(self):
        columns = []
        for col in range(len(self.columns2)):
            columns.append(col)
        Data = pd.DataFrame([], index=[], columns=columns)
        Data.at[1, 0] = "Согласовываю"
        Data.at[2, 0] = "Подрядчик:"
        Data.at[3, 0] = "____________(__________)"
        Data.at[1, len(self.columns2) - 1] = "Утверждаю"
        Data.at[2, len(self.columns2) - 1] = "Заказчик:"
        Data.at[3, len(self.columns2) - 1] = "____________(__________)"
        self.DataFrameTotal.loc[len(self.total_massive) + 1] = ""
        self.DataFrameTotal.at[len(self.total_massive) + 2,
                               self.columns2[len(self.columns2) - 1]] = "Составил Начальник ПТО"
        self.DataFrameTotal.at[len(self.total_massive) + 3,
                               self.columns2[len(self.columns2) - 1]] = "____________(__________)"
        self.DataFrameTotal.at[len(self.total_massive) + 4,
                               self.columns2[len(self.columns2) - 1]] = "«___» __________ _________г"
        return Data

    def ActionScreen(self):
        pr = DialogActions(self.DataFrameTotal, self.ConstructDataFrame(), "График работ ГПМ")
        pr.cursor.movePosition(QTextCursor.Start)
        pr.cursor.insertText("Согласовываю" + " " * 226 + "Утверждаю" + "\n")
        pr.cursor.insertText("Подрядчик:" + " " * 230 + "Заказчик:" + "\n")
        pr.cursor.insertText("____________(__________)" + " " * 208 + "____________(__________)" + "\n")
        pr.cursor.insertBlock()
        table = pr.cursor.insertTable(len(self.total_massive) + 1, len(self.columns2) + 1)
        for i, item in enumerate(self.columns2):
            headerCell = table.cellAt(0, i)
            headerCellCursor = headerCell.firstCursorPosition()
            headerCellCursor.insertText(item)
        for j, r in enumerate(self.total_massive):
            for k, rok in enumerate(r):
                cell = table.cellAt(j + 1, k)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(str(rok))
        massive_trapdoor = ["Составил Начальник ПТО",
                            "____________(__________)",
                            "«___»___________________г"]
        pr.cursor.movePosition(QTextCursor.End)
        pr.cursor.insertBlock()
        for i, item in enumerate(massive_trapdoor, start=1):
            if i != 0:
                pr.cursor.insertText("\n")
            pr.cursor.insertText(" " * 248 + item)
        pr.exec_()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.Dialog_Size = Dialog_Size()
        self.Dialog_About = Dialog_About()
        self.DialogSolveTask1 = DialogSolveTask1()
        self.DialogSolveTask2 = DialogSolveTask2()
        self.DialogSolveTask3 = DialogSolveTask3()
        self.DialogSolveTask4 = DialogSelectWeekTask4()
        self.Dialog_Admin = DialogAdministration()
        self.Dialog_Change_Window_theme = Dialog_Change_Window_theme()
        self.action_4.setCheckable(True)
        self.action_5.setCheckable(True)
        self.action_5.setChecked(True)
        self.Task4.setEnabled(False)
        self.Task5.setEnabled(False)
        self.resize(720, 576)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #  Переводчик
        self.trans = QTranslator(self)
        # QLineEdit - поля пользователя (его логин)
        self.current_user = QLineEdit()
        self.current_user.setReadOnly(True)
        # Название перед именем пользователя: Пользователь/User
        self.label_user = ""
        if self.action_5.isChecked():
            self.trigger_english()
        else:
            self.trigger_russian()
        # statusbar, где будет пользователь
        self.statusbar.addWidget(self.current_user)
        # Подключение к функции слота
        self.action_4.triggered.connect(self.trigger_russian)
        self.action_5.triggered.connect(self.trigger_english)
        self.SettingsWindowColor.triggered.connect(self.Dialog_Change_Window_theme.ChangeWindowColor)
        self.SettingsSWindowSize.triggered.connect(self.ChangeSize)
        self.About.triggered.connect(self.Dialog_About.About)
        self.Task1.triggered.connect(self.DialogSolveTask1.showSolveWindow)
        self.Task2.triggered.connect(self.DialogSolveTask2.ShowSolveWindow)
        self.Task4.triggered.connect(self.DialogSolveTask3.solveTask)
        self.Task5.triggered.connect(self.DialogSolveTask4.solveTask)
        self.action_Administration.triggered.connect(self.Dialog_Admin.showAdministration)

    def activated(self):

        if self.Dialog_Size.comboBox.currentText() == "640 x 480":
            self.resize(640, 480)

        elif self.Dialog_Size.comboBox.currentText() == "720 x 576":
            self.resize(720, 576)

        elif self.Dialog_Size.comboBox.currentText() == "1280 x 720":
            self.resize(1280, 720)

        elif self.Dialog_Size.comboBox.currentText() == "1920 x 1080":
            self.resize(1920, 1080)

    def ChangeSize(self):
        self.Dialog_Size.comboBox.activated.connect(self.activated)
        self.Dialog_Size.show()

    @staticmethod
    def getLabel():
        return tr("User: ")

    def createCurrentUser(self):
        self.label_user = self.getLabel()
        if self.current_user.text().split(':')[0] + ": " == self.label_user:
            self.current_user.setText(self.label_user +
                                      self.current_user.text().split(':')[1].strip())
        else:
            self.current_user.setText(self.current_user.text().replace(self.current_user.text().split(':')[0]
                                                                       + ": ", self.label_user))

    def trigger_russian(self):
        if not self.action_5.setChecked(False):
            self.action_5.setChecked(False)
        self.action_4.setChecked(True)
        self.trans.load('main.en.qm')
        _app = QApplication.instance()  # получить экземпляр приложения
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.createCurrentUser()
        self.Dialog_Size.retranslateUi(self.Dialog_Size)
        self.Dialog_About.retranslateUi(self.Dialog_About)
        self.Dialog_Change_Window_theme.retranslateUi(self.Dialog_Change_Window_theme)

    def trigger_english(self):
        if not self.action_4.setChecked(False):
            self.action_4.setChecked(False)
        self.action_5.setChecked(True)
        self.trans.load('main.ru.qm')
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.createCurrentUser()
        self.Dialog_Size.retranslateUi(self.Dialog_Size)
        self.Dialog_About.retranslateUi(self.Dialog_About)
        self.Dialog_Change_Window_theme.retranslateUi(self.Dialog_Change_Window_theme)


class DialogSolveTask1(QDialog, Ui_DialogSolveTask1):
    def __init__(self, parent=None):
        super(DialogSolveTask1, self).__init__(parent)
        self.setupUi(self)
        # Данные из БД
        # даннные по рабочим (из справочника рабочих)
        self.rec_data_workers_info = []
        # данные из ведомости объёмов работ
        self.rec_data_list_of_vol_works = []
        # даты из производственного на 22 - 23 годы
        self.date_from_prod_calendar = []
        # данные по объектам из БД
        self.records_buildings = []
        # поля данных формы
        self.date_field = datetime.date
        self.Amount_of_objects_field = ''
        self.SumTimeConsume_field = ''
        # Для решения задачи:
        # Общий объём CМР на электромонтажные работы в тыс. руб.
        self.total_smr = 0
        # будущая модель в TableView
        self.model = ''
        # строки TableView
        self.rows = []
        # столбцы TableView
        self.columns = []
        # этажность дома полная (этажи + подъезды)
        self.house_properties = []
        # списки для хранения трудозатрат и объёмов СМР в тыс.руб на объект
        self.time_of_work, self.Cost_of_volume_CMR = [], []
        # количество рабочих из справочников бригад
        self.workers_distribution = []
        # таблица рабочих и времени работы на пяти объектах.
        # (Время выполнения электромонтажных работ в ч.)
        self.time_of_electric_works = np.array([])
        # таблица рабочих и объёмов СМР, распределенных по пяти объектам.
        # (Выработка в тыс.руб./бригаду при различном кол-ве рабочих)
        self.table_of_volume_CMR_with_brigades = np.array([])
        # Ведомость объёмов работ на объект => Ведомость объёмов работ на объект итог
        self.table_of_volume_CMR = []
        # Трудозатраты СМР в чел.ч => Трудозатраты СМР итог
        self.time_of_work_dict_total = []
        # общий объём СМР на электромонтажные работы в тыс.руб.
        self.value_problem = 0
        # ДатаФрейм для вывода на экран и загрузки документа в excel
        self.DataFrame = pd.DataFrame()
        self.DataFrameNextDoc = pd.DataFrame()
        # флаг на сохранение решения
        self.checkSolved = False

    def setDataFromForm(self):
        # Выбранная дата из календаря
        self.date_field = self.calendarWidget.selectedDate().toPyDate()
        # Выбранное количество объектов в микрорайоне
        self.Amount_of_objects_field = self.spinBoxAmObj.text()
        # Суммарная продолжительность выполнения работ на всех объектах
        self.SumTimeConsume_field = int(self.spinBoxSumTimeCons.text())

    def showSolveWindow(self):
        Dialog = QtWidgets.QDialog()
        self.setupUi(Dialog)
        # корректирую шрифт текста в labelах для отображения
        self.label.setFont(QFont("Times", 12))
        self.label_2.setFont(QFont("Time", 12))
        self.label_3.setFont(QFont("Times", 12))
        # настройка календаря
        self.calendarWidget.setMinimumDate(QDate(2022, 1, 1))
        self.calendarWidget.setMaximumDate(QDate(2023, 12, 31))
        # настройка спинбоксов
        self.spinBoxAmObj.setRange(5, 10)
        self.spinBoxSumTimeCons.setRange(100, 1000)
        # временно блокирую кнопки
        if self.checkSolved:
            self.calendarWidget.setSelectedDate(QDate(self.date_field.year, self.date_field.month, self.date_field.day))
            self.spinBoxAmObj.setValue(int(self.Amount_of_objects_field))
            self.spinBoxSumTimeCons.setValue(int(self.SumTimeConsume_field))
            self.pushPrint.setDisabled(False)
            self.pushShowMatrixDistr.setDisabled(False)
            self.pushButtonSolveTask.setDisabled(False)
        else:
            self.pushPrint.setDisabled(True)
            self.pushShowMatrixDistr.setDisabled(True)
            self.pushButtonSolveTask.setDisabled(True)
        # кнопки для решения задачи
        self.pushButtonGetData.clicked.connect(self.getDataFromDB)
        self.pushButtonSolveTask.clicked.connect(self.solveTask)
        self.pushShowMatrixDistr.clicked.connect(self.show_matrix)
        self.pushPrint.clicked.connect(self.ActionScreen)
        # запускаю диалоговое окно на отображение
        Dialog.exec_()

    def getDataFromDB(self):
        # сначала записываем данные из формы
        # кол-во объектов + суммарное вр. работы + дата начала работ
        self.date_from_prod_calendar.clear()
        self.setDataFromForm()
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select * from dir_prof_workers_brig '
                               'where Position = \'Электромонтажники\''
                               'Order by brigade_id')
                self.rec_data_workers_info = cursor.fetchall()
                cursor.execute('Select work_name, "Scope_of_SMR_in_thousand_rub_per_floor",'
                               'duration_of_work from list_of_volume_of_works')
                self.rec_data_list_of_vol_works = cursor.fetchall()
                if self.date_field.year.__str__() == "2023":
                    cursor.execute("""Select working_days_in_2023"
                                   "from production_calendar where working_days_in_2023 >= %s""",
                                   (self.date_field,))
                    for row in cursor:
                        for item in row:
                            self.date_from_prod_calendar.append(item)
                else:
                    cursor.execute("""Select working_days_in_2022, working_days_in_2023"
                                   "from production_calendar where working_days_in_2022 >= %s
                                   and working_days_in_2023 >= %s""",
                                   (self.date_field, self.date_field))
                    for row in cursor:
                        for item in row:
                            self.date_from_prod_calendar.append(item)
                cursor.execute("""Select * from reg_buildings_in_district 
                               where "Floors" is not NULL and 
                               "Entrances" is not NULL and
                               "Total_number_of_floors" is not NULL
                               Order by "Number_of_building" ASC
                               Limit %s""",
                               (self.Amount_of_objects_field,))
                self.records_buildings = cursor.fetchall()
        msgBoxError = QMessageBox()
        msgBoxError.setWindowTitle(tr("Data status"))
        msgBoxError.setText(tr("The data was successfully received from the database!"))
        msgBoxError.exec_()
        self.pushButtonSolveTask.setDisabled(False)

    def math_algorithm(self):
        # определяем максимальный объём ресурсов
        C = max(self.workers_distribution)
        # Неизвестные
        variables = np.array([
            [pulp.LpVariable("v" + str(it + 1) + str(obj + 1), lowBound=0, cat='Binary')
             for obj in range(len(self.records_buildings))]
            for it in range(len(self.workers_distribution))])
        # формулировка задачи(цели) и ее максимизация
        problem = pulp.LpProblem('Volume_CMR_maximization', LpMaximize)
        # математическая запись целевой функции
        problem += np.sum(variables * self.table_of_volume_CMR_with_brigades), 'Aim_Function'
        # Constraints(ограничения) по ресурсам
        sum_composition = 0
        for w in range(len(self.workers_distribution)):
            sum_composition += np.multiply(np.sum(variables[w], axis=0), self.workers_distribution[w])
        problem += sum_composition == C
        # Constraints(ограничения) по работникам, на каждом объекте только 1 бригада
        for b in range(len(self.records_buildings)):
            problem += np.sum(variables[:, b]) <= 1
        # Constraints(ограничения) по времени работы на объектах
        for build in range(len(self.records_buildings)):
            problem += (np.sum(variables[:, build] *
                               self.time_of_electric_works[:, build])) <= self.SumTimeConsume_field
        # поиск решения
        problem.solve()
        # хранится распределение рабочих
        matrix_distribution, matrix_help = [], []
        # Выводим результат в консоль
        print("Результат: ")
        c, i = 0, 0
        for variable in problem.variables():
            if c == 0:
                print(f'\t', f'Распределение по {self.workers_distribution[i]} чел.:', end='| ')
            print(variable.varValue, end=' ')
            matrix_help.append(variable.varValue)
            if c == len(self.workers_distribution):
                matrix_distribution.append(matrix_help)
                print('|\n', end=' ')
                i += 1
                c = 0
                matrix_help = []
            else:
                c += 1
        print(f"Общий объём CМР на электромонтажные работы: {value(problem.objective)} тыс.руб.")
        self.total_smr = value(problem.objective)
        self.model = TableModel(pd.DataFrame(matrix_distribution,
                                             columns=["объект" + str(idx + 1)
                                                      for idx in range(len(self.records_buildings))],
                                             index=[f"Распределение по {item} чел.:"
                                                    for item in self.workers_distribution]))
        self.checkSolved = True
        self.pushPrint.setDisabled(False)
        self.pushShowMatrixDistr.setDisabled(False)
        self.show_calendar_plan(matrix_distribution)

    def insertToDBCalendarPlan(self, days):
        result, massive_help, days_final = [], [], []
        for i, r in enumerate(self.rows):
            for k, rok in enumerate(r):
                if k == 0 or k == 3 or k == 4:
                    massive_help.append(rok)
            result.append(massive_help)
            massive_help = []
        for b, brig in enumerate(self.rec_data_workers_info):
            for br, brigate in enumerate(brig):
                for j, res in enumerate(result):
                    for jo, resu in enumerate(res):
                        if resu == brigate:
                            res.insert(1, brig[0])
                            res.pop(2)
        for j, d in enumerate(days):
            for k, res in enumerate(result):
                for idx, r in enumerate(res):
                    if j == 0 and idx == 2:
                        massive_help.append(d + "-" + days[r - 1])
                        massive_help.append(d)
                        massive_help.append(days[r - 1])
                        days_final.append(massive_help)
                        massive_help = []
        for j, jtem in zip(result, self.rows):
            j.append(jtem[1])
            j.append(jtem[2])
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Delete from calendar_plan_el_works""")
                conn.commit()
                for r in range(len(result)):
                    cursor.execute("""INSERT INTO calendar_plan_el_works
                        ("st_end_date_el_works", "pr_calendar",
                        "building_name", "brigade_id", "st_date_electr_iworks",
                        "end_date_electr_iworks","duration_of_works_in_days",
                        "Cost_of_SMR", "Labor_per_obj")
                        Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                   (days_final[r][0], r + 1, result[r][0],
                                    result[r][1], days_final[r][1],
                                    days_final[r][2], result[r][2],
                                    int(result[r][3]), int(result[r][4])))
                    conn.commit()

    def show_matrix(self):
        Dialog = QtWidgets.QDialog()
        Dialog_matrix = DialogMatrix()
        Dialog_matrix.setupUi(Dialog)
        Dialog_matrix.tableView.setModel(self.model)
        Dialog_matrix.line_Total_SMR.setText(f"Общая стоимость СМР за электромонтажные работы:"
                                             f" {self.total_smr} тыс. рублей")
        # запускаю диалоговое окно на отображение
        Dialog.exec_()

    def clearData(self):
        self.workers_distribution.clear()
        self.house_properties.clear()
        self.Cost_of_volume_CMR.clear()
        self.time_of_work.clear()
        self.time_of_electric_works = np.array([])
        self.table_of_volume_CMR_with_brigades = np.array([])
        self.rows.clear()
        self.columns.clear()

    def solveTask(self):
        self.clearData()
        for val in self.records_buildings:
            for jx, val2 in enumerate(val):
                if jx == 2:
                    self.house_properties.append(val2)
        for item in self.rec_data_list_of_vol_works:
            for j, val in enumerate(item):
                if j == 1:
                    self.Cost_of_volume_CMR.append(val)
                elif j == 2:
                    self.time_of_work.append(val)
        # Трудозатраты СМР в чел.ч => Трудозатраты СМР итог
        self.time_of_work_dict_total = np.sum([[i * j for i in self.time_of_work]
                                               for j in self.house_properties], axis=1)
        # Ведомость объёмов работ на объект => Ведомость объёмов работ на объект итог
        self.table_of_volume_CMR = np.sum([[float("{0:.1f}".format(i * j)) for i in self.Cost_of_volume_CMR]
                                           for j in self.house_properties], axis=1)
        # определяем максимальный объём ресурсов
        for worker in self.rec_data_workers_info:
            for wx, v in enumerate(worker):
                if wx == 1:
                    self.workers_distribution.append(v)

        self.time_of_electric_works = np.array([
            [round(self.time_of_work_dict_total[build_idx] / self.workers_distribution[wor_idx] / 1.03)
             if wor_idx == 0
             else
             round(self.time_of_work_dict_total[build_idx] / self.workers_distribution[wor_idx] * 1.04)
             if wor_idx == 1
             else
             round(self.time_of_work_dict_total[build_idx] / self.workers_distribution[wor_idx] * 1.05)
             if len(self.workers_distribution) != wor_idx + 1
             else
             round(self.time_of_work_dict_total[build_idx] / self.workers_distribution[wor_idx])
             for build_idx in range(len(self.records_buildings))]
            for wor_idx in range(len(self.workers_distribution))])

        self.table_of_volume_CMR_with_brigades = np.array([
            [round(self.table_of_volume_CMR[building_idx] /
                   self.workers_distribution[len(self.workers_distribution) - 1] *
                   self.workers_distribution[work_idx] * 1.03)
             if work_idx == 0
             else
             round(self.table_of_volume_CMR[building_idx] / self.workers_distribution[
                 len(self.workers_distribution) - 1] * self.workers_distribution[work_idx] * 1.04)
             if work_idx == 1
             else
             round(self.table_of_volume_CMR[building_idx] / self.workers_distribution[
                 len(self.workers_distribution) - 1] * self.workers_distribution[work_idx] * 1.05)
             if len(self.workers_distribution) != work_idx + 1
             else
             round(self.table_of_volume_CMR[building_idx])
             for building_idx in range(len(self.records_buildings))]
            for work_idx in range(len(self.workers_distribution))])

        self.math_algorithm()
        self.pushButtonSolveTask.setDisabled(True)
        # self.pushShowMatrixDistr.setDisabled(True)
        # self.pushPrint.setDisabled(True)

    def show_calendar_plan(self, matrix):
        # 1 эл - номер бригады, 2 эл - объект, 3 - Трудозатраты СМР рабочих (итог)
        # 4 эл - выработка бригады, 5 -затраты труда на объект 6 - количестов дней работы
        # 7 эл - название объекта
        data_for_cal_plan = []
        for idx, val in enumerate(matrix):
            for jdx, val2 in enumerate(val):
                if val2 == 1.0:
                    for kdx, val3 in enumerate(self.table_of_volume_CMR_with_brigades):
                        for ldx, val4 in enumerate(val3):
                            if kdx == idx and ldx == jdx:
                                data_for_cal_plan.append([idx, jdx, val4])
        for i, el in enumerate(data_for_cal_plan):
            for j, el1 in enumerate(el):
                if j == 0:
                    for b, brig in enumerate(self.workers_distribution):
                        if b == el1:
                            el.pop(j)
                            el.insert(j, brig)
                elif j == 1:
                    for bu, building in enumerate(self.table_of_volume_CMR):
                        if bu == el1:
                            el.insert(j, building)
                elif j == 2:
                    for t, tim in enumerate(self.time_of_work_dict_total):
                        if t == el1:
                            el.insert(j, tim)
                elif j == 3:
                    for i1, name in enumerate(self.records_buildings):
                        if el1 + 1 == name[4]:
                            el.pop(j)
                            el.insert(j, name[3])
                else:
                    continue
        for item in data_for_cal_plan:
            item.append(round(item[4] * item[2] / item[1]))
            item.append(round(item[5] / item[0] / 8))
        self.rows, massive_help_model = [], []
        massive_days = 0
        mass_days = []
        for idx, element in enumerate(data_for_cal_plan):
            for el, val in enumerate(element):
                if el == 3:
                    massive_help_model.append(val)
                elif el == 4:
                    massive_help_model.append(val)
                elif el == 5:
                    massive_help_model.append(val)
                elif el == 6:
                    massive_help_model.append(element[0])
                    massive_help_model.append(val)
                    mass_days.append(val)
                    massive_days = val
                    for i in range(val):
                        massive_help_model.append("_" * 7)
            self.rows.append(massive_help_model)
            massive_help_model = []
        self.columns = ["Наименование объекта",
                        "Ст-ть СМР в тыс. руб",
                        "Затраты труда в чел.ч",
                        "Численность бригады, чел.",
                        "Продолжительность в дн."]
        self.date_from_prod_calendar.sort()
        massiveDays = []
        for idx, dat in enumerate(self.date_from_prod_calendar):
            if massive_days == idx:
                break
            if self.date_field.strftime("%Y-%m-%d") <= dat.strftime("%Y-%m-%d"):
                self.columns.append(dat.strftime("%d-%m-%Y"))
                massiveDays.append(dat.strftime("%Y-%m-%d"))
        self.DataFrame = pd.DataFrame(self.rows,
                                      columns=[col for col in self.columns],
                                      index=[i + 1 for i in range(len(self.rows))])
        model = TableModel(self.DataFrame)
        for k in range(len(self.rows)):
            MainWindow.tableView.setSpan(k, 0, 1, 1)
            MainWindow.tableView.setSpan(k, 1, 1, 1)
            MainWindow.tableView.setSpan(k, 2, 1, 1)
            MainWindow.tableView.setSpan(k, 4, 1, 1)
        MainWindow.tableView.setModel(model)
        MainWindow.Task4.setEnabled(True)
        self.insertToDBCalendarPlan(massiveDays)

    def ConstructDataFrame(self):
        columns = []
        for col in range(len(self.columns)):
            columns.append(col)
        Data = pd.DataFrame([], index=[], columns=columns)
        Data.at[1, 0] = "Согласовываю"
        Data.at[2, 0] = "Подрядчик:"
        Data.at[3, 0] = "____________(__________)"
        Data.at[1, len(self.columns) - 1] = "Утверждаю"
        Data.at[2, len(self.columns) - 1] = "Заказчик:"
        Data.at[3, len(self.columns) - 1] = "____________(__________)"
        self.DataFrame.loc[len(self.rows) + 1] = ""
        self.DataFrame.at[len(self.rows) + 2, self.columns[len(self.columns) - 1]] = "Составил Начальник ПТО"
        self.DataFrame.at[len(self.rows) + 3, self.columns[len(self.columns) - 1]] = "____________(__________)"
        self.DataFrame.at[len(self.rows) + 4, self.columns[len(self.columns) - 1]] = "«___» __________ _________г"
        return Data

    def ActionScreen(self):
        pr = DialogActions(self.DataFrame, self.ConstructDataFrame(), "Кал. график эл. монтаж. работ")
        pr.cursor.movePosition(QTextCursor.Start)
        pr.cursor.insertText("Согласовываю" + " " * 226 + "Утверждаю" + "\n")
        pr.cursor.insertText("Подрядчик:" + " " * 230 + "Заказчик:" + "\n")
        pr.cursor.insertText("____________(__________)" + " " * 208 + "____________(__________)" + "\n")
        pr.cursor.insertBlock()
        table = pr.cursor.insertTable(len(self.rows) + 1, len(self.columns) + 1)
        for i, item in enumerate(self.columns):
            headerCell = table.cellAt(0, i)
            headerCellCursor = headerCell.firstCursorPosition()
            headerCellCursor.insertText(item)
        for j, r in enumerate(self.rows):
            for k, rok in enumerate(r):
                cell = table.cellAt(j + 1, k)
                cellCursor = cell.firstCursorPosition()
                cellCursor.insertText(str(rok))
        massive_trapdoor = ["Составил Начальник ПТО",
                            "____________(__________)",
                            "«___»___________________г"]
        pr.cursor.movePosition(QTextCursor.End)
        pr.cursor.insertBlock()
        for i, item in enumerate(massive_trapdoor, start=1):
            if i != 0:
                pr.cursor.insertText("\n")
            pr.cursor.insertText(" " * 248 + item)
        pr.exec_()


class DialogAddToDirectoryOfWorks(QDialog, Ui_AddToDirectoryOfWorksTable):
    def __init__(self, parent=None):
        super(DialogAddToDirectoryOfWorks, self).__init__(parent)
        self.setupUi(self)
        self.WorkName = ""
        self.Unit = ""
        self.Gesn = ""
        self.pushAddData.clicked.connect(self.ADDData)

    def ADDData(self):
        self.WorkName = self.lineWorkName.text()
        self.Unit = self.line_Unit.text()
        self.Gesn = self.lineGESN_ID.text()
        if self.WorkName != '' and self.Gesn != '' and self.Unit != '':
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Insert Into directory_of_works ("work_name", "gesn_id",
                                    "unit") Values(%s,%s,%s)""", (self.WorkName, self.Gesn, self.Unit))
                conn.commit()
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
            msgBoxFileLoaded.setText(tr("The data has been successfully inserted into the table directory_of_works!"))
            msgBoxFileLoaded.exec_()
        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Data entry error!"))
            msgBoxFileLoaded.setText(tr("There is no data to insert into the table directory_of_works!\n"
                                        "Please repeat adding the data again!"))
            msgBoxFileLoaded.exec_()
        self.close()


class DialogAddToRegBuildingsinDistrict(QDialog, Ui_AddToRegBuildingsInDistrictTable):
    def __init__(self, parent=None):
        super(DialogAddToRegBuildingsinDistrict, self).__init__(parent)
        self.setupUi(self)
        self.pushAddData.clicked.connect(self.ADDData)

    def ADDData(self):
        Buildings_name_reg = self.lineBuildings_name_reg.text()
        Floors = self.spinFloors.value()
        Entrances = self.spinBox_Entrances.value()
        Total_number_of_floors = Floors * Entrances
        N_Building = self.spinBox_NumberOfBuilding.value()
        if Buildings_name_reg != '' and Floors > 0 and Entrances > 0:
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Insert Into reg_buildings_in_district ("Floors",
                                              "Entrances", "Total_number_of_floors", "Building_name_reg",
                                              "Number_of_building") Values(%s,%s,%s,%s,%s)""",
                                   (Floors, Entrances,
                                    Total_number_of_floors, Buildings_name_reg, N_Building))
                    conn.commit()
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
            msgBoxFileLoaded.setText(tr("The data has been successfully inserted into"
                                        " the table reg_buildings_in_district!"))
            msgBoxFileLoaded.exec_()
        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Data entry error!"))
            msgBoxFileLoaded.setText(tr("There is no data to insert into the table reg_buildings_in_district!\n"
                                        "Please repeat adding the data again!"))
            msgBoxFileLoaded.exec_()
        self.close()


class DialogAddToStateElementEstimates(QDialog, Ui_AddToStateElementEstimatesTable):
    def __init__(self, parent=None):
        super(DialogAddToStateElementEstimates, self).__init__(parent)
        self.setupUi(self)
        self.pushAddData.clicked.connect(self.ADDData)

    def ADDData(self):
        if self.lineGesn_id.text() != '' and self.lineEdit_GESN_name.text() != '' \
                and self.lineEdit_GESN_Unit.text() != '':
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Insert Into state_element_estimates ("gesn_id",
                                "gesn_unit", "gesn_name") Values(%s,%s,%s)""",
                                   (self.lineGesn_id.text(), self.lineEdit_GESN_Unit.text(),
                                    self.lineEdit_GESN_name.text()))
                conn.commit()
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
            msgBoxFileLoaded.setText(tr("The data has been successfully inserted into"
                                        " the table state_element_estimates!"))
            msgBoxFileLoaded.exec_()
        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Data entry error!"))
            msgBoxFileLoaded.setText(tr("There is no data to insert into the table state_element_estimates!\n"
                                        "Please repeat adding the data again!"))
            msgBoxFileLoaded.exec_()
        self.close()


class DialogAddToAmWorksPerBuilding_GPM(QDialog, Ui_DialogAddDataToAM_works_per_build_GPM):
    def __init__(self, parent=None):
        super(DialogAddToAmWorksPerBuilding_GPM, self).__init__(parent)
        self.setupUi(self)
        self.resize(1000, 300)
        self.works = []
        self.buildings = []
        self.units = []
        self.name_of_gpm = []
        self.dsBVol_of_works.setRange(0.1, 10000)
        self.SelectWorkNames()
        self.SelectBuildingName()
        self.SelectUnits()
        self.SelectNameOfGPM()
        self.pushButtonADD_Data.clicked.connect(self.AddData)

    def AddData(self):
        building_name = self.cBBuilding_name.currentText()
        work_name = self.cBWork_name.currentText()
        unit = self.cBUnit.currentText()
        name_of_gpm = self.cBName_of_GPM.currentText()
        vol_of_works = self.dsBVol_of_works.value()
        if isinstance(building_name, str) and isinstance(work_name, str) and \
                isinstance(unit, str) and isinstance(name_of_gpm, str) and vol_of_works > 0.0:
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute('Insert Into "am_works_per_building_GPM"'
                                   '("building_name", "work_name", "unit", "name_of_GPM", "volume_of_works")'
                                   'Values(%s, %s, %s, %s, %s)', (building_name, work_name,
                                                                  unit, name_of_gpm, vol_of_works))
                    conn.commit()
                    msgBoxFileLoaded = QMessageBox()
                    msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
                    msgBoxFileLoaded.setText(tr("The data has been successfully inserted into"
                                                " the table am_works_per_building_GPM!"))
                    msgBoxFileLoaded.exec_()
        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Error data!"))
            msgBoxFileLoaded.setText(tr("The data was not added to the table am_works_per_building_GPM"
                                        " because the entered data does not match the format!"))
            msgBoxFileLoaded.exec_()
        self.close()

    def SelectWorkNames(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "work_name" from directory_of_works
                               where "gesn_id" <> '08-03-599-11' and "gesn_id" <> '08-03-604-01'
                                and "gesn_id" <> '08-02-401-01' 
                                and "gesn_id" <> '08-03-593-01' and "gesn_id" <> '08-03-591-03' """)
                self.works = cursor.fetchall()
                for note in self.works:
                    for w in note:
                        self.cBWork_name.addItem(w)

    def SelectBuildingName(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "Building_name_reg" from reg_buildings_in_district')
                self.buildings = cursor.fetchall()
                for note in self.buildings:
                    for w in note:
                        self.cBBuilding_name.addItem(w)

    def SelectUnits(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "unit" from directory_of_works')
                self.units = cursor.fetchall()
                for note in self.units:
                    for w in note:
                        self.cBUnit.addItem(w)

    def SelectNameOfGPM(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "name_of_gpm" from directory_nomenclature_gpm')
                self.name_of_gpm = cursor.fetchall()
                for note in self.name_of_gpm:
                    for w in note:
                        self.cBName_of_GPM.addItem(w)


class DialogUpdateDataToAM_works_per_build_GPM(QDialog, Ui_DialogUpdateDataToAM_works_per_build_GPM):
    def __init__(self, build_name_old, work_name_old, unit_old, name_of_gpm_old, vol_works_old, parent=None):
        super(DialogUpdateDataToAM_works_per_build_GPM, self).__init__(parent)
        self.setupUi(self)
        self.resize(1000, 300)
        self.works = []
        self.buildings = []
        self.units = []
        self.name_of_gpm = []
        self.build_name_old = build_name_old
        self.work_name_old = work_name_old
        self.unit_old = unit_old
        self.name_of_gpm_old = name_of_gpm_old
        self.vol_works_old = vol_works_old
        self.SelectWorkNames()
        self.SelectBuildingName()
        self.dsBVol_of_works.setRange(0.1, 10000)
        self.SelectUnits()
        self.SelectNameOfGPM()
        self.pushButtonUpdate_Data.clicked.connect(self.UpdateData)

    def UpdateData(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Update "am_works_per_building_GPM" '
                               'set "building_name" = %s, "work_name" = %s, "unit" = %s, "name_of_GPM" = %s, '
                               '"volume_of_works" = %s where "building_name"  = %s and "work_name" = %s and '
                               '"unit" = %s and"name_of_GPM" = %s and "volume_of_works" = %s',
                               (self.cBBuilding_name.currentText(),
                                self.cBWork_name.currentText(),
                                self.cBUnit.currentText(),
                                self.cBName_of_GPM.currentText(),
                                self.dsBVol_of_works.value(),
                                self.build_name_old.strip('"'),
                                self.work_name_old.strip('"'),
                                self.unit_old.strip('"'),
                                self.name_of_gpm_old.strip('"'),
                                self.vol_works_old))
                conn.commit()
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data update!"))
        msgBoxFileLoaded.setText(tr("The data has been successfully updated in"
                                    " the table list_of_volume_of_works!"))
        msgBoxFileLoaded.exec_()
        self.close()

    def SelectWorkNames(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "work_name" from directory_of_works
                               where "gesn_id" <> '08-03-599-11' and "gesn_id" <> '08-03-604-01'
                                and "gesn_id" <> '08-02-401-01' 
                                and "gesn_id" <> '08-03-593-01' and "gesn_id" <> '08-03-591-03' """)
                self.works = cursor.fetchall()
                for note in self.works:
                    for w in note:
                        self.cBWork_name.addItem(w)

    def SelectBuildingName(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "Building_name_reg" from reg_buildings_in_district')
                self.buildings = cursor.fetchall()
                for note in self.buildings:
                    for w in note:
                        self.cBBuilding_name.addItem(w)

    def SelectUnits(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "unit" from directory_of_works')
                self.units = cursor.fetchall()
                for note in self.units:
                    for w in note:
                        self.cBUnit.addItem(w)

    def SelectNameOfGPM(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "name_of_gpm" from directory_nomenclature_gpm')
                self.name_of_gpm = cursor.fetchall()
                for note in self.name_of_gpm:
                    for w in note:
                        self.cBName_of_GPM.addItem(w)


class DialogUpdateDirOfWorks(QDialog, Ui_DialogUpdateDirOfWorks):
    def __init__(self, data, parent=None):
        super(DialogUpdateDirOfWorks, self).__init__(parent)
        self.setupUi(self)
        self.pushUpdateData.clicked.connect(self.UpdateDataPressed)
        self.work_name_old = data

    def UpdateDataPressed(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select * from list_of_volume_of_works
                where "work_name" = %s""", (self.work_name_old,))
                list_of_vol_data = cursor.fetchall()
                if len(list_of_vol_data) > 0:
                    cursor.execute("""Delete from list_of_volume_of_works
                                    where "work_name" = %s""", (self.work_name_old,))
                    conn.commit()
                cursor.execute('Select "gesn_id"'
                               ' from state_element_estimates '
                               'where "gesn_id" = %s', (self.lineGesn_id.text(),))
                GESN_ID_ST_EST = cursor.fetchall()
                if len(GESN_ID_ST_EST) > 0:
                    cursor.execute('Update directory_of_works '
                                   'set "work_name" = %s, "gesn_id" = %s, unit = %s '
                                   'where "work_name" = %s', (self.lineWork_name.text(),
                                                              self.lineGesn_id.text(),
                                                              self.lineUnit.text(),
                                                              self.work_name_old))
                    conn.commit()
                    msgBoxFileLoaded = QMessageBox()
                    msgBoxFileLoaded.setWindowTitle(tr("Successful data modification!"))
                    msgBoxFileLoaded.setText(tr("The data has been successfully changed"
                                                " in the table directory_of_works!"))
                    msgBoxFileLoaded.exec_()
                else:
                    msgBoxFileLoaded = QMessageBox()
                    msgBoxFileLoaded.setWindowTitle(tr("Data Modification error!"))
                    msgBoxFileLoaded.setText(tr("The chosen data cannot be changed in the table directory_of_works,"
                                                " until an entry is added to state_element_estimates!"))
                    msgBoxFileLoaded.exec_()
                if len(list_of_vol_data) > 0:
                    cursor.execute("""Insert into list_of_volume_of_works
                                        ("work_name", "Scope_of_work_per_floor", 
                                        "Scope_of_SMR_in_thousand_rub_per_floor",
                                        "duration_of_work", "Work_ID") Values(%s, %s, %s, %s, %s)""",
                                   (self.lineWork_name.text(),
                                    list_of_vol_data[0][1],
                                    list_of_vol_data[0][2],
                                    list_of_vol_data[0][3],
                                    list_of_vol_data[0][4] + 1))
                    conn.commit()
        self.close()


class DialogUpdateStateElementEstimates(QDialog, Ui_DialogUpdateState_Element_Estimates):
    def __init__(self, data, parent=None):
        super(DialogUpdateStateElementEstimates, self).__init__(parent)
        self.setupUi(self)
        self.oldGesnId = data
        self.pushUpdateData.clicked.connect(self.UpdateDataPressed)

    def UpdateDataPressed(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Update state_element_estimates '
                               'set "gesn_id" = %s, "gesn_unit" = %s,"gesn_name" = %s '
                               'where "gesn_id" = %s', (self.lineGesn_id.text().strip('"'),
                                                        self.lineUnit.text().strip('"'),
                                                        self.lineGesn_name.text().strip('"'),
                                                        self.oldGesnId))
            conn.commit()
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data modification!"))
        msgBoxFileLoaded.setText(tr("The data has been successfully changed in the table state_element_estimates!"))
        msgBoxFileLoaded.exec_()
        self.close()


class DialogUpdateRegBuildingsInDistrict(QDialog, Ui_DialogUpdateRegBuildingsInDistrict):
    def __init__(self, data1, data2, data3, data4, parent=None):
        super(DialogUpdateRegBuildingsInDistrict, self).__init__(parent)
        self.setupUi(self)
        # Amount of floors
        self.data1 = data1
        # Amount of entrances
        self.data2 = data2
        # old name of Building
        self.data3 = data3
        # Number of Building
        self.data4 = data4
        self.Check = False
        self.spinTotalAmFloors.setReadOnly(True)
        self.spinNumber_of_building.setReadOnly(True)
        self.pushButtonUpdateData.clicked.connect(self.UpdateDataPressed)
        self.spinAmOfFloors.valueChanged.connect(self.spin1Changed)
        self.spinAmOfEntrances.valueChanged.connect(self.spin2Changed)

    def spin1Changed(self):
        self.data1 = self.spinAmOfFloors.value()
        self.spinTotalAmFloors.setValue(self.data1 * self.data2)

    def spin2Changed(self):
        self.data2 = self.spinAmOfEntrances.value()
        self.spinTotalAmFloors.setValue(self.data1 * self.data2)

    def UpdateDataPressed(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select * from calendar_plan_el_works
                                                where "building_name" = %s""",
                               (self.data3,))
                obj = cursor.fetchall()
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select * from report_on_compl_works
                                                where "building_name" = %s""",
                               (self.data3,))
                obj1 = cursor.fetchall()
        Check1 = False
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                if len(obj1) > 0:
                    cursor.execute("""Delete from report_on_compl_works where "building_name" = %s""", (obj1[0][1],))
                    conn.commit()
                    Check1 = True
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                if len(obj) > 0:
                    cursor.execute("""Delete from calendar_plan_el_works where "building_name" = %s""", (obj[0][2],))
                    conn.commit()
                    self.Check = True
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Update reg_buildings_in_district
                               set "Floors" = %s, "Entrances" = %s,"Total_number_of_floors" = %s,
                               "Building_name_reg" = %s, "Number_of_building" = %s
                                where "Number_of_building" = %s""",
                               (str(self.data1), str(self.data2),
                                self.spinTotalAmFloors.text(),
                                self.lineBuilding_name_reg.text().strip('"'),
                                str(self.data4), str(self.data4)))
                conn.commit()

        if self.Check:
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    for i in range(len(obj)):
                        cursor.execute("""INSERT INTO calendar_plan_el_works
                            ("st_end_date_el_works", "pr_calendar",
                            "building_name", "brigade_id", "st_date_electr_iworks",
                            "end_date_electr_iworks","duration_of_works_in_days")
                            Values(%s,%s,%s,%s,%s,%s,%s)""",
                                       (obj[i][0], obj[i][1], self.lineBuilding_name_reg.text().strip('"'),
                                        obj[i][3], obj[i][4], obj[i][5], obj[i][6]))
                    conn.commit()
                    self.Check = False
        if Check1:
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    for k in range(len(obj1)):
                        cursor.execute("""INSERT INTO report_on_compl_works
                            Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                       (obj1[k][0], self.lineBuilding_name_reg.text().strip('"'), obj1[k][2],
                                        obj1[k][3], obj1[k][4], obj1[k][5], obj1[k][6], obj1[k][7], obj1[k][8]))
                    conn.commit()
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data modification!"))
        msgBoxFileLoaded.setText(tr("The data has been successfully changed in the table reg_buildings_in_district!"))
        msgBoxFileLoaded.exec_()
        self.close()


class DialogUpdateListOfVolumeOfWorks(QDialog, Ui_DialogUpdateL_vol_works):
    def __init__(self, old_work, parent=None):
        super(DialogUpdateListOfVolumeOfWorks, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonUpdate.clicked.connect(self.UpdateDataListOfVolWorks)
        self.dBlScope_of_work_per_floor.setRange(0.1, 10000.0)
        self.dBScope_of_SMR_in_thousand_rub_per_floor.setRange(0.1, 10000.0)
        self.dBduration_of_work.setRange(0.1, 10000.0)
        self.old_work = old_work
        self.works = []
        self.SelectWorkNames()

    def SelectWorkNames(self):

        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "work_name" from directory_of_works')
                self.works = cursor.fetchall()
                for note in self.works:
                    for w in note:
                        self.cBWork_name.addItem(w)

    def UpdateDataListOfVolWorks(self):
        work_name = self.cBWork_name.currentText()
        Scope_per_floor = self.dBlScope_of_work_per_floor.value()
        Scope_per_floor_thous_rub = self.dBScope_of_SMR_in_thousand_rub_per_floor.value()
        Duration = self.dBduration_of_work.value()
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Update list_of_volume_of_works
                set "work_name" = %s, "Scope_of_work_per_floor" = %s, 
                "Scope_of_SMR_in_thousand_rub_per_floor" = %s, "duration_of_work" = %s 
                 where "work_name" = (select "work_name"
                 from directory_of_works
                 where "work_name" = %s)""", (work_name.strip("'"),
                                              "{:.1f}".format(Scope_per_floor),
                                              "{:.1f}".format(Scope_per_floor_thous_rub),
                                              "{:.1f}".format(Duration), self.old_work))
                conn.commit()

                cursor.execute("""Select * from list_of_volume_of_works
                where "work_name" = %s""", (work_name,))
                work_info = cursor.fetchall()
                if len(work_info) > 1:
                    cursor.execute("""Delete from list_of_volume_of_works
                                    where "work_name" = %s""", (self.old_work,))
                    conn.commit()
                    cursor.execute("""Delete from list_of_volume_of_works
                                                        where "work_name" = %s""", (work_name,))
                    conn.commit()
                    cursor.execute("""Insert Into list_of_volume_of_works
                                      Values(%s, %s, %s,  %s)""", (work_info[0][0],
                                                                   Scope_per_floor + work_info[0][1],
                                                                   Scope_per_floor_thous_rub + work_info[0][2],
                                                                   Duration + work_info[0][3]))
                    conn.commit()
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("Successful data update!"))
        msgBoxFileLoaded.setText(tr("The data has been successfully updated in"
                                    " the table list_of_volume_of_works!"))
        msgBoxFileLoaded.exec_()
        self.close()


class DialogAddToListOfVolumeOfWorks(QDialog, Ui_DialogADDL_vol_works):
    def __init__(self, parent=None):
        super(DialogAddToListOfVolumeOfWorks, self).__init__(parent)
        self.setupUi(self)
        self.works = []
        self.SelectWorkNames()
        self.dBlScope_of_work_per_floor.setRange(0.1, 10000.0)
        self.dBScope_of_SMR_in_thousand_rub_per_floor.setRange(0.1, 10000.0)
        self.dBduration_of_work.setRange(0.1, 10000.0)
        self.pushButtonAdd.clicked.connect(self.AddDataToListOfVolWorks)

    def SelectWorkNames(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "work_name" from directory_of_works')
                self.works = cursor.fetchall()
                for note in self.works:
                    for w in note:
                        self.cBWork_name.addItem(w)

    def AddDataToListOfVolWorks(self):
        work_name = self.cBWork_name.currentText()
        Scope_per_floor = self.dBlScope_of_work_per_floor.value()
        Scope_per_floor_thous_rub = self.dBScope_of_SMR_in_thousand_rub_per_floor.value()
        Duration = self.dBduration_of_work.value()
        if isinstance(work_name, str) and Scope_per_floor > 0.0 and \
                Scope_per_floor_thous_rub > 0.0 and Duration > 0.0:
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Select "work_name", "Scope_of_work_per_floor",
                    "Scope_of_SMR_in_thousand_rub_per_floor", "duration_of_work" from list_of_volume_of_works
                    where "work_name" = %s """, (work_name.strip("'"),))
                    check = cursor.fetchall()
            if len(check) == 0:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute('Insert INTO list_of_volume_of_works '
                                       'Values(%s, %s, %s, %s)', (work_name.strip("'"),
                                                                  "{:.1f}".format(Scope_per_floor),
                                                                  "{:.1f}".format(Scope_per_floor_thous_rub),
                                                                  "{:.1f}".format(Duration)))
                        conn.commit()
                msgBoxFileLoaded = QMessageBox()
                msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
                msgBoxFileLoaded.setText(tr("The data has been successfully inserted into"
                                            " the table list_of_volume_of_works!"))
                msgBoxFileLoaded.exec_()
            else:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("""Update list_of_volume_of_works
                                       set "Scope_of_work_per_floor" = %s,
                                       "Scope_of_SMR_in_thousand_rub_per_floor" = %s,
                                       "duration_of_work" = %s 
                                       where "work_name" = %s """,
                                       ("{:.1f}".format(Scope_per_floor + check[0][1]),
                                        "{:.1f}".format(Scope_per_floor_thous_rub + check[0][2]),
                                        "{:.1f}".format(Duration + check[0][3]), check[0][0]))
                        conn.commit()
                msgBoxFileLoaded = QMessageBox()
                msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
                msgBoxFileLoaded.setText(tr("The data has been combined with the same work in"
                                            " the table list_of_volume_of_works!"))
                msgBoxFileLoaded.exec_()
        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Error data!"))
            msgBoxFileLoaded.setText(tr("The data was not added to the table list_of_volume_of_works"
                                        " because the entered data does not match the format!"))
            msgBoxFileLoaded.exec_()
        self.close()


class DialogAddToReport_on_compl_works(QDialog, Ui_DialogAddToReport_on_compl_works):
    def __init__(self, parent=None):
        super(DialogAddToReport_on_compl_works, self).__init__(parent)
        self.setupUi(self)
        self.resize(1000, 300)
        self.date_st_date_act_am_work_perf.setDateRange(datetime.date.fromisoformat("2022-01-01"),
                                                        datetime.date.fromisoformat("2023-12-31"))
        self.date_end_date_act_am_work_perf.setDateRange(datetime.date.fromisoformat("2022-01-01"),
                                                         datetime.date.fromisoformat("2023-12-31"))
        self.date_date_of_remain_vol.setDateRange(datetime.date.fromisoformat("2022-01-01"),
                                                  datetime.date.fromisoformat("2023-12-31"))
        self.sBact_am_work_performed.setRange(0, 10000)
        self.sBvolume_per_object.setRange(1, 10000)
        self.sBremaining_volume.setRange(0, 10000)
        self.buildings = []
        self.SelectBuildingName()
        self.pushButtonADDData.clicked.connect(self.AddData)

    def SelectBuildingName(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "Building_name_reg" from reg_buildings_in_district')
                self.buildings = cursor.fetchall()
                for note in self.buildings:
                    for w in note:
                        self.cBbuilding_name.addItem(w)

    def AddData(self):
        work_name_report = self.linework_name_report.text()
        building_name = self.cBbuilding_name.currentText()
        unit = self.lineunit.text()
        vol_per_obj = self.sBvolume_per_object.value()
        act_am_of_work_perf = self.sBact_am_work_performed.value()
        st_date = self.date_st_date_act_am_work_perf.date().toPyDate().strftime("%Y-%m-%d")
        end_date = self.date_end_date_act_am_work_perf.date().toPyDate().strftime("%Y-%m-%d")
        remaining_vol = self.sBremaining_volume.value()
        date_of_remai_vol = self.date_date_of_remain_vol.date().toPyDate().strftime("%Y-%m-%d")
        if work_name_report != "" and unit != "":
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Select "work_name_report", "building_name", "unit",
                "volume_per_object", "act_am_work_performed", "st_date_act_am_work_perf",
                "end_date_act_am_work_perf", "remaining_volume", "date_of_remain_vol"
                 from report_on_compl_works
                  where "work_name_report" = %s and "building_name" = %s and "unit" = %s
                  ORDER BY "Report_ID" ASC """, (work_name_report, building_name, unit))
                    check = cursor.fetchall()
                    if len(check) == 0:
                        cursor.execute("""Insert into "report_on_compl_works"
                         ("work_name_report", "building_name", "unit", "volume_per_object", "act_am_work_performed",
                         "st_date_act_am_work_perf", "end_date_act_am_work_perf", "remaining_volume",
                         "date_of_remain_vol")
                         Values(%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (work_name_report, building_name, unit,
                                                                         vol_per_obj, act_am_of_work_perf, st_date,
                                                                         end_date, remaining_vol, date_of_remai_vol))
                        conn.commit()
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
                        msgBoxFileLoaded.setText(tr("The data has been successfully inserted into"
                                                    " the table report_on_compl_works!"))
                    else:
                        val_act_am_of_work, val_remain_vol = 0, 0
                        if isinstance(check[0][4], int):
                            val_act_am_of_work = check[0][4]
                        if isinstance(check[0][7], int):
                            val_remain_vol = check[0][7]
                        cursor.execute("""Update report_on_compl_works
                                       set "work_name_report" = %s,
                                       "building_name" = %s,
                                       "unit" = %s, "volume_per_object" = %s, "act_am_work_performed" = %s,
                                       "st_date_act_am_work_perf" = %s, "end_date_act_am_work_perf"= %s,
                                        "remaining_volume" = %s, "date_of_remain_vol" = %s
                                       where "work_name_report" = %s and "building_name" = %s and "unit" = %s """,
                                       (work_name_report, building_name, unit,
                                        vol_per_obj + check[0][3], act_am_of_work_perf + val_act_am_of_work,
                                        st_date, end_date, remaining_vol + val_remain_vol, date_of_remai_vol,
                                        check[0][0], check[0][1], check[0][2]))
                        conn.commit()
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Successful data addition!"))
                        msgBoxFileLoaded.setText(tr("The data has been combined with the same work, unit, building in"
                                                    " the table report_on_compl_works!"))
                        msgBoxFileLoaded.exec_()

        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Error data!"))
            msgBoxFileLoaded.setText(tr("The data was not added to the table report_on_compl_works"
                                        " because the entered data does not match the format!"))
            msgBoxFileLoaded.exec_()
        self.close()


class DialogUpdateInReport_on_compl_works(QDialog, Ui_DialogUpdateInReport_on_compl_works):
    def __init__(self, work_name_old, building_name_old, unit_old, parent=None):
        super(DialogUpdateInReport_on_compl_works, self).__init__(parent)
        self.setupUi(self)
        self.resize(1000, 300)
        self.work_name_old = work_name_old
        self.building_name_old = building_name_old
        self.unit_old = unit_old
        self.date_st_date_act_am_work_perf.setDateRange(datetime.date.fromisoformat("2022-01-01"),
                                                        datetime.date.fromisoformat("2023-12-31"))
        self.date_end_date_act_am_work_perf.setDateRange(datetime.date.fromisoformat("2022-01-01"),
                                                         datetime.date.fromisoformat("2023-12-31"))
        self.date_date_of_remain_vol.setDateRange(datetime.date.fromisoformat("2022-01-01"),
                                                  datetime.date.fromisoformat("2023-12-31"))
        self.sBact_am_work_performed.setRange(0, 10000)
        self.sBvolume_per_object.setRange(1, 10000)
        self.sBremaining_volume.setRange(0, 10000)
        self.buildings = []
        self.SelectBuildingName()
        self.pushButtonUpdateData.clicked.connect(self.UpdateData)

    def UpdateData(self):
        if self.linework_name_report.text() != "" and self.lineunit.text() != "":
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Update report_on_compl_works
                                      set "work_name_report" = %s,
                                      "building_name" = %s,
                                      "unit" = %s, "volume_per_object" = %s, "act_am_work_performed" = %s,
                                      "st_date_act_am_work_perf" = %s, "end_date_act_am_work_perf"= %s,
                                       "remaining_volume" = %s, "date_of_remain_vol" = %s
                                      where "work_name_report" = %s and "building_name" = %s and "unit" = %s """,
                                   (self.linework_name_report.text(), self.cBbuilding_name.currentText(),
                                    self.lineunit.text(), self.sBvolume_per_object.value(),
                                    self.sBact_am_work_performed.value(),
                                    self.date_st_date_act_am_work_perf.date().toPyDate().strftime("%Y-%m-%d"),
                                    self.date_end_date_act_am_work_perf.date().toPyDate().strftime("%Y-%m-%d"),
                                    self.sBremaining_volume.value(),
                                    self.date_date_of_remain_vol.date().toPyDate().strftime("%Y-%m-%d"),
                                    self.work_name_old, self.building_name_old, self.unit_old))
                conn.commit()
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Successful data modification!"))
            msgBoxFileLoaded.setText(tr("The data has been successfully changed in the table report_on_compl_works!"))
            msgBoxFileLoaded.exec_()
        else:
            msgBoxFileLoaded = QMessageBox()
            msgBoxFileLoaded.setWindowTitle(tr("Error data!"))
            msgBoxFileLoaded.setText(tr("The data was not added to the table report_on_compl_works"
                                        " because the entered data does not match the format!"))
            msgBoxFileLoaded.exec_()
        self.close()

    def SelectBuildingName(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "Building_name_reg" from reg_buildings_in_district')
                self.buildings = cursor.fetchall()
                for note in self.buildings:
                    for w in note:
                        self.cBbuilding_name.addItem(w)


class Dialog_DeleteADDSearch(QDialog, Ui_DialogDelADDSearch):
    def __init__(self, parent=None):
        super(Dialog_DeleteADDSearch, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.resize(850, 600)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.rBDirOfWorks.clicked.connect(self.showDirofWorks)
        self.rBBuildingsData.clicked.connect(self.showBuildingsData)
        self.rBStateElemEst.clicked.connect(self.showStateElemEstData)
        self.rBl_of_vol_of_works.clicked.connect(self.show_list_of_volume_of_works)
        self.rBam_works_per_building_GPM.clicked.connect(self.show_am_works_per_building_GPM)
        self.rBreport_on_compl_works.clicked.connect(self.show_report_on_compl_works)
        self.DirofWorks = []
        self.StElEstim = []
        self.BuildingsData = []
        self.listOfVolWork = []
        self.report_on_compl_works = []
        self.am_works_per_building_GPM = []
        # проверка на порядок вставки данеых в БД
        self.GESN_ID_Check = ""
        self.GESN_ID = ""
        # данные конкретной ячейки
        self.CellData = ""
        # выбранный индекс таблицы (колонки)
        self.index_table = 0
        self.tableView.clicked.connect(self.selectedCell)
        self.PushSearchData.clicked.connect(self.searchData)
        self.lineEdit_2.selectionChanged.connect(self.checkLineEdit_2)
        self.PushAddData.clicked.connect(self.addData)
        self.PushDeleteData.clicked.connect(self.deleteData)
        self.PushUpdateData.clicked.connect(self.updateData)

    def updateData(self):
        if self.rBDirOfWorks.isChecked():
            if self.index_table == 2:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("""Select "work_name", "gesn_id", "unit"
                        from directory_of_works
                        where "gesn_id" = %s""", (str(self.CellData).strip('"'),))
                        DirOfWorks = cursor.fetchall()
                        if len(DirOfWorks) > 0:
                            Dialog = DialogUpdateDirOfWorks(DirOfWorks[0][0])
                            Dialog.lineGesn_id.setText(DirOfWorks[0][1])
                            Dialog.lineWork_name.setText(DirOfWorks[0][0])
                            Dialog.lineUnit.setText(DirOfWorks[0][2])
                            Dialog.exec_()
                            self.showDirofWorks()
                        else:
                            return
            else:
                return
        elif self.rBBuildingsData.isChecked():
            if self.index_table == 1:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute('Select "Floors", "Entrances", "Building_name_reg", "Number_of_building"'
                                       ' from reg_buildings_in_district '
                                       'where "Number_of_building" = %s', (str(self.CellData).strip('"'),))
                        BuildingsData = cursor.fetchall()
                        if len(BuildingsData) > 0:
                            if BuildingsData[0][0] is None:
                                BuildingsData[0][0] = 0
                            if BuildingsData[0][1] is None:
                                BuildingsData[0][1] = 0
                            Dialog = DialogUpdateRegBuildingsInDistrict(BuildingsData[0][0], BuildingsData[0][1],
                                                                        BuildingsData[0][2], BuildingsData[0][3])

                            Dialog.spinAmOfFloors.setValue(BuildingsData[0][0])
                            Dialog.spinAmOfEntrances.setValue(BuildingsData[0][1])
                            Dialog.lineBuilding_name_reg.setText(BuildingsData[0][2])
                            Dialog.spinNumber_of_building.setValue(BuildingsData[0][3])
                            Dialog.exec_()
                            self.showBuildingsData()
                        else:
                            return
            else:
                return
        elif self.rBl_of_vol_of_works.isChecked():
            if self.index_table == 1:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute("""Select "work_name", "Scope_of_work_per_floor",
                        "Scope_of_SMR_in_thousand_rub_per_floor", "duration_of_work" from
                         list_of_volume_of_works where "work_name" = %s """, (str(self.CellData).strip('"'),))
                        ListOfVolWorks = cursor.fetchall()
                        if len(ListOfVolWorks) > 0:
                            Dialog = DialogUpdateListOfVolumeOfWorks(str(self.CellData).strip('"'))
                            for i in range(Dialog.cBWork_name.count()):
                                if Dialog.cBWork_name.itemText(i) == str(self.CellData).strip('"'):
                                    Dialog.cBWork_name.setCurrentIndex(i)
                                    break
                            Dialog.dBlScope_of_work_per_floor.setValue(ListOfVolWorks[0][1])
                            Dialog.dBScope_of_SMR_in_thousand_rub_per_floor.setValue(ListOfVolWorks[0][2])
                            Dialog.dBduration_of_work.setValue(ListOfVolWorks[0][3])
                            Dialog.exec_()
                            self.show_list_of_volume_of_works()
                        else:
                            return
            else:
                return
        elif self.rBStateElemEst.isChecked():
            if self.index_table == 1:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        cursor.execute('Select "gesn_id", "gesn_unit", "gesn_name"'
                                       ' from state_element_estimates '
                                       'where "gesn_id" = %s', (str(self.CellData).strip('"'),))
                        StElEstimates = cursor.fetchall()
                        if len(StElEstimates) > 0:
                            # запись измененного номера ГЭСНА
                            self.GESN_ID = str(self.CellData).strip('"')
                            Dialog = DialogUpdateStateElementEstimates(str(self.CellData).strip('"'))
                            Dialog.lineGesn_id.setText(StElEstimates[0][0])
                            Dialog.lineUnit.setText(StElEstimates[0][1])
                            Dialog.lineGesn_name.setText(StElEstimates[0][2])
                            Dialog.exec_()
                            self.showStateElemEstData()
                        else:
                            return
            else:
                return
        elif self.rBam_works_per_building_GPM.isChecked():
            if self.index_table == 1:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        index = (self.tableView.selectionModel().currentIndex())
                        data = []
                        for i in range(5):
                            data.append(index.sibling(index.row(), i).data())
                        cursor.execute("""Select "building_name", "work_name",
                              "unit", "name_of_GPM", "volume_of_works" from
                               "am_works_per_building_GPM" 
                               where "building_name" = %s and
                                "work_name" = %s and 
                                "unit" = %s and
                                "name_of_GPM" = %s and
                                "volume_of_works" = %s  """, (data[0].strip('"'),
                                                              data[1].strip('"'),
                                                              data[2].strip('"'),
                                                              data[3].strip('"'),
                                                              float(data[4])))
                        AmWorksPerBuildingGPM = cursor.fetchall()
                        if len(AmWorksPerBuildingGPM) > 0:
                            Dialog = DialogUpdateDataToAM_works_per_build_GPM(data[0].strip('"'),
                                                                              data[1].strip('"'),
                                                                              data[2].strip('"'),
                                                                              data[3].strip('"'),
                                                                              float(data[4]))
                            for i in range(Dialog.cBWork_name.count()):
                                if Dialog.cBWork_name.itemText(i) == data[1].strip('"'):
                                    Dialog.cBWork_name.setCurrentIndex(i)
                                    break
                            for j in range(Dialog.cBUnit.count()):
                                if Dialog.cBUnit.itemText(j) == data[2].strip('"'):
                                    Dialog.cBUnit.setCurrentIndex(j)
                                    break
                            for k in range(Dialog.cBName_of_GPM.count()):
                                if Dialog.cBName_of_GPM.itemText(k) == data[3].strip('"'):
                                    Dialog.cBName_of_GPM.setCurrentIndex(k)
                                    break
                            for o in range(Dialog.cBBuilding_name.count()):
                                if Dialog.cBBuilding_name.itemText(o) == data[0].strip('"'):
                                    Dialog.cBBuilding_name.setCurrentIndex(o)
                                    break
                            Dialog.dsBVol_of_works.setValue(float(data[4]))
                            Dialog.exec_()
                            self.show_am_works_per_building_GPM()
                        else:
                            return
            else:
                return
        elif self.rBreport_on_compl_works.isChecked():
            if self.index_table == 1:
                with closing(connect_to_DB()) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        index = (self.tableView.selectionModel().currentIndex())
                        data = []
                        for i in range(9):
                            data.append(index.sibling(index.row(), i).data())
                        cursor.execute("""Select "work_name_report", "building_name",
                                                     "unit", "volume_per_object", "act_am_work_performed",
                                                      "st_date_act_am_work_perf", "end_date_act_am_work_perf",
                                                       "remaining_volume", "date_of_remain_vol" from
                                                      "report_on_compl_works" 
                                                      where "work_name_report" = %s and
                                                       "building_name" = %s and "unit" = %s and
                                                       "volume_per_object" = %s and
                                                       "st_date_act_am_work_perf" = %s and
                                                       "end_date_act_am_work_perf" = %s and
                                                        "date_of_remain_vol" = %s""", (data[0].strip('"'),
                                                                                       data[1].strip('"'),
                                                                                       data[2].strip('"'),
                                                                                       data[3], data[5],
                                                                                       data[6], data[8]))
                        r_on_works = cursor.fetchall()
                        if len(r_on_works) > 0:
                            Dialog = DialogUpdateInReport_on_compl_works(data[0].strip('"'),
                                                                         data[1].strip('"'),
                                                                         data[2].strip('"'))
                            for i in range(Dialog.cBbuilding_name.count()):
                                if Dialog.cBbuilding_name.itemText(i) == r_on_works[0][1]:
                                    Dialog.cBbuilding_name.setCurrentIndex(i)
                                    break
                            if not isinstance(r_on_works[0][4], int):
                                r_on_works[0][4] = 0
                            if not isinstance(r_on_works[0][7], int):
                                r_on_works[0][7] = 0
                            Dialog.linework_name_report.setText(r_on_works[0][0])
                            Dialog.lineunit.setText(r_on_works[0][2])
                            Dialog.sBvolume_per_object.setValue(r_on_works[0][3])
                            Dialog.date_st_date_act_am_work_perf.setDate(r_on_works[0][5])
                            Dialog.date_end_date_act_am_work_perf.setDate(r_on_works[0][6])
                            Dialog.date_date_of_remain_vol.setDate(r_on_works[0][8])
                            Dialog.sBact_am_work_performed.setValue(r_on_works[0][4])
                            Dialog.sBremaining_volume.setValue(r_on_works[0][7])
                            Dialog.exec_()
                            self.show_report_on_compl_works()
                        else:
                            return
            else:
                return

    def addData(self):
        if self.rBDirOfWorks.isChecked():
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Select * from state_element_estimates
                    where "gesn_id" = %s""", (self.GESN_ID,))
                    checkGESN = cursor.fetchall()
            if self.GESN_ID_Check != "" and len(checkGESN) != 0:
                DialogAdd = DialogAddToDirectoryOfWorks()
                DialogAdd.lineGESN_ID.setText(self.GESN_ID_Check)
                DialogAdd.exec_()
                self.showDirofWorks()
            else:
                msgBoxFileLoaded = QMessageBox()
                msgBoxFileLoaded.setWindowTitle(tr("Error in the order of entering data into the database!"))
                msgBoxFileLoaded.setText(tr("First you need to enter the data in the table "
                                            "state_element_estimates!"))
                msgBoxFileLoaded.exec_()

        elif self.rBStateElemEst.isChecked():
            Dialog = DialogAddToStateElementEstimates()
            Dialog.exec_()
            self.GESN_ID = Dialog.lineGesn_id.text()
            self.showStateElemEstData()
            self.GESN_ID_Check = self.GESN_ID

        elif self.rBBuildingsData.isChecked():
            DialogAdd = DialogAddToRegBuildingsinDistrict()
            N_Building = 0
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute("""Select MAX("Number_of_building") from reg_buildings_in_district""")
                    Number_of_buildings = cursor.fetchone()
            for result in Number_of_buildings:
                N_Building = result
            DialogAdd.spinBox_NumberOfBuilding.setValue(N_Building + 1)
            DialogAdd.exec_()
            self.showBuildingsData()

        elif self.rBl_of_vol_of_works.isChecked():
            DialogAdd = DialogAddToListOfVolumeOfWorks()
            DialogAdd.exec_()
            self.show_list_of_volume_of_works()

        elif self.rBam_works_per_building_GPM.isChecked():
            DialogAdd = DialogAddToAmWorksPerBuilding_GPM()
            DialogAdd.exec_()
            self.show_am_works_per_building_GPM()

        elif self.rBreport_on_compl_works.isChecked():
            DialogAdd = DialogAddToReport_on_compl_works()
            DialogAdd.exec_()
            self.show_report_on_compl_works()

    def deleteData(self):
        text_delete = self.lineEdit.text().strip('"')
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                if self.rBBuildingsData.isChecked() and self.index_table == 2:
                    cursor.execute("""Select * from calendar_plan_el_works 
                    where "building_name" = %s""", (text_delete,))
                    b_info = cursor.fetchall()
                    cursor.execute("""Select * from report_on_compl_works 
                                        where "building_name" = %s""", (text_delete,))
                    rep_info = cursor.fetchall()
                    cursor.execute("""Select * from "am_works_per_building_GPM"
                                                           where "building_name" = %s""", (text_delete,))
                    am_info = cursor.fetchall()
                    cursor.execute("""Select * from "сal_sch_constr_works" where "building_name" = %s""",
                                   (text_delete,))
                    cal_sch_info = cursor.fetchall()
                    cursor.execute("""Select * from "cert_of_compl_works_for_month" where "building_name" = %s""",
                                   (text_delete,))
                    cert_of_compl_works_info = cursor.fetchall()
                    if len(b_info) > 0 or len(rep_info) > 0 or len(am_info) > 0 or\
                            len(cal_sch_info) > 0 or len(cert_of_compl_works_info) > 0:
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Data deletion error from the database"))
                        msgBoxFileLoaded.setText(tr("You can't delete data because it already "
                                                    "exists in other tables!"))
                        msgBoxFileLoaded.exec_()
                    else:
                        cursor.execute("""Delete from reg_buildings_in_district where
                                       "Building_name_reg" = %s""", (text_delete,))
                        conn.commit()
                        cursor.close()
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Deleting data from the database"))
                        msgBoxFileLoaded.setText(tr("Row with the selected data has been deleted!"))
                        msgBoxFileLoaded.exec_()
                    self.showBuildingsData()
                elif self.rBDirOfWorks.isChecked() and self.index_table == 1:
                    cursor.execute("""Select * from report_on_compl_works 
                                                         where "work_name_report" = %s""", (text_delete,))
                    rep_info = cursor.fetchall()
                    cursor.execute("""Select * from "am_works_per_building_GPM" where "work_name" = %s""",
                                   (text_delete,))
                    am_info = cursor.fetchall()
                    cursor.execute("""Select * from "list_of_volume_of_works" where "work_name" = %s""",
                                   (text_delete,))
                    list_of_vol_works_info = cursor.fetchall()
                    if len(rep_info) > 0 or len(am_info) > 0 or len(list_of_vol_works_info) > 0:
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Data deletion error from the database"))
                        msgBoxFileLoaded.setText(tr("You can't delete data because it already "
                                                    "exists in other tables!"))
                        msgBoxFileLoaded.exec_()
                    else:
                        cursor.execute("""Delete from directory_of_works where "work_name" = %s""", (text_delete,))
                        conn.commit()
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Deleting data from the database"))
                        msgBoxFileLoaded.setText(tr("Row with the selected data has been deleted!"))
                        msgBoxFileLoaded.exec_()
                    cursor.close()
                    self.showDirofWorks()
                elif self.rBStateElemEst.isChecked() and self.index_table == 3:
                    cursor.execute("""Select "gesn_id" from "state_element_estimates" where "gesn_name" = %s""",
                                   (text_delete,))
                    gesn_id = cursor.fetchone()[0]
                    cursor.execute("""Select * from "staffing_arrangements" where "gesn_id" = %s""",
                                   (gesn_id,))
                    st_arr_info = cursor.fetchall()
                    cursor.execute("""Select * from "directory_of_works" where "gesn_id" = %s""",
                                   (gesn_id,))
                    dir_of_works_info = cursor.fetchall()
                    cursor.execute("""Select * from "exploition of GPM" where "gesn_id" = %s""",
                                   (gesn_id,))
                    explotion_info = cursor.fetchall()
                    if len(st_arr_info) > 0 or len(dir_of_works_info) > 0 or len(explotion_info) > 0:
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Data deletion error from the database"))
                        msgBoxFileLoaded.setText(tr("You can't delete data because it already "
                                                    "exists in other tables!"))
                        msgBoxFileLoaded.exec_()
                    else:
                        cursor.execute("Delete from state_element_estimates where "
                                       "gesn_name = %s", (text_delete,))
                        conn.commit()
                        msgBoxFileLoaded = QMessageBox()
                        msgBoxFileLoaded.setWindowTitle(tr("Deleting data from the database"))
                        msgBoxFileLoaded.setText(tr("Row with the selected data has been deleted!"))
                        msgBoxFileLoaded.exec_()
                    cursor.close()
                    self.showStateElemEstData()
                elif self.rBl_of_vol_of_works.isChecked() and self.index_table == 1:
                    index = (self.tableView.selectionModel().currentIndex())
                    data = []
                    for i in range(4):
                        data.append(index.sibling(index.row(), i).data())
                    cursor.execute("""Delete from list_of_volume_of_works where
                                   "work_name" = %s and "Scope_of_work_per_floor" = %s and
                                   "Scope_of_SMR_in_thousand_rub_per_floor" = %s and
                                    "duration_of_work" = %s  """, (data[0].strip('"'),
                                                                   data[1], data[2], data[3]))
                    conn.commit()
                    cursor.close()
                    msgBoxFileLoaded = QMessageBox()
                    msgBoxFileLoaded.setWindowTitle(tr("Deleting data from the database"))
                    msgBoxFileLoaded.setText(tr("Row with the selected data has been deleted!"))
                    msgBoxFileLoaded.exec_()
                    self.show_list_of_volume_of_works()
                elif self.rBam_works_per_building_GPM.isChecked() and self.index_table == 1:
                    index = (self.tableView.selectionModel().currentIndex())
                    data = []
                    for i in range(5):
                        data.append(index.sibling(index.row(), i).data())
                    cursor.execute("""Delete from "am_works_per_building_GPM" where
                                   "building_name" = %s and "work_name" = %s and
                                   "unit" = %s and "name_of_GPM" = %s and "volume_of_works" = %s""",
                                   (data[0].strip('"'), data[1].strip('"'),
                                    data[2].strip('"'), data[3].strip('"'), float(data[4])))
                    conn.commit()
                    cursor.close()
                    msgBoxFileLoaded = QMessageBox()
                    msgBoxFileLoaded.setWindowTitle(tr("Deleting data from the database"))
                    msgBoxFileLoaded.setText(tr("Row with the selected data has been deleted!"))
                    msgBoxFileLoaded.exec_()
                    self.show_am_works_per_building_GPM()
                elif self.rBreport_on_compl_works.isChecked() and self.index_table == 1:
                    index = (self.tableView.selectionModel().currentIndex())
                    data = []
                    for i in range(9):
                        data.append(index.sibling(index.row(), i).data())
                    cursor.execute("""Delete from "report_on_compl_works"
                                    where "work_name_report" = %s and
                                    "building_name" = %s and "unit" = %s and
                                    "volume_per_object" = %s and
                                    "st_date_act_am_work_perf" = %s and
                                    "end_date_act_am_work_perf" = %s and
                                    "date_of_remain_vol" = %s""", (data[0].strip('"'),
                                                                   data[1].strip('"'),
                                                                   data[2].strip('"'),
                                                                   data[3], data[5],
                                                                   data[6], data[8]))
                    conn.commit()
                    cursor.close()
                    msgBoxFileLoaded = QMessageBox()
                    msgBoxFileLoaded.setWindowTitle(tr("Deleting data from the database"))
                    msgBoxFileLoaded.setText(tr("Row with the selected data has been deleted!"))
                    msgBoxFileLoaded.exec_()
                    self.show_report_on_compl_works()

    # проверка поисковой строки на заполняемость, если ничего нет -то выводим таблицу заново
    def checkLineEdit_2(self):
        if self.rBDirOfWorks.isChecked() and self.lineEdit_2.text() == "":
            self.showDirofWorks()
        elif self.rBBuildingsData.isChecked() and self.lineEdit_2.text() == "":
            self.showBuildingsData()
        elif self.rBStateElemEst.isChecked() and self.lineEdit_2.text() == "":
            self.showStateElemEstData()
        elif self.rBl_of_vol_of_works.isChecked() and self.lineEdit_2.text() == "":
            self.show_list_of_volume_of_works()
        elif self.rBam_works_per_building_GPM.isChecked() and self.lineEdit_2.text() == "":
            self.show_am_works_per_building_GPM()
        elif self.rBreport_on_compl_works.isChecked() and self.lineEdit_2.text() == "":
            self.show_report_on_compl_works()

    def selectedCell(self):
        # данные конкретной ячейки
        self.CellData = self.tableView.model().data(self.tableView.currentIndex(), role=0)
        # выбранный индекс таблицы
        self.index_table = self.tableView.selectedIndexes()[0].column() + 1
        # print('Column %d is selected' % self.index_table)
        self.lineEdit.setText(self.CellData)
        self.lineEdit_2.setText(self.CellData)
        # print("Данные из выбранной ячейки tableview        -> {}".format(
        #     self.tableView.model().data(self.tableView.currentIndex(), role=0)))

    def searchData(self):
        if self.rBStateElemEst.isChecked() or self.rBBuildingsData.isChecked() \
                or self.rBDirOfWorks.isChecked() or self.rBl_of_vol_of_works.isChecked() \
                or self.rBam_works_per_building_GPM.isChecked() or self.rBreport_on_compl_works.isChecked():
            DataFromSearchLine = self.lineEdit_2.text().strip('"')
            with closing(connect_to_DB()) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    if self.rBDirOfWorks.isChecked():
                        cursor.execute('Select * from directory_of_works where work_name = %s',
                                       (DataFromSearchLine,))
                        DirofWorks = cursor.fetchall()
                        Data = pd.DataFrame(DirofWorks,
                                            index=[j + 1 for j in range(len(DirofWorks))],
                                            columns=["work_name", "gesn_id", "unit"])
                    elif self.rBBuildingsData.isChecked():
                        cursor.execute("""Select "Number_of_building", "Building_name_reg",
                                        "Floors", "Entrances", "Total_number_of_floors"
                                                          from reg_buildings_in_district
                                                          where "Building_name_reg" = %s """,
                                       (DataFromSearchLine,))
                        BuildingsData = cursor.fetchall()
                        Data = pd.DataFrame(BuildingsData,
                                            index=[i + 1 for i in range(len(BuildingsData))],
                                            columns=["Number_of_building", "Building_name_reg",
                                                     "Floors", "Entrances", "Total_number_of_floors"])
                    elif self.rBStateElemEst.isChecked():
                        cursor.execute('Select "gesn_id", "gesn_unit", "gesn_name"'
                                       ' from state_element_estimates'
                                       ' where "gesn_name" = %s', (DataFromSearchLine,))
                        StateElEstimates = cursor.fetchall()
                        Data = pd.DataFrame(StateElEstimates,
                                            index=[i + 1 for i in range(len(StateElEstimates))],
                                            columns=["gesn_id", "gesn_unit", "gesn_name"])
                    elif self.rBl_of_vol_of_works.isChecked():
                        cursor.execute("""Select "work_name", "Scope_of_work_per_floor",
                                     "Scope_of_SMR_in_thousand_rub_per_floor", "duration_of_work" 
                                     from list_of_volume_of_works
                                     where "work_name" = %s """, (DataFromSearchLine,))
                        list_of_vol_works = cursor.fetchall()
                        Data = pd.DataFrame(list_of_vol_works,
                                            index=[i + 1 for i in range(len(list_of_vol_works))],
                                            columns=["work_name", "Scope_of_work_per_floor",
                                                     "Scope_of_SMR_in_thousand_rub_per_floor",
                                                     "duration_of_work"])
                    elif self.rBam_works_per_building_GPM.isChecked():
                        cursor.execute("""Select "building_name", "work_name",
                                     "unit", "name_of_GPM", "volume_of_works" 
                                     from "am_works_per_building_GPM" where "building_name" = %s
                                      Order by "building_ID" """, (DataFromSearchLine,))
                        am_works_per_building = cursor.fetchall()
                        Data = pd.DataFrame(am_works_per_building,
                                            index=[i + 1 for i in range(len(am_works_per_building))],
                                            columns=["building_name", "work_name",
                                                     "unit", "name_of_GPM", "volume_of_works"])
                    elif self.rBreport_on_compl_works.isChecked():
                        cursor.execute("""Select "work_name_report", "building_name", "unit",
                "volume_per_object", "act_am_work_performed", "st_date_act_am_work_perf",
                "end_date_act_am_work_perf", "remaining_volume", "date_of_remain_vol"
                 from report_on_compl_works where "work_name_report" = %s
                 ORDER BY "Report_ID" ASC """, (DataFromSearchLine,))
                        report_on_compl_works = cursor.fetchall()
                        Data = pd.DataFrame(report_on_compl_works,
                                            index=[i + 1 for i in range(len(report_on_compl_works))],
                                            columns=["work_name_report", "building_name",
                                                     "unit", "volume_per_object", "act_am_work_performed",
                                                     "st_date_act_am_work_perf", "end_date_act_am_work_perf",
                                                     "remaining_volume", "date_of_remain_vol"])
            self.tableView.setModel(TableModel(Data))

    def show_report_on_compl_works(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "work_name_report", "building_name", "unit",
                "volume_per_object", "act_am_work_performed", "st_date_act_am_work_perf",
                "end_date_act_am_work_perf", "remaining_volume", "date_of_remain_vol"
                 from report_on_compl_works ORDER BY "Report_ID" ASC """)
                self.report_on_compl_works = cursor.fetchall()
            Data = pd.DataFrame(self.report_on_compl_works,
                                index=[j + 1 for j in range(len(self.report_on_compl_works))],
                                columns=["work_name_report", "building_name",
                                         "unit", "volume_per_object", "act_am_work_performed",
                                         "st_date_act_am_work_perf", "end_date_act_am_work_perf",
                                         "remaining_volume", "date_of_remain_vol"])
            self.tableView.setModel(TableModel(Data))

    def show_am_works_per_building_GPM(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "building_name", "work_name",
                 "unit", "name_of_GPM", "volume_of_works" 
                 from "am_works_per_building_GPM" Order by "building_ID" """)
                self.am_works_per_building_GPM = cursor.fetchall()
        Data = pd.DataFrame(self.am_works_per_building_GPM,
                            index=[j + 1 for j in range(len(self.am_works_per_building_GPM))],
                            columns=["building_name", "work_name",
                                     "unit", "name_of_GPM", "volume_of_works"])
        self.tableView.setModel(TableModel(Data))

    def show_list_of_volume_of_works(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "work_name", "Scope_of_work_per_floor",
                 "Scope_of_SMR_in_thousand_rub_per_floor", "duration_of_work" 
                 from list_of_volume_of_works ORDER BY "Work_ID" ASC """)
                self.listOfVolWork = cursor.fetchall()
        Data = pd.DataFrame(self.listOfVolWork,
                            index=[j + 1 for j in range(len(self.listOfVolWork))],
                            columns=["work_name", "Scope_of_work_per_floor",
                                     "Scope_of_SMR_in_thousand_rub_per_floor", "duration_of_work"])
        self.tableView.setModel(TableModel(Data))

    def showStateElemEstData(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select "gesn_id", "gesn_unit", "gesn_name"'
                               ' from state_element_estimates Order by gesn_id')
                self.StElEstim = cursor.fetchall()
        Data = pd.DataFrame(self.StElEstim,
                            index=[j + 1 for j in range(len(self.StElEstim))],
                            columns=["gesn_id", "gesn_unit", "gesn_name"])
        self.tableView.setModel(TableModel(Data))

    def showDirofWorks(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('Select * from directory_of_works Order by gesn_id')
                self.DirofWorks = cursor.fetchall()
        Data = pd.DataFrame(self.DirofWorks,
                            index=[j + 1 for j in range(len(self.DirofWorks))],
                            columns=["work_name", "gesn_id", "unit"])
        self.tableView.setModel(TableModel(Data))

    def showBuildingsData(self):
        with closing(connect_to_DB()) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""Select "Number_of_building", "Building_name_reg",
                "Floors", "Entrances", "Total_number_of_floors"
                                  from reg_buildings_in_district
                                  Order by "Number_of_building" """)
                self.BuildingsData = cursor.fetchall()
        Data = pd.DataFrame(self.BuildingsData,
                            index=[i + 1 for i in range(len(self.BuildingsData))],
                            columns=["Number_of_building", "Building_name_reg",
                                     "Floors", "Entrances", "Total_number_of_floors"])
        self.tableView.setModel(TableModel(Data))


class DialogActions(QDialog, Ui_DialogActions):
    def __init__(self, data, ddata, data_sheet, flag=None, parent=None):
        super(DialogActions, self).__init__(parent)
        self.setupUi(self)
        self.DialogADDSearchDelete = Dialog_DeleteADDSearch()
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setOrientation(QPrinter.Landscape)
        self.printer.setPaperSize(QPrinter.A4)
        self.printer.setPageSize(QPrinter.A4)
        self.printer.setPageMargins(5, 5, 5, 5, QPrinter.Millimeter)
        self.doc = QtGui.QTextDocument()
        self.cursor = QTextCursor(self.doc)
        self.DataFrame = data
        self.Data = ddata
        self.flag = flag
        self.resDoc = data_sheet
        tableFormat = QTextTableFormat()
        tableFormat.setBorder(0.2)
        tableFormat.setBorderStyle(3)
        tableFormat.setCellSpacing(0)
        tableFormat.setTopMargin(0)
        tableFormat.setCellPadding(4)
        self.pushPrint.clicked.connect(self.print_file)
        self.pushPrintPreview.clicked.connect(self.print_preview_dialog)
        self.pushSaveData.clicked.connect(self.saveData)
        self.pushSearchData.clicked.connect(self.DialogADDSearchDelete.show)
        self.pushAddData.clicked.connect(self.DialogADDSearchDelete.show)
        self.pushDeleteData.clicked.connect(self.DialogADDSearchDelete.show)
        self.pushUpdateData.clicked.connect(self.DialogADDSearchDelete.show)

    def print_file(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec():
            if QPrintDialog.accepted:
                self.doc.print_(self.printer)

    def print_preview_dialog(self):
        previewDialog = QPrintPreviewDialog(self.printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPreview(self):
        self.doc.print_(self.printer)

    def saveData(self):
        # запись содержимого в файл
        df_list = [self.Data, self.DataFrame]
        if self.flag is None:
            with pd.ExcelWriter(self.resDoc + ".xlsx") as writer:
                row = 0
                for i, dataframe in enumerate(df_list):
                    if i == 0:
                        dataframe.to_excel(writer, sheet_name=self.resDoc, index=False,
                                           startrow=row, startcol=0, header=None)
                    else:
                        dataframe.to_excel(writer, sheet_name=self.resDoc, index=False,
                                           startrow=row, startcol=0)
                    row = row + len(dataframe.index) + 1 + 1
                    # выравнивание текста в колонках по ширине
                for column in self.DataFrame:
                    column_width = max(self.DataFrame[column].astype(str).map(len).max(), len(column))
                    col_idx = self.DataFrame.columns.get_loc(column)
                    writer.sheets[self.resDoc].set_column(col_idx, col_idx, column_width + 2)
        else:
            with pd.ExcelWriter(self.resDoc + ".xlsx", engine='xlsxwriter') as writer:
                row = 0
                workbook = writer.book
                merge_format1 = workbook.add_format({
                    'align': 'center',
                    'valign': 'vcenter'
                })
                new_format = workbook.add_format()
                new_format.set_align('left')
                new_format.set_valign('vcenter')
                start_cell = 9
                for i, dataframe in enumerate(df_list):
                    if i == 0:
                        dataframe.to_excel(writer, sheet_name=self.resDoc, index=False,
                                           startrow=row, startcol=0, header=None)
                    else:
                        writer.sheets[self.resDoc].merge_range(row + 1, 0, start_cell + 3, 0,
                                                               self.DataFrame.loc[row - 1, 'Наименование объекта'])
                        writer.sheets[self.resDoc].merge_range(row + 1, 1, start_cell + 3, 1,
                                                               self.DataFrame.loc[row - 1, 'Номер бригады'])
                        writer.sheets[self.resDoc].merge_range(row + 1, 2, start_cell + 3, 2,
                                                               self.DataFrame.loc[row - 1, 'Специальность рабочего'])
                        writer.sheets[self.resDoc].merge_range(row + 1, 4, start_cell + 3, 4,
                                                               self.DataFrame.loc[row - 1, 'Разряд специалиста'])
                        dataframe.to_excel(writer, sheet_name=self.resDoc, index=False,
                                           startrow=row, startcol=0)
                    row = row + len(dataframe.index) + 1 + 1
                    # выравнивание текста в колонках по ширине
                last_date = ""
                for column in self.DataFrame:
                    column_width = max(self.DataFrame[column].astype(str).map(len).max(), len(column))
                    col_idx = self.DataFrame.columns.get_loc(column)
                    writer.sheets[self.resDoc].set_column(col_idx, col_idx, column_width + 2, merge_format1)
                    if column.startswith('Пятница '):
                        last_date = column
                writer.sheets[self.resDoc].set_column("A1:A3",
                                                      max(self.DataFrame["Наименование объекта"].astype(str).map(
                                                          len).max(),
                                                          len(column)) + 2, new_format)
                writer.sheets[self.resDoc].set_column("P1:P3",
                                                      max(self.DataFrame[last_date].astype(str).map(
                                                          len).max(),
                                                          len(column)) + 2, new_format)
                writer.sheets[self.resDoc].set_column("P15:P17",
                                                      max(self.DataFrame[last_date].astype(str).map(
                                                          len).max(),
                                                          len(column)) + 2, new_format)
        msgBoxFileLoaded = QMessageBox()
        msgBoxFileLoaded.setWindowTitle(tr("File Upload"))
        msgBoxFileLoaded.setText(tr("The output document was written to an excel file in a local directory!"))
        msgBoxFileLoaded.exec_()
        # print('Календарный план записан в файл excel в локальный каталог!')


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Get the raw value
            value = self._data.iloc[index.row(), index.column()]
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            # Perform per-type checks and render accordingly.

            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 1 dp
                return "%.2f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value

            if value is None:
                return

            return str(value)

        if role == Qt.DecorationRole:
            value = self._data.iloc[index.row()][index.column()]
            # if isinstance(value, bool):
            #     return QtGui.QIcon('line.png')

        # if role == Qt.BackgroundRole:
        #     if index.row() % 5 == 0 and index.row() != 0:
        #         return QBrush(Qt.green)

        if role == Qt.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]

            if isinstance(value, int) or isinstance(value, float) or isinstance(value, datetime.date):
                # Align center
                return Qt.AlignVCenter + Qt.AlignHCenter

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


if __name__ == '__main__':
    app = QApplication([])
    # Создание экземпляра класса Окна Авторизации программы
    MainWindow = MyWindow()
    # Создание экземпляра класса Окна Авторизации программы
    DAuth = DialogAuth()
    # Изменение темы окон на светлую
    onClickedLightTheme()
    DAuth.show()
    app.exec_()
# Пробная реализация
# translator = QTranslator(app)
# Form, Window = uic.loadUiType("mainwindow.ui")
# FormDialog_Size, WindowsDialog_Size = uic.loadUiType("Dialog_Size.ui")
# FormDialog_About, WindowsDialog_About = uic.loadUiType("Dialog_About.ui")
# FormDialog_Change_theme, WindowsDialog_Change_theme = \
#     uic.loadUiType("Dialog_Change_window_theme.ui")
# FormDialog_Authorization, WindowsDialog_Authorization =\
#     uic.loadUiType("Dialog_authorization.ui")
# window = Window()
# form = Form()
# form.setupUi(window)
# Создание экземпляра класса Диалогового Окна для изменения размера окна
# windowDialogSize = WindowsDialog_Size()
# form1 = FormDialog_Size()
# form1.setupUi(windowDialogSize)
# Создание экземпляра класса Диалогового Окна для вывода информации об авторе
# windowDialogAbout = WindowsDialog_About()
# form2 = FormDialog_About()
# form2.setupUi(windowDialogAbout)
# Создание экземпляра класса Диалогового Окна для изменения темы окна
# windowsDialog_Change_theme = WindowsDialog_Change_theme()
# form3 = FormDialog_Change_theme()
# form3.setupUi(windowsDialog_Change_theme)
# Создание экземпляра класса Диалогового Окна авторизации
# WindowsAuthorization = WindowsDialog_Authorization()
# form3.radioButtonLigthTheme.setChecked(True)
