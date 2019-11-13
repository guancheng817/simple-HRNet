import sys
import os
sys.path.insert(1, os.getcwd())
import torch
print(sys.path)
from scripts.sit_ups import sitUps
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication,QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from openCamera import Ui_Mainwindow, Ui_Dialog
from opts import parse_opts


class PyQtMainEntry(QMainWindow, Ui_Mainwindow, sitUps):
    def __init__(self, args):
        super().__init__()
        # self.main_ui = Ui_Mainwindow()
        # self.main_ui.setupUi(self)
        self.setupUi(self)

        self.args = args
        #self.main(self.args)
        self.count_down = 10
        self.num_of_before_click = 0

        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.btn_start = False

        self.is_camera_opened = False  # 摄像头有没有打开标记
        # self.timer_open_camera = QtCore.QTimer(self)
        # self.timer_open_camera.timeout.connect(self._queryFrame)
        # self.timer_open_camera.setInterval(30)
        self.reset_button = False
        self.flag = False
    def start_testing(self):
        '''
        start testing
        '''
        self.starting.setEnabled(False)
        self.flag = True
        if self.reset_button:
            self.count_down = 10

    def Reset(self):
        '''
        reset and restart
        :return:
        '''
        self.reset_button = True
        self.starting.setEnabled(True)
        self.btnOpenCamera.setEnabled(True)
        self.Counter(num_of_std=' ')  # counter clear
        self.timer_box.setText(' ')  # timer clear
        self.time.stop()
    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        frame_generator = self.main(self.args)

        if self.flag:
            self.Action()

        while True:
            if self.flag:
                self.Action()
                self.flag = False

            if self.starting.isEnabled():
                state_box_text, error_box_text, self.frame, num_of_std = next(frame_generator)
                self.num_of_before_click = num_of_std
            else:
                state_box_text, error_box_text, self.frame, num_of_std = next(frame_generator)
                num_of_std = num_of_std - self.num_of_before_click
                self.State_Box(state_box_text)
                self.Error_Box(error_box_text)
                self.Counter(num_of_std)


            img_rows, img_cols, channels = self.frame.shape
            bytesPerLine = channels * img_cols
            cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
            QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)

            self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            QApplication.processEvents()

    def Close(self):
        os._exit()
    def Action(self):
        #print(self.starting.isEnabled())
        if self.btnOpenCamera.isEnabled():
            self.time.start()
            self.btnOpenCamera.setEnabled(False)


    def Refresh(self):
        if self.count_down > 0:
            self.timer_box.setText('剩余：'+ str(self.count_down))
            self.count_down -= 1
            #print(self.count_down)
        else:
            print('debug in count less than 0',self.count_down)
            self.time.stop()
            #time.sleep(5)

    def Counter(self, num_of_std):
        self.counter_box.setText(str(num_of_std))


    def State_Box(self, state_box_text):
        #print(self.count_down)
        if self.count_down <= 0:
            self.state_box.setText('测试结束')
            #time.sleep(5)
        else:
            self.state_box.setText(state_box_text)

    def Error_Box(self, error_box_text):
        self.error_box.setText(error_box_text)

    def setArgs(self):
        dialog = QtWidgets.QDialog()
        btn = QPushButton("ok", dialog)
        btn.move(50, 50)
        self.arg1= QtWidgets.QLineEdit(dialog)
        self.arg1.setGeometry(QRect(70, 70, 81, 50))
        self.arg1.setObjectName("arg_1")
        self.arg1.textChanged.connect(self.getArgs)
        dialog.setWindowTitle("Dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def getArgs(self):
        args.stg = int(self.lineEdit.text())
        print(type(self.lineEdit_2.text()))
        args.sew = int(self.lineEdit_2.text())


    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片
        '''
        ret, self.frame = self.camera.read()
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols
        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class childWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, args):
        #super().__init__()
        QtWidgets.QDialog.__init__(self)
        self.args = args
        self.setupUi(self)
        # self.child=Ui_Dialog()
        # self.child.setupUi(self)

    def getArgs(self):

        args.stg = int(self.lineEdit.text())
        args.sew = int(self.lineEdit_2.text())
        print(type(args.stg))
        print(type(args.sew))
        print('stg',args.stg)
        print('sew',args.sew)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    args = parse_opts()
    child = childWindow(args)
    window = PyQtMainEntry(args)


    btn=window.toolButton
    btn.clicked.connect(child.show)

    window.show()
    sys.exit(app.exec_())
