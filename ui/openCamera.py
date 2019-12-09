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
        # self.btnOpenCamera = QtWidgets.QPushButton(self.centralwidget)
        # self.btnOpenCamera.setGeometry(QtCore.QRect(130, 470, 99, 27))
        # self.btnOpenCamera.setObjectName("btnOpenCamera")

        ## start testing 
        self.starting = QtWidgets.QPushButton(self.centralwidget)
        self.starting.setGeometry(QtCore.QRect(360, 500, 99, 27))
        self.starting.setObjectName("btnOpenCamera")

        ## close
        # self.btnClose = QtWidgets.QPushButton(self.centralwidget)
        # self.btnClose.setGeometry(QtCore.QRect(330, 500, 99, 27))
        # self.btnClose.setObjectName("btnOpenCamera")

        ## stop
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(531, 500, 99, 27))
        self.reset.setObjectName("btnOpenCamera")


        ## connect two windows
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(160, 500, 99, 27))
        self.toolButton.setObjectName("toolButton")

        ## show video
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(140, 80, 500, 400))
        #self.labelCamera.setGeometry(QtCore.QRect(160, 90, 471, 341))
        self.labelCamera.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.labelCamera.setWordWrap(True)
        self.labelCamera.setObjectName("labelCamera")

        ## timer
        self.timer_box = QtWidgets.QLabel(self.centralwidget)
        self.timer_box.setGeometry(QtCore.QRect(30, 30, 90, 50))
        self.timer_box.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.timer_box.setWordWrap(True)
        self.timer_box.setObjectName("计时器")

        ## counter
        self.counter_box = QtWidgets.QLabel(self.centralwidget)
        self.counter_box.setGeometry(QtCore.QRect(230, 30, 90, 50))
        self.counter_box.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.counter_box.setWordWrap(True)
        self.counter_box.setObjectName("计数器")

        ## preparing
        self.state_box = QtWidgets.QLabel(self.centralwidget)
        self.state_box.setGeometry(QtCore.QRect(430, 30, 100, 50))
        self.state_box.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.state_box.setWordWrap(True)
        self.state_box.setObjectName("状态显示")

        ## wrong action
        self.error_box = QtWidgets.QLabel(self.centralwidget)
        self.error_box.setGeometry(QtCore.QRect(630, 30, 81, 50))
        self.error_box.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.error_box.setWordWrap(True)
        self.error_box.setObjectName("错误提示")


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
        #self.btnOpenCamera.clicked.connect(mainwindow.btnOpenCamera_Clicked)
        self.reset.clicked.connect(mainwindow.Reset)
        #self.btnClose.clicked.connect(mainwindow.Close)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "SAFLIGHT人工智能仰卧起坐测试仪"))
        self.starting.setText(_translate("mainwindow", "开始"))
        #self.btnOpenCamera.setText(_translate("mainwindow", "打开摄像头"))
        self.reset.setText(_translate("mainwindow", "停止"))
        self.labelCamera.setText(_translate("mainwindow", "画布显示"))
        self.timer_box.setText(_translate("mainwindow", "计时器"))
        self.counter_box.setText(_translate("mainwindow", "计数器"))
        self.state_box.setText(_translate("mainwindow", "状态提示"))
        self.error_box.setText(_translate("mainwindow", "错误提示"))
        #self.btnClose.setText(_translate("mainwindow","关闭"))
        # self.btnArgs.setText(_translate("mainwindow", "set arg"))
        self.toolButton.setText(_translate("mainwindow", "设置"))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.stgText = QtWidgets.QLineEdit(Dialog)
        self.stgText.setGeometry(QtCore.QRect(150, 20, 108, 26))
        self.stgText.setObjectName("lineEdit")
        self.sewText = QtWidgets.QLineEdit(Dialog)
        self.sewText.setGeometry(QtCore.QRect(150, 60, 108, 26))
        self.sewText.setObjectName("lineEdit_2")
        self.raiseFeetText = QtWidgets.QLineEdit(Dialog)
        self.raiseFeetText.setGeometry(QtCore.QRect(150, 100, 108, 26))
        self.raiseFeetText.setObjectName("lineEdit_3")
        self.hksText = QtWidgets.QLineEdit(Dialog)
        self.hksText.setGeometry(QtCore.QRect(150, 150, 108, 26))
        self.hksText.setObjectName("lineEdit_4")
        self.ratioDistanceText = QtWidgets.QLineEdit(Dialog)
        self.ratioDistanceText.setGeometry(QtCore.QRect(150, 190, 108, 26))
        self.ratioDistanceText.setObjectName("lineEdit_5")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 91, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 121, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 81, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 121, 21))
        self.label_5.setObjectName("label_5")
        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setGeometry(QtCore.QRect(170, 240, 80, 26))
        self.saveButton.setObjectName("saveButton")


        self.retranslateUi(Dialog)
        self.stgText.textChanged.connect(Dialog.getArgs)
        self.sewText.textChanged.connect(Dialog.getArgs)
        self.raiseFeetText.textChanged.connect(Dialog.getArgs)
        self.hksText.textChanged.connect(Dialog.getArgs)
        self.ratioDistanceText.textChanged.connect(Dialog.getArgs)
        #self.closeButton.clicked.connect(Dialog.cancel)
        self.saveButton.clicked.connect(Dialog.save)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog","stg:(5, 10)"))
        self.label_2.setText(_translate("Dialog", "sew:(90, 100)"))
        self.label_3.setText(_translate("Dialog", "raise_feet:(5, 10)"))
        self.label_4.setText(_translate("Dialog", "hks:(60, 80)"))
        self.label_5.setText(_translate("Dialog", "ratio_dis:(0.2, 0.8)"))
        self.saveButton.setText(_translate("Dialog", "保存"))
        #self.closeButton.setText(_translate("Dialog", "关闭"))
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))