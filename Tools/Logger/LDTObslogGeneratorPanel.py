# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LDTObslogGeneratorPanel.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1101, 830)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.TimesWorld = QtWidgets.QGroupBox(self.centralwidget)
        self.TimesWorld.setObjectName("TimesWorld")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.TimesWorld)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.txt_utc = QtWidgets.QLabel(self.TimesWorld)
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(50)
        self.txt_utc.setFont(font)
        self.txt_utc.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_utc.setObjectName("txt_utc")
        self.gridLayout_5.addWidget(self.txt_utc, 0, 0, 1, 1)
        self.txt_localtime = QtWidgets.QLabel(self.TimesWorld)
        font = QtGui.QFont()
        font.setFamily("Digital-7")
        font.setPointSize(50)
        self.txt_localtime.setFont(font)
        self.txt_localtime.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_localtime.setObjectName("txt_localtime")
        self.gridLayout_5.addWidget(self.txt_localtime, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.TimesWorld, 1, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName("tabWidget")
        self.dataLogTab = QtWidgets.QWidget()
        self.dataLogTab.setObjectName("dataLogTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dataLogTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.table_datalog = QtWidgets.QTableWidget(self.dataLogTab)
        self.table_datalog.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.table_datalog.setAlternatingRowColors(True)
        self.table_datalog.setObjectName("table_datalog")
        self.table_datalog.setColumnCount(0)
        self.table_datalog.setRowCount(0)
        self.gridLayout_3.addWidget(self.table_datalog, 9, 0, 1, 6)
        self.datalog_opendir = QtWidgets.QPushButton(self.dataLogTab)
        self.datalog_opendir.setObjectName("datalog_opendir")
        self.gridLayout_3.addWidget(self.datalog_opendir, 0, 0, 1, 1)
        self.txt_datalogdir = QtWidgets.QLabel(self.dataLogTab)
        font = QtGui.QFont()
        font.setItalic(True)
        self.txt_datalogdir.setFont(font)
        self.txt_datalogdir.setObjectName("txt_datalogdir")
        self.gridLayout_3.addWidget(self.txt_datalogdir, 0, 1, 1, 3)
        self.txt_datalogsavefile = QtWidgets.QLabel(self.dataLogTab)
        font = QtGui.QFont()
        font.setItalic(True)
        self.txt_datalogsavefile.setFont(font)
        self.txt_datalogsavefile.setObjectName("txt_datalogsavefile")
        self.gridLayout_3.addWidget(self.txt_datalogsavefile, 1, 1, 1, 3)
        self.datalog_savefile = QtWidgets.QPushButton(self.dataLogTab)
        self.datalog_savefile.setObjectName("datalog_savefile")
        self.gridLayout_3.addWidget(self.datalog_savefile, 1, 0, 1, 1)
        self.widget_6 = QtWidgets.QWidget(self.dataLogTab)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.datalog_editkeywords = QtWidgets.QPushButton(self.widget_6)
        self.datalog_editkeywords.setObjectName("datalog_editkeywords")
        self.gridLayout_14.addWidget(self.datalog_editkeywords, 0, 4, 1, 1)
        self.datalog_forcewrite = QtWidgets.QPushButton(self.widget_6)
        self.datalog_forcewrite.setObjectName("datalog_forcewrite")
        self.gridLayout_14.addWidget(self.datalog_forcewrite, 0, 1, 1, 1)
        self.datalog_addrow = QtWidgets.QPushButton(self.widget_6)
        self.datalog_addrow.setObjectName("datalog_addrow")
        self.gridLayout_14.addWidget(self.datalog_addrow, 0, 2, 1, 1)
        self.datalog_deleterow = QtWidgets.QPushButton(self.widget_6)
        self.datalog_deleterow.setObjectName("datalog_deleterow")
        self.gridLayout_14.addWidget(self.datalog_deleterow, 0, 3, 1, 1)
        self.datalog_forceupdate = QtWidgets.QPushButton(self.widget_6)
        self.datalog_forceupdate.setObjectName("datalog_forceupdate")
        self.gridLayout_14.addWidget(self.datalog_forceupdate, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.widget_6, 10, 0, 1, 6)
        self.widget_5 = QtWidgets.QWidget(self.dataLogTab)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.datalog_instrumentselect = QtWidgets.QComboBox(self.widget_5)
        self.datalog_instrumentselect.setObjectName("datalog_instrumentselect")
        self.datalog_instrumentselect.addItem("")
        self.datalog_instrumentselect.addItem("")
        self.datalog_instrumentselect.addItem("")
        self.datalog_instrumentselect.addItem("")
        self.datalog_instrumentselect.addItem("")
        self.gridLayout_12.addWidget(self.datalog_instrumentselect, 1, 3, 1, 1)
        self.datalog_autoupdate = QtWidgets.QCheckBox(self.widget_5)
        self.datalog_autoupdate.setChecked(True)
        self.datalog_autoupdate.setObjectName("datalog_autoupdate")
        self.gridLayout_12.addWidget(self.datalog_autoupdate, 0, 1, 1, 1)
        self.txt_datalog_instrument = QtWidgets.QLabel(self.widget_5)
        self.txt_datalog_instrument.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_datalog_instrument.setObjectName("txt_datalog_instrument")
        self.gridLayout_12.addWidget(self.txt_datalog_instrument, 1, 1, 1, 1)
        self.datalog_updateinterval = QtWidgets.QSpinBox(self.widget_5)
        self.datalog_updateinterval.setAlignment(QtCore.Qt.AlignCenter)
        self.datalog_updateinterval.setProperty("value", 60)
        self.datalog_updateinterval.setObjectName("datalog_updateinterval")
        self.gridLayout_12.addWidget(self.datalog_updateinterval, 0, 3, 1, 1)
        self.gridLayout_3.addWidget(self.widget_5, 0, 4, 2, 2)
        self.tabWidget.addTab(self.dataLogTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LDT Observing Log Autogenerator"))
        self.TimesWorld.setTitle(_translate("MainWindow", "World Times"))
        self.txt_utc.setText(_translate("MainWindow", "UTC"))
        self.txt_localtime.setText(_translate("MainWindow", "LOCAL"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Logging"))
        self.datalog_opendir.setText(_translate("MainWindow", "Set Data Directory"))
        self.txt_datalogdir.setText(_translate("MainWindow", "No Directory Chosen to Scan!"))
        self.txt_datalogsavefile.setText(_translate("MainWindow", "No Output Filename!"))
        self.datalog_savefile.setText(_translate("MainWindow", "Set Log Output File"))
        self.datalog_editkeywords.setText(_translate("MainWindow", "Edit Keywords ..."))
        self.datalog_forcewrite.setText(_translate("MainWindow", "Force Write"))
        self.datalog_addrow.setText(_translate("MainWindow", "Add a Blank Row"))
        self.datalog_deleterow.setText(_translate("MainWindow", "Remove Highlighted Row"))
        self.datalog_forceupdate.setText(_translate("MainWindow", "Force Update"))
        self.datalog_instrumentselect.setItemText(0, _translate("MainWindow", "LMI"))
        self.datalog_instrumentselect.setItemText(1, _translate("MainWindow", "DeVeny"))
        self.datalog_instrumentselect.setItemText(2, _translate("MainWindow", "NIHTS"))
        self.datalog_instrumentselect.setItemText(3, _translate("MainWindow", "RC1"))
        self.datalog_instrumentselect.setItemText(4, _translate("MainWindow", "RC2"))
        self.datalog_autoupdate.setText(_translate("MainWindow", "Autoupdate every:"))
        self.txt_datalog_instrument.setText(_translate("MainWindow", "Instrument:"))
        self.datalog_updateinterval.setSuffix(_translate("MainWindow", " seconds"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataLogTab), _translate("MainWindow", "Data Log"))
