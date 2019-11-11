# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openCamera.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton

class Ui_Mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.setEnabled(True)
        mainwindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        
        ###
        self.btnOpenCamera = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenCamera.setGeometry(QtCore.QRect(230, 470, 99, 27))
        self.btnOpenCamera.setObjectName("btnOpenCamera")

        ## start testing 
        self.starting = QtWidgets.QPushButton(self.centralwidget)
        self.starting.setGeometry(QtCore.QRect(430, 470, 99, 27))
        self.starting.setObjectName("btnOpenCamera")

        ## close
        self.btnClose = QtWidgets.QPushButton(self.centralwidget)
        self.btnClose.setGeometry(QtCore.QRect(430, 500, 99, 27))
        self.btnClose.setObjectName("btnOpenCamera")

        ## reset
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(600, 470, 99, 27))
        self.reset.setObjectName("btnOpenCamera")


        ## args
        self.btnArgs = QtWidgets.QPushButton(self.centralwidget)
        self.btnArgs.setGeometry(QtCore.QRect(700, 100, 99, 27))
        self.btnArgs.setObjectName("btnOpenCamera")

        ## connect two windows
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(10, 100, 101, 25))
        self.toolButton.setObjectName("toolButton")

        ## show video
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(220, 90, 471, 341))
        self.labelCamera.setObjectName("labelCamera")

        ## timer
        self.timer_box = QtWidgets.QLineEdit(self.centralwidget)
        self.timer_box.setGeometry(QtCore.QRect(30, 30, 81, 50))
        self.timer_box.setObjectName("timer")

        ## counter
        self.counter_box = QtWidgets.QLineEdit(self.centralwidget)
        self.counter_box.setGeometry(QtCore.QRect(150, 30, 81, 50))
        self.counter_box.setObjectName("counter")

        ## preparing
        self.state_box = QtWidgets.QTextEdit(self.centralwidget)
        self.state_box.setGeometry(QtCore.QRect(270, 30, 100, 50))
        self.state_box.setObjectName("preparing")

        ## wrong action
        self.error_box = QtWidgets.QTextEdit(self.centralwidget)
        self.error_box.setGeometry(QtCore.QRect(390, 30, 81, 50))
        self.error_box.setObjectName("error_action")


        mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        mainwindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainwindow)
        self.statusbar.setObjectName("statusbar")
        mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainwindow)
        self.starting.clicked.connect(mainwindow.start_testing)
        self.btnOpenCamera.clicked.connect(mainwindow.btnOpenCamera_Clicked)
        self.reset.clicked.connect(mainwindow.Reset)
        self.btnClose.clicked.connect(mainwindow.Close)
        self.btnArgs.clicked.connect(mainwindow.setArgs)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "MainWindow"))
        self.starting.setText(_translate("mainwindow", "Start"))
        self.btnOpenCamera.setText(_translate("mainwindow", "Open Camera"))
        self.reset.setText(_translate("mainwindow", "reset"))
        self.labelCamera.setText(_translate("mainwindow", "TextLabel"))
        self.timer_box.setText(_translate("mainwindow", "timer"))
        self.counter_box.setText(_translate("mainwindow", "counter"))
        self.state_box.setText(_translate("mainwindow", "state box"))
        self.error_box.setText(_translate("mainwindow", "error box"))
        self.btnClose.setText(_translate("mainwindow","close"))
        self.btnArgs.setText(_translate("mainwindow", "set arg"))
        self.toolButton.setText(_translate("mainwindow", "connect"))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 60, 61, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 60, 71, 26))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 60, 71, 26))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Dialog)

        self.lineEdit.textChanged.connect(Dialog.getArgs)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.lineEdit.setText(_translate("Dialog","arg1"))
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))